# Generated by Django 2.0.9 on 2018-10-16 03:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20181016_0338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pleropage',
            name='head',
        ),
    ]
