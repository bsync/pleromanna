from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.blocks import CharBlock, RichTextBlock, ListBlock
from wagtail.images import blocks as image_blocks
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet
from .blocks import PersonBlock, EventBlock


class PleromaHomePage(Page):
    heading = models.CharField(max_length=256)
    image = models.ForeignKey('wagtailimages.Image', null=True,
                              on_delete=models.SET_NULL)
    paragraph = RichTextField()
    content_panels = Page.content_panels + [
                        FieldPanel('heading'),
                        ImageChooserPanel('image'),
                        FieldPanel('paragraph'), ]

    def get_context(self, request):
        context = super(PleromaHomePage, self).get_context(request)
        # Add extra variables and return the updated context
        context['event_pages'] = EventPage.objects.live().order_by('year')
        return context


class PleromaPage(Page):
    body = StreamField([
        ('heading', CharBlock(classname="full title")),
        ('subheading', CharBlock(classname="full title")),
        ('paragraph', RichTextBlock()),
        ('image', image_blocks.ImageChooserBlock()),
        ('person', PersonBlock()),
    ])

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]


class EventPage(Page):

    year = models.PositiveSmallIntegerField()
    events = StreamField([('events', EventBlock())], blank=True)
    content_panels = Page.content_panels + [
                        FieldPanel('year'),
                        StreamFieldPanel('events')]


@register_snippet
class FooterText(models.Model):
    """
    This provides editable text for the site footer. Again it uses the
    decorator `register_snippet` to allow it to be accessible via the admin. It
    is made accessible on the template via a template tag defined in
    base/templatetags/ navigation_tags.py
    """
    body = RichTextField()

    panels = [
        FieldPanel('body'),
    ]

    def __str__(self):
        return "Footer text"

    class Meta:
        verbose_name_plural = 'Footer Text'


