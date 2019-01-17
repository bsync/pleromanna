# Generated by Django 2.1.4 on 2019-01-13 02:50

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.core.models
import wagtail.documents.blocks
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('pleromanna', '0021_auto_20190113_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docspage',
            name='body',
            field=wagtail.core.fields.StreamField([('doc_chooser', wagtail.core.blocks.StructBlock([('section', wagtail.core.blocks.CharBlock(required=False)), ('doc_list', wagtail.core.blocks.ListBlock(wagtail.documents.blocks.DocumentChooserBlock(required=False)))]))], blank=True),
        ),
        migrations.AlterField(
            model_name='imagerypage',
            name='body',
            field=wagtail.core.fields.StreamField([('image_chooser', wagtail.core.blocks.StructBlock([('section', wagtail.core.blocks.CharBlock(required=False)), ('image_list', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock(required=False)))])), ('collection_chooser', wagtail.core.blocks.StructBlock([('section', wagtail.core.blocks.CharBlock(required=False)), ('collection', wagtail.snippets.blocks.SnippetChooserBlock(wagtail.core.models.Collection))]))], blank=True),
        ),
    ]