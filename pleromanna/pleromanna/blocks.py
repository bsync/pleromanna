from wagtail.core import blocks as core_blocks
from wagtail.images import blocks as image_blocks
from commonblocks import blocks as common_blocks


class PersonBlock(core_blocks.StructBlock):
    first_name = core_blocks.CharBlock()
    middle_name = core_blocks.CharBlock()
    last_name = core_blocks.CharBlock()
    photo = image_blocks.ImageChooserBlock()
    biography = common_blocks.SimpleRichTextBlock()

    class Meta:
        icon = 'user'
        template = 'blocks/person_block.html'


class EventBlock(core_blocks.StructBlock):
    heading = core_blocks.CharBlock()
    start_date = core_blocks.DateTimeBlock()
    stop_date = core_blocks.DateTimeBlock()
    photo = image_blocks.ImageChooserBlock(required=False)
    description = common_blocks.SimpleRichTextBlock(required=False)

    class Meta:
        icon = 'date'
        template = 'blocks/event_block.html'

