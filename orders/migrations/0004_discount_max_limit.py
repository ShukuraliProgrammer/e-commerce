# Generated by Django 5.0.6 on 2024-07-09 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_payment_method_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='max_limit',
            field=models.IntegerField(default=1, verbose_name='Max Limit'),
            preserve_default=False,
        ),
    ]