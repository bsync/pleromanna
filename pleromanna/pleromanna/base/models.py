from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmenus.models import MenuPage

class PleroPage(MenuPage):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    paragraph = RichTextField(null=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('image'),
        FieldPanel('paragraph', classname='full'), ]


class HomePage(PleroPage):
    template = 'home_page.html'

class ContainerPage(Page):
    pass
