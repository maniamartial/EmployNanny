# Generated by Django 4.0.5 on 2023-06-13 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_nannydetails_nationality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nannydetails',
            name='language',
            field=models.CharField(max_length=200),
        ),
    ]
