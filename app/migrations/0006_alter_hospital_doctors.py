# Generated by Django 4.2.7 on 2023-12-21 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_doctor_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='doctors',
            field=models.ManyToManyField(related_name='hospitals', to='app.doctor'),
        ),
    ]
