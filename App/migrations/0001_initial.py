# Generated by Django 2.1.2 on 2018-10-05 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='국가명')),
                ('flag', models.CharField(max_length=255, verbose_name='국기')),
                ('callcode', models.CharField(max_length=8, verbose_name='국가번호')),
            ],
        ),
    ]
