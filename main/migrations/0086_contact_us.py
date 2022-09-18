# Generated by Django 4.0.2 on 2022-09-17 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0085_alter_category_options_remove_category_level_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact_Us',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField(max_length='20')),
                ('text_message', models.TextField()),
            ],
            options={
                'verbose_name': 'تماس با ما',
                'verbose_name_plural': 'تماس با ما',
            },
        ),
    ]
