# Generated by Django 4.0.2 on 2022-06-04 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0071_delete_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('family', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('text_comment', models.TextField(verbose_name='متن دیدگاه')),
                ('status', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
            ],
            options={
                'verbose_name': 'پرسش و پاسخ کاربر',
                'verbose_name_plural': 'پرسش و پاسخ کاربران',
            },
        ),
    ]
