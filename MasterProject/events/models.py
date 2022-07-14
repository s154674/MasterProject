from statistics import mode
from unicodedata import name
from django.db import models

# Create your models here.
class ERC20(models.Model):
    name = models.CharField(max_length=30, null=True)
    symbol = models.CharField(max_length=10)


class Networks(models.Model):
    name = models.CharField(max_length=20)
    chain_id = models.SmallIntegerField(null=True)


class ERC20Addresses(models.Model):
    ERC20 = models.ForeignKey(ERC20, on_delete=models.PROTECT)
    network = models.ForeignKey(Networks, on_delete=models.PROTECT)
    address = models.CharField(max_length=256)


class PoolAddresses(models.Model):
    network = models.ForeignKey(Networks, on_delete=models.PROTECT)
    token0 = models.ForeignKey(ERC20, on_delete=models.PROTECT)
    token1 = models.ForeignKey(ERC20, on_delete=models.PROTECT)
    address = models.CharField(max_length=256)