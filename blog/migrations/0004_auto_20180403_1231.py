# Generated by Django 2.0.3 on 2018-04-03 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180403_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='lookNumber',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]