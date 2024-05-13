import base64
import datetime

from django import template
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import folium
from folium.plugins import FastMarkerCluster, MarkerCluster

from apps.api.models import GeoLocation
from apps.home.models import Post

@login_required(login_url="/login/")
def article(request):
    context = {'segment': 'article'}
    try:
        article_id = int(request.path.split('/')[-1].split('?')[0])
        post = Post.objects.get(id=article_id)
    except Post.DoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

    map = folium.Map(location=[0, 0], zoom_start=1)
    for loc in post.locations.all():
        lat = float(loc.latitude)
        lng = float(loc.longitude)

        folium.Marker(location=[lat, lng],
                      icon=folium.Icon(color="red", icon="")).add_to(map)
    from_redirect = request.GET.get('from')
    if from_redirect is not None:
        from_redirect = from_redirect.replace(' ', '+')
        context['from_redirect'] = base64.b64decode(from_redirect).decode('utf-8')

    context['post'] = post
    context['map'] = map._repr_html_()
    html_template = loader.get_template('home/article.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def feed(request:WSGIRequest):
    context = {'segment': 'feed'}
    args_dict = request.GET

    #Получаем страницу
    page = args_dict.get('page')
    try:
        page = int(page)
    except:
        page = 1

    kwargs = {}
    href_tags = ""
    #Получаем персоны
    persons = args_dict.get('persons').split(',') if args_dict.get('persons') else None
    if persons is not None:
        kwargs['personas__name__in'] = persons
    href_tags += f"&persons={','.join(persons)}" if persons is not None else ""

    #Получаем гео
    lat = args_dict.get('lat')
    lng = args_dict.get('lng')
    if lat and lng:
        lat = float(lat)
        lng = float(lng)
        kwargs['locations__latitude__gt'] = lat - 0.001
        kwargs['locations__latitude__lt'] = lat + 0.001
        kwargs['locations__longitude__gt'] = lng - 0.001
        kwargs['locations__longitude__lt'] = lng + 0.001

    href_tags+= f"&lat={lat}&lng={lng}" if lat and lng else ""
    #Получаем дату

    date_from = args_dict.get('date_start')
    date_to = args_dict.get('date_end')

    if date_from:
        kwargs['date__gte'] = datetime.datetime.strptime(date_from, '%Y-%m-%d')
    if date_to:
        kwargs['date__lte'] = datetime.datetime.strptime(date_to, '%Y-%m-%d')

    href_tags+= f"&date_start={date_from}&date_end={date_to}" if date_from or date_to else ""

    total_posts = Post.objects.filter(**kwargs).count()
    total_pages = total_posts // 8 + 1
    if page > total_pages:
        page = total_pages
    elif page < 1:
        page = 1

    posts = Post.objects.filter(**kwargs).order_by('-date')[8 * (page - 1):8 * (page)]

    context['page'] = page
    context['total_pages'] = total_pages

    pg_nums = list(set([1] + [page-1 if page>1 else 1, page, page+1 if page<total_pages else 1]
                       + [total_pages]))
    context['pg_nums'] = pg_nums

    context['posts'] = posts
    lat = 0
    lng = 0

    map = folium.Map(location=[lat, lng], zoom_start=20)
    marker = folium.Marker(
        [lat, lng],
        zoom_start=20,
        icon=folium.Icon(color="red", icon="")
    ).add_to(map)

    #map.add_child(folium.LatLngPopup())

    """    {map}.on("click", replaceMarker);
    
    function replaceMarker(e) {
        {marker}.setLatLng(e.latlng);
        {marker}.draggable = true;
        window.parent.document.getElementById('lat-input').value = {marker}.getLatLng().lat;
        window.parent.document.getElementById('lng-input').value = {marker}.getLatLng().lng;
    }"""


    map.get_root().html.add_child(
        folium.Element(
            """
    <script type="text/javascript">
    $(document).ready(function () {
    window.parent.filter_marker = {marker};
    window.parent.filter_map = {map};

    });

    </script>
    """.replace(
                "{map}", map.get_name()
            )
        .replace(
                "{marker}", marker.get_name()
            )
        )
    )
    map = map._repr_html_()
    context['map'] = map
    context['href_tags'] = href_tags
    context['pg_prev'] = page-1
    context['pg_next'] = page+1
    context['href_b64'] = base64.b64encode(href_tags.encode('utf-8')).decode()
    html_template = loader.get_template('home/feed.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def geo(request):
    context = {'segment': 'geo'}

    args_dict = request.GET

    # Получаем страницу
    page = args_dict.get('page')
    try:
        page = int(page)
    except:
        page = 1

    kwargs = {}
    href_tags = ""
    # Получаем персоны
    persons = args_dict.get('persons').split(',') if args_dict.get('persons') else None
    if persons is not None:
        kwargs['personas__name__in'] = persons
    href_tags += f"&persons={','.join(persons)}" if persons is not None else ""

    # Получаем гео
    lat = args_dict.get('lat')
    lng = args_dict.get('lng')
    if lat and lng:
        lat = float(lat)
        lng = float(lng)
        kwargs['locations__latitude__gt'] = lat - 0.001
        kwargs['locations__latitude__lt'] = lat + 0.001
        kwargs['locations__longitude__gt'] = lng - 0.001
        kwargs['locations__longitude__lt'] = lng + 0.001

    href_tags += f"&lat={lat}&lng={lng}" if lat and lng else ""
    # Получаем дату

    date_from = args_dict.get('date_start')
    date_to = args_dict.get('date_end')

    if date_from:
        kwargs['date__gte'] = datetime.datetime.strptime(date_from, '%Y-%m-%d')
    if date_to:
        kwargs['date__lte'] = datetime.datetime.strptime(date_to, '%Y-%m-%d')

    href_tags += f"&date_start={date_from}&date_end={date_to}" if date_from or date_to else ""
    posts = Post.objects.filter(**kwargs).order_by('-date')
    lats = []
    lngs = []
    titles = []
    imgs = []
    popups = []
    hrefs = []
    ids = []
    for post in posts:
        locations = post.locations.all()
        html_popup = folium.Html("""
                <div class="card border-0 align-items-center">
                    <h4>{header}</h4>
                    <img class="d-none d-md-flex" src="{image}" class="">
                    <br></br>
                    <button class="btn btn-primary" type="button">
                        <span>Читать</span>
                    </button>
                </div>
        """.replace("{header}", post.title).replace("{image}", post.image_url))
        for location in locations:
            imgs.append(post.image_url)
            titles.append(post.title)
            lats.append(location.latitude)
            lngs.append(location.longitude)
            hrefs.append("/article/" + str(post.id))
            ids.append(post.id)
            popups.append(html_popup.render())

    data = list(zip(lats, lngs, titles, imgs, hrefs, ids))
    callback = ('function (row) {'
                'var marker = L.marker(new L.LatLng(row[0], row[1]), {color: "red"});'
                'var icon = L.AwesomeMarkers.icon({'
                "icon: 'info-sign',"
                "iconColor: 'white',"
                "markerColor: 'green',"
                "prefix: 'glyphicon',"
                "extraClasses: 'fa-rotate-0'"
                '});'
                'marker.setIcon(icon);'
                "var popup = L.popup({maxWidth: '300'});"
                "const display_text = {text: row[2], img: row[3], href: row[4], id: row[5]};"
                "var mytext2 = $(`<div id='mytext2' class='card border-0 align-items-center'><h4>${display_text.text}</h4><img class='d-none d-md-flex' src='${display_text.img}'><br></br><button id='button${display_text.id}' onclick='(function(){window.parent.document.location.href = \"${display_text.href}\"; })();' class='btn btn-primary' type='button'><span>Читать</span></button></div>`)[0];"
                "popup.setContent(mytext2);"
                "console.log(popup);"
                "marker.bindPopup(popup);"
                "$(`#button${display_text.id}`).on('click', function () {"
                "alert(display_text.text);"
                "window.parent.document.location.href = row[4];"
                "});"
                'return marker};')
    groups = FastMarkerCluster(data=data, popups=popups, callback=callback)




    lat = 0
    lng = 0

    map = folium.Map(location=[lat, lng], zoom_start=1)

    groups.add_to(map)
    context['map'] = map._repr_html_()

    html_template = loader.get_template('home/geo.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
