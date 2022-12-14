# Generated by Django 4.0.2 on 2022-03-18 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0017_remove_cartorderitems_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartorderitems',
            options={'verbose_name_plural': 'موارد سفارش شده'},
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='paid_status',
            field=models.BooleanField(default=False, verbose_name='وضعیت پرداخت'),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='total_amt',
            field=models.IntegerField(verbose_name='جمع کل'),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نام کاربر'),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='invoice_no',
            field=models.CharField(max_length=150, verbose_name='شماره فاکتور'),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='item',
            field=models.CharField(max_length=150, verbose_name='تام محصول'),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='price',
            field=models.IntegerField(verbose_name='قیمت'),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='qty',
            field=models.IntegerField(verbose_name='تعداد'),
        ),
        migrations.AlterField(
            model_name='cartorderitems',
            name='total',
            field=models.IntegerField(verbose_name='قیمت آخر'),
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.TextField()),
                ('review_rating', models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], max_length=150)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
