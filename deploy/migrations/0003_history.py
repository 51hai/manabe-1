# Generated by Django 3.0.3 on 2020-02-18 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('envx', '0002_auto_20200217_2137'),
        ('appinput', '0002_auto_20200217_1802'),
        ('deploy', '0002_auto_20200218_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='名称')),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='描述')),
                ('change_date', models.DateTimeField(auto_now=True)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('do_type', models.CharField(blank=True, max_length=32, null=True, verbose_name='操作类型')),
                ('content', models.CharField(blank=True, max_length=1024, null=True, verbose_name='操作内容')),
                ('app_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_app', to='appinput.App', verbose_name='APP应用')),
                ('deploy_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_deploy', to='deploy.DeployPool', verbose_name='发布单')),
                ('env_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_env', to='envx.Env', verbose_name='环境')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_user', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'db_table': 'history',
            },
        ),
    ]
