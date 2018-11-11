# Generated by Django 2.1.2 on 2018-11-06 02:02

import commonblocks.blocks
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_auto_20181104_0100'),
    ]

    operations = [
        migrations.AddField(
            model_name='pleromahomepage',
            name='events',
            field=wagtail.core.fields.StreamField([('start_date', wagtail.core.blocks.DateTimeBlock()), ('stop_date', wagtail.core.blocks.DateTimeBlock()), ('photo', wagtail.images.blocks.ImageChooserBlock()), ('description', commonblocks.blocks.SimpleRichTextBlock())], null=True),
        ),
    ]