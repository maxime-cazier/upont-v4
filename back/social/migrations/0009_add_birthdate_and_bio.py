# Generated by Django 3.2.12 on 2023-05-30 11:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("social", "0007_merge_0004_auto_20220826_1123_0006_alter_role_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="birthdate",
            field=models.DateField(
                blank=True,
                max_length=12,
                null=True,
                verbose_name="Date de naissance au format JJ/MM/AAAA",
            ),
        ),
        migrations.AddField(
            model_name="student",
            name="biography",
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
    ]
