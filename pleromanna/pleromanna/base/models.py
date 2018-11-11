from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtailmenus.models import MenuPage
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core import blocks as core_blocks
from wagtail.images import blocks as image_blocks
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel
from .blocks import PersonBlock, EventBlock


class PleromaHomePage(Page):
    heading = models.CharField(max_length=256)
    image = models.ForeignKey('wagtailimages.Image', null=True,
                              on_delete=models.SET_NULL)
    paragraph = RichTextField()
    content_panels = Page.content_panels \
                   + [  FieldPanel('heading'),
                        ImageChooserPanel('image'),
                        FieldPanel('paragraph'), ]

    def get_context(self, request):
        context = super(PleromaHomePage, self).get_context(request)
        # Add extra variables and return the updated context
        context['event_pages']=EventPage.objects.all().live()
        return context


class PleromaPage(MenuPage):
    body = StreamField([
        ('heading', core_blocks.CharBlock(classname="full title")),
        ('subheading', core_blocks.CharBlock(classname="full title")),
        ('paragraph', core_blocks.RichTextBlock()),
        ('image', image_blocks.ImageChooserBlock()),
        ('person', PersonBlock()),
        ('html', core_blocks.RawHTMLBlock()),
    ])

    content_panels = MenuPage.content_panels + [
        StreamFieldPanel('body'),
    ]


class EventPage(MenuPage):
    events = StreamField([('event', EventBlock()), ], blank=True)

    content_panels = MenuPage.content_panels + [
        StreamFieldPanel('events'),
    ]
