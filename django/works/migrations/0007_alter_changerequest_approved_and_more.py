# Generated by Django 4.2 on 2023-07-25 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0006_finalwork_archived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changerequest',
            name='approved',
            field=models.BooleanField(blank=True, default=None, null=True, verbose_name='approved'),
        ),
        migrations.AlterField(
            model_name='finalworkstage',
            name='status',
            field=models.IntegerField(choices=[(0, 'assigned'), (1, 'pending'), (2, 'correction'), (3, 'adjusted'), (4, 'completed late'), (5, 'completed'), (6, 'presented'), (7, 'under change')], default=0, verbose_name='status'),
        ),
    ]
