# Generated by Django 2.0.3 on 2018-11-15 03:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserCenterTitle',
            new_name='UserCenter',
        ),
        migrations.RenameField(
            model_name='file',
            old_name='userId',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='usercenter',
            old_name='isSuper',
            new_name='is_super',
        ),
        migrations.AlterField(
            model_name='blog',
            name='update',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 15, 3, 41, 20, 263795, tzinfo=utc), verbose_name='更新时间'),
        ),
    ]