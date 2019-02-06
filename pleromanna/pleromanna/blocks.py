import wagtail.core.models
from wagtail.snippets.models import register_snippet
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.core import blocks as core_blocks
from wagtail.images import blocks as image_blocks
from commonblocks import blocks as common_blocks
from wagtail.documents.blocks import DocumentChooserBlock


class SectionBlock(core_blocks.StructBlock):
    section = core_blocks.CharBlock(required=False)

    class Meta:
        icon = 'doc'
        template = 'blocks/section_block.html'


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
    register_snippet(wagtail.core.models.Collection)
    collection = SnippetChooserBlock(wagtail.core.models.Collection)

    class Meta:
        icon = 'snippet'
        template = 'blocks/image_chooser_block.html'

class LinkBlock(SectionBlock):
    link = core_blocks.URLBlock()
    paragraph = common_blocks.SimpleRichTextBlock(required=False)

    class Meta:
        icon = 'anchor'
        template = 'blocks/link_block.html'
