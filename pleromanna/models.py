import os
from django.db import models
from django.db.models import DateTimeField
from django.utils import timezone
from django.utils.html import format_html
from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmedia.models import AbstractMedia
from wagtail.embeds.blocks import EmbedBlock
from wagtail.snippets.models import register_snippet
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images import blocks as image_blocks
from wagtailmedia.blocks import AbstractMediaChooserBlock
from wagtail.core import blocks as core_blocks
from commonblocks import blocks as common_blocks
from .vimeoresource import vc


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


class ContextPage(Page):
    pub_date = DateTimeField()

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
        # Add extra variables and return the updated context

        context['event_blocks'] = EventPage.latestEvents(5)
        recent_pages = ContextPage.objects.live()
        context['recent_pages'] = recent_pages.order_by('-pub_date')[:5]
        mroot = self.get_ancestors().type(self.__class__).first()
        context['menu_root'] = self if mroot is None else mroot

        return context

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        self.pub_date = timezone.now()
        return super(ContextPage, self).save(*args, **kwargs)


class EventPage(ContextPage):
    body = StreamField([('event', EventBlock())], blank=True)
    content_panels = ContextPage.content_panels + [StreamFieldPanel('body')]

    @classmethod
    def latestEvents(cls, count):
        ep = cls.objects.live().in_menu().get(title="Events")
        epbl = list(ep.body)
        epbl.sort(key=lambda x: x.value['start_date'], reverse=True)
        return epbl[:count]


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
    heading = models.CharField(max_length=250)
    subheading = models.CharField(max_length=250, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+')
    notice = RichTextField(blank=True)
    paragraph = RichTextField()
    content_panels = ContextPage.content_panels + [
        FieldPanel('heading'),
        FieldPanel('subheading'),
        ImageChooserPanel('image'),
        FieldPanel('notice'),
        FieldPanel('paragraph', classname="full"), ]

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


PleromaPage.parent_page_types = [PleromaHomePage, PleromaPage]
EventPage.parent_page_types = [EventPage, PleromaHomePage]
ImageryPage.parent_page_types = [ImageryPage, PleromaPage]
DocsPage.parent_page_types = [DocsPage, PleromaPage]


class SectionedVimeoBlock(SectionBlock):
    album = core_blocks.ChoiceBlock(choices=vc.listAlbumChoices, required=True)

    def clean(self, value):
        result = super(SectionedVimeoBlock, self).clean(value)
        if not result['section']:
            result['section'] = vc.album_name_for(result['album'])
        return result

    class Meta:
        icon = 'media'
        template = 'blocks/sectioned_vimeo_block.html'

        class SectionedVimeoValue(core_blocks.StructValue):
            def album_name(self):
                album = self.get('album')
                # page = self.get('page')
                return vc.album_name_for(album)

            def embed_html(self):
                album = self.get('album')
                # page = self.get('page')
                return vc.album_embed_html_for(album)
        value_class = SectionedVimeoValue


class LatestLessonsPage(ContextPage):

    parent_page_types = [PleromaPage]

    def get_context(self, request):
        context = super(LatestLessonsPage, self).get_context(request)
        lv = context['latest'] = vc.latestVideos

        # Add extra variables and return the updated context
        return context


class LessonsPage(ContextPage):
    body = StreamField(
            [('vimeo_block', SectionedVimeoBlock()),
             ('collection_block', CollectionChooserBlock()),
             ('link_block', LinkBlock()),
             ], blank=True)
    parent_page_types = [LatestLessonsPage]
    content_panels = ContextPage.content_panels + [StreamFieldPanel('body')]


class Series(models.Model):
    collection = models.ForeignKey(
                'wagtailcore.collection',
                null=True, blank=True,
                on_delete=models.SET_NULL)
    title = models.CharField(max_length=250)
    start_date = models.DateField(default=timezone.now)
    stop_date = models.DateField(null=True, blank=True)
    description = RichTextField(blank=True)

    panels = [
        FieldPanel('collection'),
        FieldPanel('title'),
        FieldPanel('start_date'),
        FieldPanel('stop_date'),
        FieldPanel('description'),
    ]


class SubSeries(models.Model):
    series = models.ForeignKey(
                'Series',
                null=True, blank=True,
                on_delete=models.SET_NULL)
    title = models.CharField(max_length=250)
    start_date = models.DateField(default=timezone.now)
    stop_date = models.DateField(null=True, blank=True)
    description = RichTextField(blank=True)
    panels = [
        FieldPanel('series'),
        FieldPanel('title'),
        FieldPanel('start_date'),
        FieldPanel('stop_date'),
        FieldPanel('description'),
    ]


class PleroMedia(AbstractMedia):
    duration = models.PositiveIntegerField(null=True,
                                           blank=True,
                                           verbose_name='duration',
                                           help_text='Duration in seconds')
    series = models.ForeignKey(
        'Series', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+')

    subseries = models.ForeignKey(
        'SubSeries', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+')

    def process(self, name):
        return os.path.join(self.series.collection.name, self.series, name)
    file = models.FileField(upload_to=process, verbose_name='file')

    admin_form_fields = (
        'title',
        'file',
        'series',
        'tags',)

    def clean(self):
        cleaned_data = super().clean()
        # Make sure that the event starts before it ends
        # start_date = cleaned_data['start_date']
        # end_date = cleaned_data['end_date']
        # if start_date and end_date and start_date > end_date:
        # self.add_error('end_date', 'The end date must be after start # date')
        return cleaned_data

    def save(self, *args, **kwargs):
        # Update the duration field
        # import cv2
        # import pdb; pdb.set_trace()
        # cap = cv2.VideoCapture(self.file)
        # self.count = cap.get(cv2.CV_CAP_PROP_FRAME_COUNT)
        # self.fps = cap.get(cv2.CV_CAP_PROP_FPS)
        # self.duration = self.count/self.fps
        # self.width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        # self.height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # cap.release()

        return super().save(*args, **kwargs)


class LessonBlock(AbstractMediaChooserBlock):
    heading = core_blocks.CharBlock(classname="full title", icon='title')
    speaker = core_blocks.CharBlock(max_length=255)
    date = core_blocks.DateTimeBlock("Post date")
    paragraph = common_blocks.SimpleRichTextBlock(icon='pilcrow')

    def render_basic(self, value, context=None):
        if not value:
            return ''

        if value.type == 'video':
            player_code = '''
            <div>
                <video width="640" height="480" controls>
                    <source src="{0}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
            '''
        else:
            player_code = '''
            <div>
                <audio controls>
                    <source src="{0}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            </div>
            '''

        return format_html(player_code, value.file.url)

    class Meta:
        icon = 'view'
