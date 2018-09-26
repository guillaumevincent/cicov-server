# Generated by Django 2.0.6 on 2018-09-26 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cicovapp', '0004_auto_20180723_1234'),
    ]

    operations = [
        migrations.CreateModel(
            name='RFEResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.BooleanField()),
                ('percent', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cicovapp.JobResult')),
                ('rfe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cicovapp.RFE')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
