# Generated by Django 4.0.2 on 2022-04-04 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0038_useraddressbook_phone_2_useraddressbook_postal_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone_2',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.IntegerField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='tag',
            field=models.IntegerField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='vahed',
            field=models.IntegerField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.productattribute'),
        ),
        migrations.AlterField(
            model_name='useraddressbook',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/users/'),
        ),
    ]
