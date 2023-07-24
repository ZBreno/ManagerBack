# Generated by Django 4.2.1 on 2023-07-15 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_department_user_alter_employee_head_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='core.department'),
        ),
    ]