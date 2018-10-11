# Generated by Django 2.1.2 on 2018-10-11 19:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('App', '0010_checklog'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_uid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('imp_uid', models.CharField(blank=True, max_length=100)),
                ('status', models.CharField(choices=[('ready', '미결제'), ('paid', '결제완료'), ('cancelled', '결제취소'), ('failed', '결제실패')], default='ready', max_length=9, verbose_name='상태')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='주문일자')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일자')),
            ],
        ),
        migrations.RemoveField(
            model_name='site',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='site',
            name='imp_uid',
        ),
        migrations.RemoveField(
            model_name='site',
            name='merchant_uid',
        ),
        migrations.RemoveField(
            model_name='site',
            name='status',
        ),
        migrations.RemoveField(
            model_name='site',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='order',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.Site', verbose_name='사이트'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='유저'),
        ),
    ]
