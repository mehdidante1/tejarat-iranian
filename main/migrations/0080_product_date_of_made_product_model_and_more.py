# Generated by Django 4.0.2 on 2022-08-31 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0079_alter_commentblog_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='date_of_made',
            field=models.CharField(max_length=100, null=True, verbose_name='تاریخ ساخت'),
        ),
        migrations.AddField(
            model_name='product',
            name='model',
            field=models.CharField(max_length=100, null=True, verbose_name='مدل محصول'),
        ),
        migrations.AddField(
            model_name='product',
            name='name_of_country',
            field=models.CharField(max_length=200, null=True, verbose_name='کشور سازنده'),
        ),
    ]
