# Generated by Django 4.0.2 on 2022-04-06 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='amount',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]