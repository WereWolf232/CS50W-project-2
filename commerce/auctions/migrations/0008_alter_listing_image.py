# Generated by Django 4.1.4 on 2023-06-16 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0007_alter_listing_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="image",
            field=models.URLField(blank=True, null=True),
        ),
    ]