# Generated by Django 4.2.5 on 2023-10-24 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_additionalimage_additional_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='subtotal',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
