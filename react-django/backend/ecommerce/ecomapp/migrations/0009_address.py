# Generated by Django 5.0.7 on 2024-08-16 14:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0008_remove_products_qty'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=50)),
                ('postal_code', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
