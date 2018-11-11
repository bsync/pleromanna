# Generated by Django 2.1.2 on 2018-11-01 01:42

import commonblocks.blocks
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20181030_0356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pleromapage',
            name='body',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('subheading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('banner', wagtail.images.blocks.ImageChooserBlock()), ('event', wagtail.core.blocks.StructBlock([('start_date', wagtail.core.blocks.DateTimeBlock()), ('stop_date', wagtail.core.blocks.DateTimeBlock()), ('photo', wagtail.images.blocks.ImageChooserBlock()), ('description', commonblocks.blocks.SimpleRichTextBlock())])), ('person', wagtail.core.blocks.StructBlock([('first_name', wagtail.core.blocks.CharBlock()), ('last_name', wagtail.core.blocks.CharBlock()), ('photo', wagtail.images.blocks.ImageChooserBlock()), ('biography', commonblocks.blocks.SimpleRichTextBlock())])), ('html', wagtail.core.blocks.RawHTMLBlock())]),
        ),
    ]
