# Generated by Django 4.0.2 on 2022-02-03 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_featured',
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.color'),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default=None, upload_to='product_imgs/'),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(default=None),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.size'),
        ),
    ]
