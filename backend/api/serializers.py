from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

from django.db import transaction

from api.models import Image
from api.utils import get_file


class ImageDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'name', 'url', 'picture', 'width', 'height', 'parent_picture')


class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('file', 'url')

    def create(self, validated_data):
        picture = validated_data.get('file')
        url = validated_data.get('url')

        if picture is None and url is '':
            raise serializers.ValidationError(
                _('You must fill in at least one field'))
        with transaction.atomic():
            instance = self.Meta.model.save_image(**validated_data)
        return instance

    def validate(self, attrs):
        if attrs['file'] and attrs['url'] is not '':
            raise serializers.ValidationError(
                _('Two field'))
        if attrs['url'] != '':
            attrs['file'] = get_file(str(attrs['url']))
            return attrs
        return attrs


class ImageResizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('width', 'height')

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance = self.Meta.model.resize_image(instance, **validated_data)

        return instance
