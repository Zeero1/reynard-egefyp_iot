# Generated by Django 5.0 on 2024-02-07 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devicewebapp', '0003_auto_20220105_1017'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostnm', models.CharField(max_length=100)),
                ('ipaddr', models.CharField(max_length=30)),
                ('macaddr', models.CharField(max_length=30)),
                ('signalstr', models.CharField(max_length=10)),
            ],
        ),
    ]
