# Generated by Django 5.1.2 on 2024-10-26 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('immapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('channels', models.ManyToManyField(related_name='groups', to='immapi.channel')),
            ],
        ),
    ]
