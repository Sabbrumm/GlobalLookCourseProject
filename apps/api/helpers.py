import re
import signal
import warnings
from queue import Queue
from threading import Thread, Event

from razdel import sentenize
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    Doc
)

from bs4 import BeautifulSoup
from datetime import date, timedelta

from apps.api.models import GeoLocation, Persona, Article

import requests


class LentaParser:

    @staticmethod
    def parse_topics(topic_date: date) -> dict:
        url = "https://lenta.ru"

        result = {}
        req = requests.get(url + topic_date.strftime("/%Y/%m/%d/"), "html")

        if req.status_code != 200:
            print(f"{url} stsus code:{req.status_code}")
            return {}

        soup = BeautifulSoup(req.text, "html.parser")

        if soup.find('title').get_text() == "Страница не найдена" or \
                soup.find('li', class_="archive-page__no-topics") is not None:
            return {}

        for item in soup.find_all('a', class_='card-full-news _archive'):
            titleurl = url + item.get('href')
            title = item.find('h3').get_text()
            result[title] = titleurl

        return result

    @staticmethod
    def get_text(url: str) -> str:
        req = requests.get(url, "html")
        if req.status_code != 200:
            warnings.warn(f"Can't get data from url: {url} status code: {req.status_code}'")
            return ''

        soup = BeautifulSoup(req.text, "html.parser")
        if soup.find('title').get_text() == "Страница не найдена":
            return ''

        res = soup.find('div', class_="topic-body__content").get_text(separator=" ", strip=True)
        res = re.sub(r"\s\s+", " ", res)

        return res

    @staticmethod
    def analyze_text(text:str) -> dict:
        if text == '':
            return {}

        res_locs = []
        res_names = []
        result = {}

        segmenter = Segmenter()
        morph_vocab = MorphVocab()
        emb = NewsEmbedding()
        morph_tagger = NewsMorphTagger(emb)
        syntax_parser = NewsSyntaxParser(emb)
        ner_tagger = NewsNERTagger(emb)
        doc = Doc(text)

        doc.segment(segmenter)
        doc.tag_ner(ner_tagger)
        doc.parse_syntax(syntax_parser)
        doc.tag_morph(morph_tagger)

        for span in doc.spans:
            span.normalize(morph_vocab)
            if (span.type == "PER" or span.type == "ORG") and (not (span.normal in res_names)):
                res_names.append(span.normal)
            if span.type == "LOC" and not (span.normal in res_locs):
                res_locs.append(span.normal)

        result['pers'] = res_names
        result['locs'] = res_locs

        return result

    @staticmethod
    def parse(url: str) -> dict | None:
        req = requests.get(url, "html")

        if req.status_code != 200:
            warnings.warn(f"Can't get data from url: {url} status code: {req.status_code}'")
            return None

        soup = BeautifulSoup(req.text, "html.parser")

        if soup.find('title').get_text() == "Страница не найдена":
            return None

        title = soup.find('span', class_="topic-body__title").get_text()
        try:
            image_url = soup.find('img', class_="picture__image").get('src')
        except:
            image_url = 'https://icdn.lenta.ru/assets/webpack/images/stubs/no_image/owl_detail_240.b92f8801.jpg'

        data = {"url": url}

        data['title'] = title
        data['image_url'] = image_url

        text = LentaParser.get_text(url)

        locs_and_pers = LentaParser.analyze_text(text)
        data['locs'] = []

        for loc in locs_and_pers['locs']:
            lat, lng = LentaParser.geo_lookup(loc)
            if lat is not None and lng is not None:
                data['locs'].append({'name': loc, 'latitude': lat, 'longitude': lng})

        data['pers'] = []
        for pers in locs_and_pers['pers']:
            data['pers'].append({'name': pers})

        sentences = list(sentenize(text))
        data['subtitle'] = sentences[0].text
        data['content'] = " ".join([_.text for _ in sentences[1:]])

        post_date = re.findall(r"\d{4}/\d{2}/\d{2}", url)[0]
        post_date = post_date.replace('/', '-')
        data['date'] = post_date

        return data

    @staticmethod
    def geo_lookup(query: str) -> (float, float):
        # вернет координаты геолокации

        response = requests.get(f"https://nominatim.openstreetmap.org/search",
                                headers={'Accept': 'application/json', 'User-Agent': 'GlobalLook Crawler'},
                                params={'q': query, 'format': 'json'})
        geo_data = response.json()
        if geo_data:
            geo_lat = float(geo_data[0]['lat'])
            geo_lon = float(geo_data[0]['lon'])
            return geo_lat, geo_lon

        return None, None


