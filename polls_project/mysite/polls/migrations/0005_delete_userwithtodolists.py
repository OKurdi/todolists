# Generated by Django 3.0.3 on 2020-03-03 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_todolist_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserWithTodoLists',
        ),
    ]
