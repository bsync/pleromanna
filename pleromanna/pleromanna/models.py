from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.blocks import CharBlock
from wagtail.admin.edit_handlers import StreamFieldPanel, MultiFieldPanel
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from .blocks import EventBlock, PersonBlock, ArticleBlock


class ContextPage(Page):
    parent_page_types=[]

    @property
    def sections(self):
        try:
            return [x for x in self.body if x.block_type == 'section']
        except Exception:
            return []

    def get_context(self, request):
        context = super(ContextPage, self).get_context(request)
        # Add extra variables and return the updated context
        context['event_pages'] = EventPage.objects.live().order_by('year')
        for x, section in enumerate(self.sections):
            section.sid = x
        context['sections'] = self.sections
        return context


class PleromaHomePage(ContextPage):
    heading = models.CharField(max_length=250)
    subheading = models.CharField(max_length=250, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+')
    paragraph = RichTextField()
    content_panels = Page.content_panels + [
        FieldPanel('heading'),
        FieldPanel('subheading'),
        ImageChooserPanel('image'),
        FieldPanel('paragraph', classname="full"), ]

class PleromaPage(ContextPage):
    body = StreamField([('section', CharBlock()),
                        ('person', PersonBlock()),
                        ('event', EventBlock()),
                        ('article', ArticleBlock())])
    content_panels = ContextPage.content_panels + [StreamFieldPanel('body')]
    parent_page_types=[PleromaHomePage]


class EventPage(ContextPage):
    year = models.PositiveSmallIntegerField()
    body = StreamField([('section', CharBlock()),
                        ('event', EventBlock())], blank=True)
    content_panels = ContextPage.content_panels \
                   + [FieldPanel('year'), StreamFieldPanel('body')]
    parent_page_types=[PleromaHomePage]

    @property
    def event_sections(self):
        sections = []
        events = []
        for block in self.body:
            if block.block_type == 'section':
                sections.append(block)
            elif block.block_type == 'event':
                events.append(block)
        return zip(sections, events)



