# Generated by Django 4.1.1 on 2022-09-27 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AbhaDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('health_id', models.CharField(blank=True, max_length=200, null=True, verbose_name='Health Id')),
                ('token', models.CharField(blank=True, max_length=200, null=True, verbose_name='Token')),
            ],
        ),
    ]