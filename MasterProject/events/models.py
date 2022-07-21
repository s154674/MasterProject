from argparse import RawDescriptionHelpFormatter
from dataclasses import dataclass
from statistics import mode
from unicodedata import decimal, name
from django.db import models
from eth_typing import BlockNumber

class BigIntegerField(models.IntegerField):
    empty_strings_allowed=False
    def get_internal_type(self):
        return "BigIntegerField"	
    def db_type(self, connection):
        return 'bigint'
class BiggerIntegerField(models.IntegerField):
    empty_strings_allowed=False
    def get_internal_type(self):
        return "BiggerIntegerField"	
    def db_type(self, connection):
        return 'NUMERIC(77)'

# Create your models here.
class ERC20(models.Model):
    name = models.CharField(max_length=30, null=True)
    symbol = models.CharField(max_length=10, unique=True)
    decimals = models.PositiveSmallIntegerField(default=18)


class Networks(models.Model):
    name = models.CharField(max_length=20, unique=True)
    chain_id = models.IntegerField(null=True)
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

        
class TransactionMeta(models.Model):
    address = models.CharField(max_length=256)
    blockHash = models.CharField(max_length=256)
    blockNumber = models.BigIntegerField()
    data = models.TextField()
    logIndex = models.BigIntegerField()
    removed = models.CharField(max_length=256)
    topics = models.CharField(max_length=256)
    transactionHash = models.CharField(max_length=256)
    transactionIndex = models.CharField(max_length=256)



class SwapEvent(models.Model):
    pool_address = models.ForeignKey(PoolAddresses, on_delete=models.PROTECT)
    transaction_meta = models.ForeignKey(TransactionMeta, on_delete=models.PROTECT, null=True, default=None)
    event_hash = models.CharField(max_length=256)
    sender = models.CharField(max_length=256)
    recipient = models.CharField(max_length=256)
    amount0 = models.DecimalField(max_digits=77, decimal_places=0)
    amount1 = models.DecimalField(max_digits=77, decimal_places=0)
    sqrtPriceX96 = models.CharField(max_length=100)
    liquidity = models.DecimalField(max_digits=77, decimal_places=0)
    tick = models.DecimalField(max_digits=77, decimal_places=0)

    class Meta:
        pass

class BlockTimes(models.Model):
    network = models.ForeignKey(Networks, on_delete=models.PROTECT)
    blockNumber = models.BigIntegerField()
    blockHash = models.CharField(max_length=256)
    timestamp = models.DecimalField(max_digits=77, decimal_places=0)
    datetime = models.DateTimeField()