# Generated by Django 4.2 on 2023-06-10 20:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0002_workstep'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkStepVersion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('content', models.JSONField(verbose_name='content')),
            ],
        ),
    ]
