# Generated by Django 2.1.4 on 2018-12-10 01:49

import commonblocks.blocks
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('pleromanna', '0003_auto_20181210_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pleromapage',
            name='body',
            field=wagtail.core.fields.StreamField([('section', wagtail.core.blocks.CharBlock()), ('person', wagtail.core.blocks.StructBlock([('first_name', wagtail.core.blocks.CharBlock()), ('middle_name', wagtail.core.blocks.CharBlock(required=False)), ('last_name', wagtail.core.blocks.CharBlock()), ('titles', wagtail.core.blocks.CharBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock()), ('biography', commonblocks.blocks.SimpleRichTextBlock())])), ('people', wagtail.core.blocks.StructBlock([('people', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('first_name', wagtail.core.blocks.CharBlock()), ('middle_name', wagtail.core.blocks.CharBlock(required=False)), ('last_name', wagtail.core.blocks.CharBlock()), ('titles', wagtail.core.blocks.CharBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock()), ('biography', commonblocks.blocks.SimpleRichTextBlock())], required=False))), ('group_photo', wagtail.images.blocks.ImageChooserBlock()), ('group_bio', commonblocks.blocks.SimpleRichTextBlock())])), ('event', wagtail.core.blocks.StructBlock([('start_date', wagtail.core.blocks.DateTimeBlock()), ('stop_date', wagtail.core.blocks.DateTimeBlock()), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False)), ('description', commonblocks.blocks.SimpleRichTextBlock(required=False))])), ('article', wagtail.core.blocks.StructBlock([('subject', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('paragraph', commonblocks.blocks.SimpleRichTextBlock())]))]),
        ),
    ]