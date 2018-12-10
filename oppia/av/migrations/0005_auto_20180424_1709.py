# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-24 17:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import oppia.av.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('av', '0004_auto_20171203_1308'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedMediaImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date created')),
                ('image', models.ImageField(upload_to=oppia.av.models.image_file_name)),
                ('default_image', models.BooleanField(default=False)),
                ('create_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media_image_create_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Uploaded Media Image',
                'verbose_name_plural': 'Uploaded Media Images',
            },
        ),
        migrations.AlterModelOptions(
            name='uploadedmedia',
            options={'verbose_name': 'Uploaded Media', 'verbose_name_plural': 'uUploaded Media'},
        ),
        migrations.AddField(
            model_name='uploadedmediaimage',
            name='uploaded_media',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='av.UploadedMedia'),
        ),
    ]