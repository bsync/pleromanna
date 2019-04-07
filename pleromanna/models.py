from django.db import models
from django.utils import timezone
from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images import blocks as image_blocks
from wagtail.core import blocks as core_blocks
from commonblocks import blocks as common_blocks
from wagtailmenus.models import MenuPage


class SectionBlock(core_blocks.StructBlock):
    section = core_blocks.CharBlock(required=False)

    class Meta:
        icon = 'doc'


class PersonBlock(SectionBlock):
    first_name = core_blocks.CharBlock()
    middle_name = core_blocks.CharBlock(required=False)
    last_name = core_blocks.CharBlock()
    titles = core_blocks.CharBlock(required=False)
    photo = image_blocks.ImageChooserBlock()
    biography = common_blocks.SimpleRichTextBlock()

    class Meta:
        icon = 'user'
        template = 'blocks/person_block.html'


class PeopleBlock(SectionBlock):
    people = core_blocks.ListBlock(PersonBlock(required=False))
    group_photo = image_blocks.ImageChooserBlock()
    group_bio = common_blocks.SimpleRichTextBlock()

    class Meta:
        icon = 'user'
        template = 'blocks/people_block.html'


class EventBlock(SectionBlock):
    start_date = core_blocks.DateTimeBlock()
    stop_date = core_blocks.DateTimeBlock()
    photo = image_blocks.ImageChooserBlock(required=False)
    description = common_blocks.SimpleRichTextBlock(required=False)

    class Meta:
        icon = 'date'
        template = 'blocks/event_block.html'


class ArticleBlock(SectionBlock):
    image = image_blocks.ImageChooserBlock(required=False)
    paragraph = common_blocks.SimpleRichTextBlock()

    class Meta:
        icon = 'snippet'
        template = 'blocks/article_block.html'


class SectionedImageChooserBlock(SectionBlock):
    image_list = core_blocks.ListBlock(
                    image_blocks.ImageChooserBlock(required=False))

    class Meta:
        icon = 'image'
        template = 'blocks/image_chooser_block.html'


class SectionedDocChooserBlock(SectionBlock):
    doc_list = core_blocks.ListBlock(DocumentChooserBlock(required=False))

    class Meta:
        icon = 'doc'
        template = 'blocks/doc_chooser_block.html'


class CollectionChooserBlock(SectionBlock):
    import wagtail.core.models
    register_snippet(wagtail.core.models.Collection)
    collection = SnippetChooserBlock(wagtail.core.models.Collection)

    class Meta:
        icon = 'snippet'
        template = 'blocks/image_chooser_block.html'


class LinkBlock(SectionBlock):
    link = core_blocks.URLBlock()
    paragraph = common_blocks.SimpleRichTextBlock(required=False)

    class Meta:
        icon = 'link'
        template = 'blocks/link_block.html'


class ContextPage(MenuPage):
    pub_date = models.DateTimeField()

    @property
    def sections(self):
        """ Generate list of section name, id pairs for all sections """
        sblocks = []
        for field in getattr(self, 'body', []):
            if isinstance(field.block, SectionBlock):
                field.name = field.value['section']
                if isinstance(field.block, LinkBlock):
                    field.link = field.value['link']
                sblocks.append(field)
        return sblocks

    def get_context(self, request):
        context = super(ContextPage, self).get_context(request)
        context['event_blocks'] = EventPage.latestEvents(5)
        recent_pages = ContextPage.objects.live()
        context['recent_pages'] = recent_pages.order_by('-pub_date')[:5]
        mroot = self.get_ancestors().type(self.__class__).first()
        context['menu_root'] = self if mroot is None else mroot
        context['page_children'] = Page.objects.child_of(self)
        hp = Page.objects.type(PleromaHomePage).first().specific
        context['backdrop'] = hp.backdrop
        return context

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        self.pub_date = timezone.now()
        return super(ContextPage, self).save(*args, **kwargs)


