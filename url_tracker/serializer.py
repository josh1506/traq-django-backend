from rest_framework import serializers

from .models import Url, Viewer


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ('user', 'title', 'link', 'short_url', 'total_visitors')
        read_only_fields = ('total_visitors',)


class ViewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viewer
        fields = ('url', 'date_viewed')
        read_only_fields = ('date_viewed',)
