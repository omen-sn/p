# Generated by Django 5.0.2 on 2024-02-28 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockcontrol', '0002_alter_product_options_alter_product_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_published',
            field=models.BooleanField(choices=[(0, 'Draft'), (1, 'Published')], default=1),
        ),
    ]