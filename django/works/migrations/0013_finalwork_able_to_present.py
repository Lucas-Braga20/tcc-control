# Generated by Django 4.2 on 2023-09-10 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0012_finalwork_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='finalwork',
            name='able_to_present',
            field=models.BooleanField(default=False, verbose_name='able to present'),
        ),
    ]