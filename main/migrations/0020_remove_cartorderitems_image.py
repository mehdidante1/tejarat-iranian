# Generated by Django 4.0.2 on 2022-03-20 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_cartorderitems_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartorderitems',
            name='image',
        ),
    ]
