# Generated by Django 5.0.7 on 2024-07-31 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0006_rename_vendas_sales_rename_valor_sales_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='qty',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
