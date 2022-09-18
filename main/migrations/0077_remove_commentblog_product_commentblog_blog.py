# Generated by Django 4.0.2 on 2022-06-16 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0076_commentblog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentblog',
            name='product',
        ),
        migrations.AddField(
            model_name='commentblog',
            name='blog',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, to='main.blog'),
            preserve_default=False,
        ),
    ]