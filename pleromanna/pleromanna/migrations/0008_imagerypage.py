# Generated by Django 2.1.4 on 2018-12-16 02:44

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('pleromanna', '0007_auto_20181216_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageryPage',
            fields=[
                ('contextpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pleromanna.ContextPage')),
                ('imagery', wagtail.core.fields.StreamField([('section', wagtail.core.blocks.CharBlock()), ('images', wagtail.core.blocks.ListBlock(wagtail.images.blocks.ImageChooserBlock()))])),
            ],
            options={
                'abstract': False,
            },
            bases=('pleromanna.contextpage',),
        ),
    ]
