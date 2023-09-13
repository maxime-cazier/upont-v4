# Generated by Django 3.2.12 on 2023-09-13 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0011_alter_student_birthdate'),
        ('news', '0005_auto_20230117_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='bookmark',
            field=models.ManyToManyField(blank=True, editable=False, related_name='posts_bookmark', to='social.Student'),
        ),
    ]
