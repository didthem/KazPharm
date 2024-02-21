# Generated by Django 4.2.7 on 2023-12-21 04:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_hospital_doctors_doctor_hospitals'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='hospitals',
        ),
        migrations.AddField(
            model_name='doctor',
            name='hospitals',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='app.hospital'),
        ),
    ]
