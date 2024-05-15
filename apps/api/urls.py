from django.urls import path
from .views import GetGeoByName, GetPersonaByName, GetGeoByLatLong

urlpatterns = [
    path('api/getgeobyname', GetGeoByName.as_view(), name="geobyname"),
    path('api/getpersonabyname', GetPersonaByName.as_view(), name="personabyname"),
    path('api/getgeobylatlong', GetGeoByLatLong.as_view(), name="geobylatlong"),
]
