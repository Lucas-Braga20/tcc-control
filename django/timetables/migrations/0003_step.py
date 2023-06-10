# Generated by Django 4.2 on 2023-06-10 18:55

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_activityconfiguration_template_abnt'),
        ('timetables', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(verbose_name='description')),
                ('start_date', models.DateField(verbose_name='start date')),
                ('send_date_advisor', models.DateField(verbose_name='send date advisor')),
                ('send_date', models.DateField(verbose_name='send date')),
                ('presentation_date', models.DateField(verbose_name='presentation date')),
                ('activity_configuration', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='activity_configuration', to='activities.activityconfiguration', verbose_name='activity configuration')),
            ],
        ),
    ]
