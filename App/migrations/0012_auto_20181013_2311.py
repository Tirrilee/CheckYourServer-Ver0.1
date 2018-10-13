# Generated by Django 2.1.2 on 2018-10-13 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0011_auto_20181012_0418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('ready', '미결제'), ('paid', '결제완료'), ('cancelled', '결제취소'), ('failed', '결제실패'), ('reservation', '결제예약')], default='ready', max_length=9, verbose_name='상태'),
        ),
    ]
