# Generated by Django 4.2.6 on 2023-10-26 11:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0036_alter_contractmodel_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractmodel',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2023, 11, 25, 11, 4, 59, 822784, tzinfo=datetime.timezone.utc)),
        ),
    ]
