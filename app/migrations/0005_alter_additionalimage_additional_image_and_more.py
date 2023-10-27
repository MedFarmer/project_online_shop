# Generated by Django 4.2.5 on 2023-10-22 18:02

import app.models
from django.db import migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_additionalimage_additional_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalimage',
            name='additional_image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=app.models.image_path_for_add_images),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=app.models.image_path),
        ),
    ]