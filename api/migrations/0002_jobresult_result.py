# Generated by Django 2.0.6 on 2018-10-24 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobresult',
            name='result',
            field=models.CharField(default='SUCCESS', max_length=100),
            preserve_default=False,
        ),
    ]
