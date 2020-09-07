# Generated by Django 3.0.8 on 2020-07-27 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interactionstatistic',
            name='mechanic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='api.GMechanic'),
        ),
        migrations.AlterField(
            model_name='interactionstatistic',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Gamer'),
        ),
    ]