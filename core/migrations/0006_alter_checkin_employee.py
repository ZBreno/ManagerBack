# Generated by Django 4.2.1 on 2023-06-02 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_employee_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='employee',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.employee'),
        ),
    ]