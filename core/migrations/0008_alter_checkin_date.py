# Generated by Django 4.2.1 on 2023-06-02 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_checkin_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
