from django.db import models

from wagtail.core.models import Page
from wagtailmenus.models import MenuPageMixin
from wagtailmenus.panels import menupage_panel
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock


class BasicPage(Page, MenuPageMixin):
    settings_panels = [menupage_panel]

    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    content_panels = Page.content_panels + [StreamFieldPanel('body')]