class LentaCrawlerTask(object):
    task_type:str
    task_date:date
    task_date_range: tuple[date, date]
    is_done:bool
    task_result:list
    def done(self, task_result):
        self.is_done = True
        self.task_result = task_result


class LentaCrawlerTaskRange(LentaCrawlerTask):
    def __init__(self, range_start: date, range_end: date):
        self.task_type:str = 'parse_range'
        self.task_date_range = (range_start, range_end)


class LentaCrawlerTaskSingle(LentaCrawlerTask):
    def __init__(self, single_date: date):
        self.task_type:str = 'parse_single'
        self.task_date = single_date


class LentaCrawler:
    """
    В классе реализована логика парсинга новостей

    Каждые 10 минут запускается задача по парсу, которую можно включить/отключить
    Помимо этого в очередь можно добавлять задачи на парсинг по отдельной дате
    Или по диапазону дат
    """

    # 10 минут
    REQUEST_DELAY = 10 * 60

    def __init__(self, do_refresh: bool = True):
        self._task_queue = Queue()
        self._constant_parsing = do_refresh
        self._exit_event = Event()
        self.task1_end = False
        self.task2_end = False
        for sig in ('TERM', 'INT'):
            signal.signal(getattr(signal, 'SIG' + sig), self.stop)

    def _crawl(self, crawl_date: date):
        print("Parsing: " + crawl_date.strftime("%Y-%m-%d"))
        parser = LentaParser()
        topics = parser.parse_topics(crawl_date)
        created_geos = 0
        created_pers = 0
        created_posts = 0
        for topic in topics:
            if self._exit_event.is_set(): break
            obj = parser.parse(topics[topic])
            geos = []
            pers_s = []

            for loc in obj['locs']:
                geo, created = GeoLocation.objects.get_or_create(
                    name=loc['name'],
                    latitude=loc['latitude'],
                    longitude=loc['longitude']
                )
                geos.append(geo)
                created_geos += created

            for pers in obj['pers']:
                pers, created = Persona.objects.get_or_create(
                    name=pers['name']
                )
                pers_s.append(pers)
                created_pers += created


            post, created = Article.objects.get_or_create(
                title=obj['title'],
                subtitle=obj['subtitle'],
                content=obj['content'],
                date=obj['date'],
                image_url=obj['image_url'],
            )
            if created:
                post.personas.set(pers_s)
                post.locations.set(geos)
            created_posts += created
        print("Created {} geos".format(created_geos))
        print("Created {} persons".format(created_pers))
        print("Created {} posts".format(created_posts))
        result = {
            "created_geos": created_geos,
            "created_pers": created_pers,
            "created_posts": created_posts
        }
        return result


    def _crawl_range(self, range:(date, date)):
        range_start, range_end = range
        print(range_start, range_end)
        ret = []
        while range_start < range_end:
            ret.append(self._crawl(range_start))
            range_start = range_start + timedelta(days=1)
            print(range_start, range_end)
        return ret

    def crawl(self, crawl_date: date):
        self._task_queue.put_nowait(LentaCrawlerTaskSingle(crawl_date))

    def put_task(self, task:LentaCrawlerTask):
        self._task_queue.put_nowait(task)

    def crawl_range(self, range_start: date, range_end: date):
        self._task_queue.put_nowait(LentaCrawlerTaskRange(range_start, range_end))

    def enable_constant_parsing(self):
        self._constant_parsing = True

    def disable_constant_parsing(self):
        self._constant_parsing = False

    def _constant_parsing_queue_manager(self):
        print("LentaCrawler parsing manager started")
        while not self._exit_event.is_set():
            if self._constant_parsing:
                self._task_queue.put(LentaCrawlerTaskSingle(date.today()))
            self._exit_event.wait(self.REQUEST_DELAY)
        print("LentaCrawler parsing manager stopped")
        self.task2_end = True
    def _executor(self):
        print('LentaCrawler Task executor started')
        while not self._exit_event.is_set():
            task = self._task_queue.get()
            res = None
            if task.task_type == 'parse_single':
                res = [self._crawl(task.task_date)]
            elif task.task_type == 'parse_range':
                res = self._crawl_range(task.task_date_range)
            task.done(res)
        print('LentaCrawler Task executor stopped')
        self.task1_end = True
    def stop(self, *args):
        print('Stopping LentaCrawler instance')
        self._task_queue = Queue()
        self._exit_event.set()
        while not (self.task1_end and self.task2_end):
            pass
        exit(0)
    def start(self):
        thread1 = Thread(target=self._constant_parsing_queue_manager)
        thread2 = Thread(target=self._executor)
        thread1.start()
        thread2.start()
        print('Started LentaCrawler instance')

    def __del__(self):
        self.stop()