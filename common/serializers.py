from rest_framework import serializers
from django.conf import settings

from .models import Media


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

    def get_file(self, obj):
        return str(settings.HOST) + str(obj.file.url)
