# Generated by Django 4.1.7 on 2023-03-14 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_address_line_2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]