class EventPage(ContextPage):
    body = StreamField([('event', EventBlock())], blank=True)
    content_panels = ContextPage.content_panels + [StreamFieldPanel('body')]
    template = 'pleromanna/events.html'

    def modify_submenu_items(self, menu_items, **kwargs):
        """
        If rendering a 'main_menu', add some additional menu items to the end
        of the list that link to various anchored sections on the same page.

        We're only making use 'original_menu_tag' and 'current_site' in this
        example, but `kwargs` should have all of the following keys:

        * 'current_page'
        * 'current_ancestor_ids'
        * 'current_site'
        * 'allow_repeating_parents'
        * 'apply_active_classes'
        * 'original_menu_tag'
        * 'menu_instance'
        * 'request'
        * 'use_absolute_page_urls'
        """
        # Start by applying default modifications
        menu_items = super(EventPage, self).modify_submenu_items(menu_items, **kwargs)

        if kwargs['original_menu_tag'] == 'main_menu':
            page_url = self.relative_url(kwargs['current_page'])
            """
            Additional menu items can be objects with the necessary attributes,
            or simple dictionaries. `href` is used for the link URL, and `text`
            is the text displayed for each link. Below, I've also used
            `active_class` to add some additional CSS classes to these items,
            so that I can target them with additional CSS
            """
            for evt in self.latestEvents():
                if evt.value['stop_date'] > timezone.now():
                    menu_items.append(( {
                            'text': evt.value['section'],
                            'href': page_url + "#{}".format(evt.id),
                        }))

        return menu_items

    def has_submenu_items(self, **kwargs):
        """
        Because `modify_submenu_items` is being used to add additional menu
        items, we need to indicate in menu templates that `EventPage` objects
        do have submenu items in main menus, even if they don't have children
        pages.

        We're only making use 'original_menu_tag' in this example, but
        `kwargs` should have all of the following keys:

        * 'current_page'
        * 'allow_repeating_parents'
        * 'original_menu_tag'
        * 'menu_instance'
        * 'request'
        """

        if kwargs['original_menu_tag'] == 'main_menu':
            return True
        # Resort to default behaviour
        return super(EventPage, self).has_submenu_items(**kwargs)

    @classmethod
    def latestEvents(cls, count=-1):
        ep = cls.objects.live().in_menu().get(title="Events")
        epbl = list(ep.body)
        tnow = timezone.now()
        epbl.sort(key=lambda x: x.value['start_date'], reverse=True)
        epfbl = list(filter(lambda x: x.value['stop_date'] > tnow, epbl))
        return epfbl[:count]


class ImageryPage(ContextPage):
    body = StreamField(
        [('image_chooser', SectionedImageChooserBlock()),
         ('collection_chooser', CollectionChooserBlock())],
        blank=True)
    content_panels = ContextPage.content_panels + [StreamFieldPanel('body')]


class DocsPage(ContextPage):
    body = StreamField([('doc_chooser', SectionedDocChooserBlock())],
                       blank=True)
    content_panels = ContextPage.content_panels + [StreamFieldPanel('body')]


class PleromaHomePage(ContextPage):
    backdrop = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+')
    heading = models.CharField(max_length=250)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+')
    notice = RichTextField(blank=True)
    paragraph = RichTextField()
    content_panels = ContextPage.content_panels + [
        ImageChooserPanel('backdrop'),
        FieldPanel('heading'),
        ImageChooserPanel('image'),
        FieldPanel('notice'),
        FieldPanel('paragraph', classname="full"), ]
    template = 'pleromanna/home_page.html'

    @property
    def events(self):
        return EventPage.objects.get(title="Events")


class PleromaPage(ContextPage):
    body = StreamField([('person',  PersonBlock()),
                        ('people',  PeopleBlock()),
                        ('event',   EventBlock()),
                        ('article', ArticleBlock()),
                        ('link',    LinkBlock()), ])
    content_panels = ContextPage.content_panels + [StreamFieldPanel('body')]
    template = 'pleromanna/page.html'


PleromaPage.parent_page_types = [PleromaHomePage, PleromaPage]
EventPage.parent_page_types = [EventPage, PleromaHomePage]
ImageryPage.parent_page_types = [ImageryPage, PleromaPage]
DocsPage.parent_page_types = [DocsPage, PleromaPage]


class LessonsPage(ContextPage):
    pass


LessonsPage.parent_page_types = [PleromaPage, LessonsPage]
