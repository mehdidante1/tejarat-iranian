# Generated by Django 4.0.2 on 2022-04-20 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0054_remove_useraddressbook_phone_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddressbook',
            name='phone_2',
            field=models.IntegerField(blank=True, max_length=100, null=True),
        ),
    ]