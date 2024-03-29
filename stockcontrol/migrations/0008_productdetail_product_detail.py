# Generated by Django 5.0.2 on 2024-02-28 15:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockcontrol', '0007_tagproduct_alter_product_category_product_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detailed_description', models.TextField()),
                ('warranty_information', models.TextField(blank=True, null=True)),
                ('usage_instructions', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='detail',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='stockcontrol.productdetail'),
        ),
    ]
