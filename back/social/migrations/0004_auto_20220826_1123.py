# Generated by Django 3.2.12 on 2022-08-26 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social", "0003_clubrequest"),
    ]

    operations = [
        migrations.AlterField(
            model_name="club",
            name="background_picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="background_pictures/"
            ),
        ),
        migrations.AlterField(
            model_name="club",
            name="logo",
            field=models.ImageField(blank=True, null=True, upload_to="logos/"),
        ),
        migrations.AlterField(
            model_name="student",
            name="picture",
            field=models.ImageField(blank=True, null=True, upload_to="pictures/"),
        ),
    ]
