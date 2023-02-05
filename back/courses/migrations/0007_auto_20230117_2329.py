# Generated by Django 3.2.12 on 2023-01-17 22:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0006_group_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="groups",
                to="courses.course",
            ),
        ),
        migrations.AlterField(
            model_name="group",
            name="teacher",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="groups",
                to="courses.teacher",
            ),
        ),
    ]
