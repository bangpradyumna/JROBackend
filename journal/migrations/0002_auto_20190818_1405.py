# Generated by Django 2.2.4 on 2019-08-18 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadedresearchobject',
            old_name='file',
            new_name='uploadedfile',
        ),
    ]
