# Generated by Django 4.0.6 on 2022-07-21 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_transactionmeta_events_tran_blocknu_de0c24_idx'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='swapevent',
            index=models.Index(fields=['transaction_meta'], name='events_swap_transac_4d0b9d_idx'),
        ),
    ]
