# Generated by Django 2.2.10 on 2021-11-17 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_question_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poll',
            options={'ordering': ('title', 'id')},
        ),
        migrations.RemoveField(
            model_name='question',
            name='order',
        ),
    ]
