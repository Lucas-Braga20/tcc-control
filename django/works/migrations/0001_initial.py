# Generated by Django 4.2 on 2023-06-10 20:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('timetables', '0005_alter_step_presentation_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TCCWork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.TextField(verbose_name='description')),
                ('approved', models.BooleanField(default=False, verbose_name='approved')),
                ('advised', models.ManyToManyField(related_name='advised', to=settings.AUTH_USER_MODEL, verbose_name='advised')),
                ('advisor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='advisor', to=settings.AUTH_USER_MODEL, verbose_name='advisor')),
            ],
        ),
        migrations.CreateModel(
            name='WorkStep',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('presented', models.BooleanField(default=False, verbose_name='presented')),
                ('status', models.SmallIntegerField(choices=[(0, 'assigned'), (1, 'pending'), (2, 'correction'), (3, 'adjusted'), (4, 'completed late'), (5, 'completed')], default=0, verbose_name='status')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='step', to='timetables.step', verbose_name='step')),
                ('tcc_work', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tcc_work', to='works.tccwork', verbose_name='tcc work')),
            ],
        ),
        migrations.CreateModel(
            name='WorkStepVersion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('content', models.JSONField(verbose_name='content')),
                ('work_step', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='work_step', to='works.workstep', verbose_name='work step')),
            ],
        ),
        migrations.CreateModel(
            name='ChangeRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('approved', models.BooleanField(default=False, verbose_name='approved')),
                ('description', models.TextField(verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='requested', to=settings.AUTH_USER_MODEL, verbose_name='requester')),
            ],
        ),
    ]
