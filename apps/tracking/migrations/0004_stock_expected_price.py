# Generated by Django 5.1 on 2024-08-31 21:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracking", "0003_alter_pricehistory_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="stock",
            name="expected_price",
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
