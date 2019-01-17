from django.db import models
from django.utils import timezone

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.blocks import CharBlock, ListBlock
from wagtail.admin.edit_handlers import StreamFieldPanel, MultiFieldPanel
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.blocks import SnippetChooserBlock
from .blocks import SectionBlock, EventBlock
from .blocks import PersonBlock, PeopleBlock, ArticleBlock
from .blocks import CollectionChooserBlock
from .blocks import SectionedImageChooserBlock
from .blocks import SectionedDocChooserBlock


class ContextPage(Page):
    pub_date = models.DateTimeField()
    parent_page_types = []

    @property
    def sections(self):
        sblocks = []
        for field in getattr(self, 'body', []):
            if isinstance(field.block, SectionBlock):
                field.block.sid = len(sblocks)
                sblocks.append(field)
        return sblocks

    def get_context(self, request):
        context = super(ContextPage, self).get_context(request)
        # Add extra variables and return the updated context

        context['event_blocks'] = EventPage.latestEvents(5)
        recent_pages = ContextPage.objects.live()
        context['recent_pages'] = recent_pages.order_by('-pub_date')[:5]
        mroot = self.get_ancestors().type(self.__class__).first()
        context['menu_root'] = self if mroot is None else mroot
        context['page_children'] = self.get_children()

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

    @property
    def events(self):
        return EventPage.objects.get(title="Events")


class PleromaPage(ContextPage):
    body = StreamField([('person', PersonBlock()),
                        ('people', PeopleBlock()),
                        ('event', EventBlock()),
                        ('article', ArticleBlock())])
    content_panels = ContextPage.content_panels + [StreamFieldPanel('body')]
    parent_page_types = [PleromaHomePage]


class EventPage(ContextPage):
    body = StreamField([('event', EventBlock())], blank=True)
    content_panels = ContextPage.content_panels + [StreamFieldPanel('body')]
    parent_page_types = [PleromaHomePage]

    @classmethod
    def latestEvents(cls, count):
        ep = cls.objects.live().in_menu().get(title="Events")
        epbl = list(ep.body)
        epbl.sort(key=lambda x: x.value['start_date'], reverse=True)
        return epbl[:count]


EventPage.parent_page_types.insert(0, EventPage)


class ImageryPage(ContextPage):
    body = StreamField(
        [('image_chooser', SectionedImageChooserBlock()),
         ('collection_chooser', CollectionChooserBlock())],
        blank=True)

    content_panels = ContextPage.content_panels + [
        StreamFieldPanel('body')
    ]
    parent_page_types = [PleromaPage]


ImageryPage.parent_page_types.insert(0, ImageryPage)


class DocsPage(ContextPage):
    body = StreamField([('doc_chooser', SectionedDocChooserBlock())],
                       blank=True)

    content_panels = ContextPage.content_panels + [StreamFieldPanel('body')]
    parent_page_types = [PleromaPage]


DocsPage.parent_page_types.insert(0, DocsPage)
