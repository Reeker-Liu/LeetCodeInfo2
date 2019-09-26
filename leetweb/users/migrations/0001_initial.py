# Generated by Django 2.1.8 on 2019-09-26 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('name', models.CharField(max_length=30)),
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=30)),
                ('version', models.IntegerField()),
                ('yesterday', models.IntegerField()),
                ('today', models.IntegerField()),
                ('latest', models.IntegerField()),
            ],
        ),
    ]
