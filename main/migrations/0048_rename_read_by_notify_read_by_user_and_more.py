# Generated by Django 4.0.2 on 2022-04-14 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0047_alter_productattribute_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notify',
            old_name='read_by',
            new_name='read_by_user',
        ),
        migrations.RemoveField(
            model_name='notify',
            name='status',
        ),
    ]
