from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    re_path(r'feed/?', views.feed, name='feed'),
    re_path(r'geo/?', views.geo, name='geo'),
    re_path(r'article/[0-9]*.?', views.article, name='article'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
