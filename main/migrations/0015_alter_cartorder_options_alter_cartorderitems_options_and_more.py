# Generated by Django 4.0.2 on 2022-03-17 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_cartorder_cartorderitems'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartorder',
            options={'verbose_name_plural': '8. Orders'},
        ),
        migrations.AlterModelOptions(
            name='cartorderitems',
            options={'verbose_name_plural': '9. Order Items'},
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='total',
            field=models.IntegerField(),
        ),
    ]
