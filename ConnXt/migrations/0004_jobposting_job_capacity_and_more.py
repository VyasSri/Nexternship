# Generated by Django 5.1.1 on 2024-09-20 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ConnXt', '0003_jobposting_job_location_alter_jobposting_job_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobposting',
            name='job_capacity',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jobposting',
            name='job_location',
            field=models.CharField(default='', max_length=100),
        ),
    ]
