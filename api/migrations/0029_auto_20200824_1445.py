# Generated by Django 3.0.8 on 2020-08-24 14:45

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_socialprofile_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialprofile',
            name='friends',
            field=jsonfield.fields.JSONField(default=[]),
        ),
    ]