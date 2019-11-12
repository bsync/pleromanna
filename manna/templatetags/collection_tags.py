from django import template
from wagtail.core.models import Page
from wagtail.images.models import Image
import re


register = template.Library()
# https://docs.djangoproject.com/en/1.9/howto/custom-template-tags/


@register.inclusion_tag('tags/image_collection.html')
def image_collection(collection):
    def regexKey(x):
        try:
            xint = int(re.search(r'(\d+)', x.title).group(1))
        except IndexError:
            xint = 0
        return xint

    collected_images = list(Image.objects.filter(collection=collection.id))
    return {'images': sorted(collected_images,key=regexKey)}
