# Generated by Django 2.1.2 on 2018-10-05 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App', '0004_auto_20181005_2209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='사이트명')),
                ('url', models.CharField(max_length=255, verbose_name='사이트URL')),
                ('merchant_uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('imp_uid', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(choices=[('ready', '미결제'), ('paid', '결제완료'), ('cancelled', '결제취소'), ('failed', '결제실패')], default='ready', max_length=9, verbose_name='상태')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='주문일자')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일자')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='유저')),
            ],
        ),
    ]