# Generated by Django 2.2.1 on 2019-06-02 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pleromanna', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pleromahomepage',
            name='verse',
            field=models.TextField(default='For of His fullness we have all receieved, and grace upon grace. -John 1:16'),
        ),
    ]