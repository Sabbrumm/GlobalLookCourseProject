from rest_framework import serializers

class GeoLocationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    name = serializers.CharField(max_length=100)

class PersonaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=512)