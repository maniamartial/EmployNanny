# Generated by Django 4.0.5 on 2023-06-29 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_nannydetails_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employerprofile',
            name='id_number',
            field=models.IntegerField(default=None),
        ),
    ]
