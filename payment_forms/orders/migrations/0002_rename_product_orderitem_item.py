# Generated by Django 3.2.9 on 2022-11-21 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="orderitem",
            old_name="product",
            new_name="item",
        ),
    ]