# Generated by Django 4.2 on 2023-06-13 02:09

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(verbose_name='description')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
        migrations.CreateModel(
            name='Receiver',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('visualized', models.BooleanField(default=False, verbose_name='visualized')),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='notifications.notification', verbose_name='notification')),
            ],
            options={
                'verbose_name': 'Receiver',
                'verbose_name_plural': 'Receivers',
            },
        ),
    ]
