from django.core.management.base import BaseCommand, CommandError
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.secrets import secrets
from events.models import PoolAddresses, ERC20, ERC20Addresses, Networks, SwapEvent, TransactionMeta, BlockTimes
from modules.connector import UniConnector
from modules.addresses import EthereumAddresses, ArbitrumAddresses, OptimismAddresses, PolygonAddresses
from attributedict.collections import AttributeDict
import time, requests, json
import numpy as np
from modules.blocktimes import MainBlocks, ArbiBlocks, OptiBlocks, PolyBlocks
from datetime import datetime
from time import sleep

class Command(BaseCommand):
    help = 'used for testing stuff'

    def add_arguments(self, parser):
        # parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        """ split blocknumbers into a range space evenly over 1000 entries
        """
       
        for network in [Networks.objects.get(pk=4)]:
            blocks = None
            if network.short == 'MAIN':
                blocks = MainBlocks
            if network.short == 'POLY':
                blocks = PolyBlocks
            if network.short == 'ARBI':
                blocks = ArbiBlocks
            if network.short == 'OPTI':
                blocks = OptiBlocks
            
            if blocks:
                linspace = np.linspace(blocks.ALL.value[0], blocks.ALL.value[1], 1000).astype(int)
                objs = []
                for blockNumber in linspace:
                    url = secrets[f'{network.short}_URL']
                    headers = {"Content-Type": "application/json"}
                    data = {"jsonrpc":"2.0","method":"eth_getBlockByNumber","params": [f'{hex(blockNumber)}',False],"id":1}

                    for i in range(3):
                        r = requests.post(url=url, headers=headers, data=json.dumps(data))
                        print(json.dumps(data))
                        response = json.loads(r.text)
                        try:
                            timestamp = response['result']['timestamp']
                            blockhash = response['result']['hash']
                            break
                        except Exception:
                            print(response)
                            if i == 2:
                                raise Exception('Hello')
                            sleep(3)

                    objs.append(BlockTimes(network=network, blockNumber=blockNumber, blockHash=blockhash, timestamp=int(timestamp,16), datetime=datetime.fromtimestamp(int(timestamp,16))))
                
                BlockTimes.objects.bulk_create(objs)
            else:
                raise Exception("Typo")