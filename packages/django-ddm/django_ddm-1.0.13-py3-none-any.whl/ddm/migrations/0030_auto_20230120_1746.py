# Generated by Django 3.2.13 on 2023-01-20 16:46

import ddm.models.core
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddm', '0029_rename_eventlog_eventlogentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationproject',
            name='img_header_left',
            field=models.ImageField(blank=True, null=True, upload_to=ddm.models.core.project_header_dir_path),
        ),
        migrations.AddField(
            model_name='donationproject',
            name='img_header_right',
            field=models.ImageField(blank=True, null=True, upload_to=ddm.models.core.project_header_dir_path),
        ),
    ]
