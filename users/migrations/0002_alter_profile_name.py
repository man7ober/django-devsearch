# Generated by Django 5.0.7 on 2024-09-12 06:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="name",
            field=models.CharField(
                blank=True, default="unknown", max_length=100, null=True
            ),
        ),
    ]
