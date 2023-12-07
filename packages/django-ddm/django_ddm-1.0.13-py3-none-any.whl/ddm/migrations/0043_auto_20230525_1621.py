# Generated by Django 3.2.13 on 2023-05-25 14:21

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddm', '0042_auto_20230429_2215'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='questionbase',
            options={'ordering': ['page', 'index']},
        ),
        migrations.AlterField(
            model_name='donationproject',
            name='redirect_target',
            field=models.CharField(blank=True, help_text='Always include <i>http://</i> or <i>https://</i> in the redirect target. If URL parameter extraction is enabled for this project, you can include the extracted URL parameters in the redirect target as follows: "https://redirect.me/?redirectpara=<b>{{participant.data.url_param.URLParameter}}</b>".', max_length=2000, verbose_name='Redirect target'),
        ),
        migrations.AlterField(
            model_name='questionbase',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='If a question is linked to a File Blueprint, data points from the donated data associated with the linked donation blueprint can be included in the question text. This data can be included as "{{ data }}" in the question text. It is possible to subset the data object (e.g., to include the last datapoint you can use {{ data.0 }} or include advanced rendering options included in the Django templating engine. For a more comprehensive overview and examples see the documentation. Additionally, information directly related to the participant can be included in the question text. This information can be referenced as "{{ participant }}".', null=True),
        ),
    ]
