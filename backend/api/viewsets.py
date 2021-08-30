from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import Image

from api.serializers import ImageDetailListSerializer, ImageCreateSerializer, ImageResizeSerializer


class ImageViewSet(viewsets.ModelViewSet):
    """
    List all images, or create a new image.
    """
    queryset = Image.objects.all()
    serializer_class = ImageResizeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ImageDetailListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ImageDetailListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ImageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ImageDetailListSerializer(instance)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def resize(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(serializer.data)
