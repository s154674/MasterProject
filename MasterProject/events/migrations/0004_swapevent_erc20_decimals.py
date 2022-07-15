# Generated by Django 4.0.6 on 2022-07-15 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_networks_short'),
    ]

    operations = [
        migrations.CreateModel(
            name='SwapEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_hash', models.CharField(max_length=256)),
                ('sender', models.CharField(max_length=256)),
                ('recipient', models.CharField(max_length=256)),
                ('amount0', models.IntegerField()),
                ('amount1', models.IntegerField()),
                ('sqrtPriceX96', models.PositiveIntegerField()),
                ('liquidity', models.PositiveIntegerField()),
                ('tick', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='erc20',
            name='decimals',
            field=models.PositiveSmallIntegerField(default=18),
        ),
    ]
