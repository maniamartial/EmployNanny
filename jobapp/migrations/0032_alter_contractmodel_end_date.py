# Generated by Django 4.0.5 on 2023-07-12 20:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0031_directcontract_nanny_signature_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractmodel',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2023, 8, 11, 20, 23, 2, 690366, tzinfo=utc)),
        ),
    ]
