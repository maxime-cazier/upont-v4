# Generated by Django 3.2.12 on 2023-09-13 15:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("social", "0010_merge_20230909_1459"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="birthdate",
            field=models.DateField(blank=True, max_length=12, null=True),
        ),
    ]
