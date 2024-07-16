# Generated by Django 5.0 on 2024-01-16 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_ingridiant'),
    ]

    operations = [
        migrations.AddField(
            model_name='centre',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='client',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employe',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='fournisseur',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
