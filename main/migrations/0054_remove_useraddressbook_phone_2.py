# Generated by Django 4.0.2 on 2022-04-20 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0053_alter_useraddressbook_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraddressbook',
            name='phone_2',
        ),
    ]
