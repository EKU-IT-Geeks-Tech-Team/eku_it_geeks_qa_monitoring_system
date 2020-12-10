# Generated by Django 3.1.4 on 2020-12-09 21:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0003_auto_20201209_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='error',
            name='committed_date',
            field=models.DateField(null=True, verbose_name='Committed Date'),
        ),
        migrations.AlterField(
            model_name='error',
            name='footprints_number',
            field=models.CharField(max_length=10, null=True, verbose_name='FP#'),
        ),
        migrations.AlterField(
            model_name='error',
            name='found_date',
            field=models.DateField(auto_now=True, default=datetime.datetime(2020, 12, 9, 16, 34, 2, 351427), verbose_name='Found Date'),
            preserve_default=False,
        ),
    ]