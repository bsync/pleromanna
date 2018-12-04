# Generated by Django 2.1.3 on 2018-12-03 01:53

import commonblocks.blocks
from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailimages', '0021_image_file_hash'),
        ('wagtailcore', '0040_page_draft_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContextPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='EventPage',
            fields=[
                ('contextpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pleromanna.ContextPage')),
                ('year', models.PositiveSmallIntegerField()),
                ('body', wagtail.core.fields.StreamField([('section', wagtail.core.blocks.CharBlock()), ('event', wagtail.core.blocks.StructBlock([('start_date', wagtail.core.blocks.DateTimeBlock()), ('stop_date', wagtail.core.blocks.DateTimeBlock()), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False)), ('description', commonblocks.blocks.SimpleRichTextBlock(required=False))]))], blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('pleromanna.contextpage',),
        ),
        migrations.CreateModel(
            name='PleromaHomePage',
            fields=[
                ('contextpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pleromanna.ContextPage')),
                ('heading', models.CharField(max_length=250)),
                ('subheading', models.CharField(blank=True, max_length=250)),
                ('paragraph', wagtail.core.fields.RichTextField()),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('pleromanna.contextpage',),
        ),
        migrations.CreateModel(
            name='PleromaPage',
            fields=[
                ('contextpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pleromanna.ContextPage')),
                ('body', wagtail.core.fields.StreamField([('section', wagtail.core.blocks.CharBlock()), ('person', wagtail.core.blocks.StructBlock([('first_name', wagtail.core.blocks.CharBlock()), ('middle_name', wagtail.core.blocks.CharBlock(required=False)), ('last_name', wagtail.core.blocks.CharBlock()), ('titles', wagtail.core.blocks.CharBlock(required=False)), ('photo', wagtail.images.blocks.ImageChooserBlock()), ('biography', commonblocks.blocks.SimpleRichTextBlock())])), ('event', wagtail.core.blocks.StructBlock([('start_date', wagtail.core.blocks.DateTimeBlock()), ('stop_date', wagtail.core.blocks.DateTimeBlock()), ('photo', wagtail.images.blocks.ImageChooserBlock(required=False)), ('description', commonblocks.blocks.SimpleRichTextBlock(required=False))])), ('article', wagtail.core.blocks.StructBlock([('subject', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('paragraph', commonblocks.blocks.SimpleRichTextBlock())]))])),
            ],
            options={
                'abstract': False,
            },
            bases=('pleromanna.contextpage',),
        ),
    ]