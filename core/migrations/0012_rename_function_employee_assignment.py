# Generated by Django 4.2.1 on 2023-07-08 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_message_attachment_alter_message_department_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='function',
            new_name='assignment',
        ),
    ]