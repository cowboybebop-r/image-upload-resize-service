import sys

from PIL import Image as PILImage
from django.conf import settings

from django.db import models

from api.utils import get_new_size_by_ratio, get_resized_image


class Image(models.Model):
    name = models.CharField('Название', max_length=255, null=True)
    url = models.URLField('Ссылка', blank=True, null=True)
    file = models.ImageField('Файл', max_length=255, null=True)
    picture = models.CharField('Изображение', max_length=1024, null=True, blank=True)
    width = models.PositiveIntegerField('Ширина', null=True)
    height = models.PositiveIntegerField('Высота', null=True)
    parent_picture = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Родитель', null=True)

    @classmethod
    def save_image(cls, file, *args, **kwargs):
        """
        Method for resizing Image using Pillow
        :param file: file from request
        :param args: None
        :param kwargs: serialized data
        :return:
        """
        obj = cls.objects.create(file=file)

        if obj.file:
            image_path = str(obj.file.path)
            image_url = str(obj.file.url)

            im = PILImage.open(image_path).convert('RGB')

            extension = image_path.rsplit('.', 1)[1]
            filename = image_path.rsplit('/', 1)[1].rsplit('.', 1)[0]
            fullpath = image_path.rsplit('/', 1)[0]
            url = image_url.rsplit('/', 1)[0]

            if extension not in ['jpg', 'jpeg', 'gif', 'png']:
                sys.exit()

            height, width = im.size
            obj.name = filename
            obj.height = height
            obj.width = width
            im.thumbnail((height, width), PILImage.ANTIALIAS)

            thumbname = filename + f'.{extension}'
            im.save(fullpath + f'/{thumbname}')
            obj.picture = url + f'/{thumbname}'

            obj.save()
        return obj

    @classmethod
    def resize_image(cls, instance, *args, **kwargs):
        """
        Method for resizing Image using Pillow
        :param instance: Image object
        :param args: empty
        :param kwargs: validated data from serializer
        :return:
        """
        new_height, new_width = kwargs['height'], kwargs['width']

        image_path = str(instance.file.path)

        filename = image_path.rsplit('/', 1)[1].rsplit('.', 1)[0]
        extension = image_path.rsplit('.', 1)[1]

        im = PILImage.open(image_path).convert('RGB')
        new_size = get_new_size_by_ratio(new_width, new_height, im)

        new_filename = filename + f'.{extension}_0_{new_size[0]}' if new_height \
            else filename + f'.{extension}_{new_size[1]}_0'

        new_thumname = new_filename + f'.{extension}'
        thumb_file = get_resized_image(im, new_size, new_thumname)

        obj = cls.objects.create(
            file=thumb_file,
            name=new_filename,
            width=new_size[1],
            height=new_size[0],
            picture=settings.MEDIA_URL + new_thumname,
            parent_picture=instance,
        )

        return obj

    class Meta:
        db_table = 'picture'
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
