# Generated by Django 5.0.7 on 2024-08-04 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_ventep_khesara_ventep_mosa3ada'),
    ]

    operations = [
        migrations.AddField(
            model_name='ventep',
            name='montantTotalVenNeutre',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
