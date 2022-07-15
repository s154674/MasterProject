from argparse import RawDescriptionHelpFormatter
from statistics import mode
from unicodedata import name
from django.db import models

# Create your models here.
class ERC20(models.Model):
    name = models.CharField(max_length=30, null=True)
    symbol = models.CharField(max_length=10, unique=True)
    decimals = models.PositiveSmallIntegerField(default=18)


class Networks(models.Model):
    name = models.CharField(max_length=20, unique=True)
    chain_id = models.SmallIntegerField(null=True)
    short = models.CharField(max_length=4, unique=True)


class ERC20Addresses(models.Model):
    ERC20 = models.ForeignKey(ERC20, on_delete=models.PROTECT)
    network = models.ForeignKey(Networks, on_delete=models.PROTECT)
    address = models.CharField(max_length=256)

    class Meta:
        unique_together = ["ERC20", "network"]

class PoolAddresses(models.Model):
    network = models.ForeignKey(Networks, on_delete=models.PROTECT)
    token0 = models.ForeignKey(ERC20, on_delete=models.PROTECT, related_name="token0")
    token1 = models.ForeignKey(ERC20, on_delete=models.PROTECT, related_name="token1")
    fee_tier = models.PositiveBigIntegerField()
    address = models.CharField(max_length=256)

    class Meta:
        unique_together = ["token0", "token1", "fee_tier", "network"]
class SwapEvent(models.Model):
    event_hash = models.CharField(max_length=256)
    sender = models.CharField(max_length=256)
    recipient = models.CharField(max_length=256)
    amount0 = models.CharField(max_length=256)
    amount1 = models.CharField(max_length=256)
    sqrtPriceX96 = models.CharField(max_length=256)
    liquidity = models.CharField(max_length=256)
    tick = models.CharField(max_length=256)
