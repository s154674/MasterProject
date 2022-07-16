# Generated by Django 4.0.6 on 2022-07-16 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_swapevent_amount0_alter_swapevent_amount1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='swapevent',
            name='amount0',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='swapevent',
            name='amount1',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='swapevent',
            name='liquidity',
            field=models.PositiveBigIntegerField(),
        ),
        migrations.AlterField(
            model_name='swapevent',
            name='sqrtPriceX96',
            field=models.PositiveBigIntegerField(),
        ),
        migrations.AlterField(
            model_name='swapevent',
            name='tick',
            field=models.BigIntegerField(),
        ),
    ]
