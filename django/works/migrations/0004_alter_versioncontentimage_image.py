# Generated by Django 4.2 on 2023-06-23 01:52

from django.db import migrations, models
import works.utils


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0003_versioncontentimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='versioncontentimage',
            name='image',
            field=models.ImageField(max_length=255, upload_to=works.utils.get_version_content_image_folder, verbose_name='image'),
        ),
    ]
