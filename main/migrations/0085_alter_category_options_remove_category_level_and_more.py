# Generated by Django 4.0.2 on 2022-09-03 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0084_category_product_parent_category_product_position_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['parent__id'], 'verbose_name': 'دسته بندی', 'verbose_name_plural': 'دسته بندی ها'},
        ),
        migrations.RemoveField(
            model_name='category',
            name='level',
        ),
        migrations.RemoveField(
            model_name='category',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='category',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='category',
            name='tree_id',
        ),
        migrations.AddField(
            model_name='category',
            name='position',
            field=models.IntegerField(blank=True, null=True, verbose_name='پوزیشن'),
        ),
        migrations.AddField(
            model_name='category',
            name='status',
            field=models.BooleanField(blank=True, null=True, verbose_name='آیا نمایش داده شود؟'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='main.category', verbose_name='زیر دست'),
        ),
        migrations.DeleteModel(
            name='Category_Product',
        ),
    ]
