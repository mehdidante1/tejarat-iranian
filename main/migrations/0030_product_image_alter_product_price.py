# Generated by Django 4.0.2 on 2022-04-01 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='product_imgs/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]