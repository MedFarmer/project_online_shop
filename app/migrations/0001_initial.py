# Generated by Django 4.2.5 on 2023-10-19 10:47

import app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to=app.models.image_path)),
                ('description', models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Textile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('textile', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField()),
                ('size', models.CharField(max_length=30)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='app.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks_product', to='app.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='textile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='app.textile'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order_quantity', models.IntegerField()),
                ('color', models.CharField(max_length=30)),
                ('size', models.CharField(max_length=30)),
                ('clients', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('products', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.product')),
            ],
        ),
        migrations.CreateModel(
            name='AdditionalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_image', models.ImageField(upload_to=app.models.image_path)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_images', to='app.product')),
            ],
        ),
    ]