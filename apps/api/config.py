from datetime import date, timedelta

from django.apps import AppConfig

crawler = None

def create_crawler():
    from .helpers import LentaCrawler
    global crawler
    if crawler is not None:
        return crawler
    crawler = LentaCrawler()
    crawler.start()
    return crawler

class ApiConfig(AppConfig):
    name = 'apps.api'
    label = 'apps_api'

    def ready(self):
        create_crawler()