# Generated by Django 4.0.2 on 2022-04-14 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0046_notify'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattribute',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
