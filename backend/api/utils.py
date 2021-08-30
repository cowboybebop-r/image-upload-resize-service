import requests
import io

from PIL import Image as PILImage

from django.core.files.base import ContentFile
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import InMemoryUploadedFile


def get_file(url: str) -> ImageFile:
    """
    :returns image from url buffered to ImageFile
    :param url: str type object from request
    :return: ImageFile
    """
    extension = url.rsplit('.', 1)[1]
    filename = url.rsplit('/', 1)[1].rsplit('.', 1)[0]
    data = requests.get(url).content
    return ImageFile(io.BytesIO(data), name=filename + f'.{extension}')


def get_resized_image(im: PILImage, new_size: tuple, new_thumname: str) -> InMemoryUploadedFile:
    """
    :returns InMemoryUploadedFile object to save it to FileField
    :param im: PILImage of old image
    :param new_size: tuple with new height and width
    :param new_thumname: new thumbname of image
    :return:
    """
    new_image = im.resize(new_size)
    buffer = io.BytesIO()
    new_image.save(fp=buffer, format='JPEG')
    content_file = ContentFile(buffer.getvalue())
    return InMemoryUploadedFile(content_file, None, new_thumname, 'image/',
                                content_file.tell, None)


def get_new_size_by_ratio(new_width: int, new_height: int, im: PILImage) -> tuple:
    if new_width:
        return round(new_width / (im.size[1] / im.size[0])), new_width
    elif new_height:
        return new_height, round(new_height / (im.size[0] / im.size[1]))
