from django.db import models
from django.utils import timezone

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.blocks import CharBlock, ListBlock
from wagtail.admin.edit_handlers import StreamFieldPanel, MultiFieldPanel
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from .blocks import EventBlock, PersonBlock, PeopleBlock, ArticleBlock


class ContextPage(Page):
    pub_date = models.DateTimeField()
    parent_page_types = []

    @property
    def sections(self):
        try:
            return [x for x in self.body if x.block_type == 'section']
        except Exception:
            return []

    def get_context(self, request):
        context = super(ContextPage, self).get_context(request)
        # Add extra variables and return the updated context
        context['event_pages'] = EventPage.objects.live().order_by('pub_date')
        recent_pages = ContextPage.objects.live()
        context['recent_pages'] = recent_pages.order_by('-pub_date')[:5]
        for x, section in enumerate(self.sections):
            section.sid = x
        context['sections'] = self.sections
        return context

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        self.pub_date = timezone.now()
        return super(ContextPage, self).save(*args, **kwargs)


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
    parent_page_types = ['wagtailcore.Page']


class PleromaPage(ContextPage):
    body = StreamField([('section', CharBlock()),
                        ('person', PersonBlock()),
                        ('people', PeopleBlock()),
                        ('event', EventBlock()),
                        ('article', ArticleBlock())])
    content_panels = ContextPage.content_panels + [StreamFieldPanel('body')]
    parent_page_types = [PleromaHomePage]


class EventPage(ContextPage):
    body = StreamField([('section', CharBlock()),
                        ('event', EventBlock())], blank=True)
    content_panels = ContextPage.content_panels \
        + [StreamFieldPanel('body')]
    parent_page_types = [PleromaHomePage]

    @property
    def event_sections(self):
        sections = []
        events = []
        for block in self.body:
            if block.block_type == 'section':
                sections.insert(0, block)
            elif block.block_type == 'event':
                events.insert(0, block)
        return zip(sections, events)


EventPage.parent_page_types.insert(0, EventPage)


class ImageryPage(ContextPage):
    imagery = StreamField([('section', CharBlock()),
                          ('images', ListBlock(ImageChooserBlock()))])

    content_panels = ContextPage.content_panels + [
        StreamFieldPanel('imagery')
    ]
    parent_page_types = [PleromaPage]


ImageryPage.parent_page_types.insert(0, ImageryPage)


class DocsPage(ContextPage):
    docs = StreamField([('section', CharBlock()),
                        ('docs', ListBlock(DocumentChooserBlock()))])

    content_panels = ContextPage.content_panels + [
        StreamFieldPanel('docs')
    ]
    parent_page_types = [PleromaPage]


DocsPage.parent_page_types.insert(0, DocsPage)
