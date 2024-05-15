from rest_framework.response import Response
from rest_framework.views import APIView
from .models import GeoLocation, Persona
from .serializers import GeoLocationSerializer, PersonaSerializer


class GetGeoByName(APIView):
    def get(self, request):
        name = request.query_params.get('name', '')
        print(name)
        if name:
            geo_locations = GeoLocation.objects.filter(name__icontains=name)[:3]
        else:
            geo_locations = []
        serializer = GeoLocationSerializer(geo_locations, many=True)

        return Response(serializer.data)


class GetGeoByLatLong(APIView):
    def get(self, request):
        lat = request.query_params.get('lat', '')
        long = request.query_params.get('long', '')
        print(lat)
        print(long)
        if lat and long:
            geo_locations = GeoLocation.objects.filter(latitude=lat, longitude=long)
        else:
            geo_locations = []
        serializer = GeoLocationSerializer(geo_locations, many=True)

        return Response(serializer.data[0])


class GetPersonaByName(APIView):
    def get(self, request):
        name = request.query_params.get('name', '')
        if name:
            geo_locations = Persona.objects.filter(name__icontains=name)[:3]
        else:
            geo_locations = []
        serializer = PersonaSerializer(geo_locations, many=True)
        return Response(serializer.data)

