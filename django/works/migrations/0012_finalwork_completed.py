# Generated by Django 4.2 on 2023-09-10 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0011_finalworkversion_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='finalwork',
            name='completed',
            field=models.BooleanField(default=False, verbose_name='completed'),
        ),
    ]
