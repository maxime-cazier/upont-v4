# Generated by Django 3.2.12 on 2022-12-12 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Update",
            new_name="CourseUpdate",
        ),
        migrations.RenameField(
            model_name="course",
            old_name="head",
            new_name="teacher",
        ),
        migrations.RenameField(
            model_name="enrolment",
            old_name="course",
            new_name="group",
        ),
    ]
