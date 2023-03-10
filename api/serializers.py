from rest_framework import serializers
from databank.models import Work, Artist


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ["name", "factor"]


class WorkSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
    image_url = serializers.SerializerMethodField("get_image_url")

    class Meta:
        model = Work
        fields = ["id", "artist", "image_url", "name",
                  "production_date", "materials", "width", "height", "depth", "price"]

    def get_image_url(self, obj):
        return obj.image.url