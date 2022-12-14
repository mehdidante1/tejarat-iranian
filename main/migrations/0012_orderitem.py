# Generated by Django 4.0.2 on 2022-03-15 23:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(verbose_name='قیمت')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='تعداد')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='main.order', verbose_name='سفارش')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='main.product', verbose_name='محصول')),
            ],
        ),
    ]
