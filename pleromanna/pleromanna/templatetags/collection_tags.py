from django import template
from wagtail.core.models import Page
from wagtail.images.models import Image


register = template.Library()
# https://docs.djangoproject.com/en/1.9/howto/custom-template-tags/


@register.inclusion_tag('tags/image_collection.html')
def render_image_collection(collection):
    collected_images = Image.objects.filter(collection=collection.id)
    return {'images': collected_images}
