# Generated by Django 5.1.2 on 2024-10-25 10:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('metadata', models.JSONField()),
                ('rating', models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('media', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('language', models.CharField(max_length=255)),
                ('cover', models.ImageField(upload_to='')),
                ('sub_channels', models.ManyToManyField(blank=True, related_name='parents', to='immapi.channel')),
                ('contents', models.ManyToManyField(blank=True, related_name='parent_channels', to='immapi.content')),
            ],
        ),
    ]
