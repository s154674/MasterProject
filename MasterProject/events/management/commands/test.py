from django.core.management.base import BaseCommand, CommandError
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.secrets import secrets
from events.models import PoolAddresses, ERC20, Networks, SwapEvent, TransactionMeta, BlockTimes
from modules.connector import UniConnector
from modules.blocktimes import Blocktimes
from web3 import Web3
from django.db.models import Q, Max, Min, Avg
from datetime import datetime
from itertools import combinations
from time import sleep
import json
import requests, math
from datetime import datetime


class Command(BaseCommand):
    help = 'used for testing stuff'

    def add_arguments(self, parser):
        # parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        
        # MAIN = Networks.objects.get_or_create(name="Mainnet Ethereum", chain_id=1, short="MAIN")[0]
        # ARBI = Networks.objects.get_or_create(name="Arbitrum One", chain_id=42161, short="ARBI")[0]
        # OPTI = Networks.objects.get_or_create(name="Optimism", chain_id=10, short="OPTI")[0]
        # POLY = Networks.objects.get_or_create(name="Mainnet Polygon", chain_id=137, short="POLY")[0]
        
        # print(f'All : {SwapEvent.objects.all().count()}')

        # print(f'Main: {SwapEvent.objects.filter(pool_address__network = MAIN ).count()}')
        # print(f'Arbi: {SwapEvent.objects.filter(pool_address__network = ARBI ).count()}')
        # print(f'Opti: {SwapEvent.objects.filter(pool_address__network = OPTI ).count()}')
        # print(f'Poly: {SwapEvent.objects.filter(pool_address__network = POLY ).count()}')
            

        # print(f'Not-null transaction meta count: {SwapEvent.objects.filter(~Q(transaction_meta=None)).count()}')
        # SwapEvent.objects.filter(~Q(transaction_meta=None)).delete()
        # TransactionMeta.objects.all().delete()

        # print('hello', TransactionMeta.objects.all().count())
        # print(f'Not-null transaction meta count: {SwapEvent.objects.filter(~Q(transaction_meta=None)).count()}')

        # print(SwapEvent.objects.all().count())

        # pools = PoolAddresses.objects.all()
        # for pool in pools:
            
        #     print(pool.id, SwapEvent.objects.filter(pool_address=pool).count())
        
        # network = Networks.objects.get(short='MAIN')
        # bt = Blocktimes(network)
        # print('hi')
        # print(int(float(str(bt.block_to_time(14881650)))),bt.block_to_time(14881650))
        # print(bt.parse(bt.time_to_block(1654022064)))
        # print('byue')
        # tup = bt.get_range(15008519)
        # print(bt.test(15008519))
        # print(tup)
        # print(datetime.fromtimestamp(tup[0]), datetime.fromtimestamp(tup[1]))

        # for network1, network2 in combinations(Networks.objects.all(), 2):
        #     print(network1.short, network2.short)

        ##################################################
        # for network in Networks.objects.all():
        #     bt = Blocktimes(network)
        #     yes = 0
        #     no = 0
        #     sumdist = 0
        #     blocks = BlockTimes.objects.filter(network=network)
        #     print(network.short)
        #     for i, blocktime in enumerate(blocks):
        #         if i != 999:
        #             dist = blocks[i+1].timestamp - blocks[i].timestamp

        #             if dist >= 0:
        #                 sumdist += dist 
        #             else:
        #                 raise Exception('thats a negative')

        #         (lower, upper) = bt.get_range(blocktime.blockNumber)
        #         if lower < blocktime.timestamp < upper:
        #             yes += 1
        #         else:
        #             no +=1

        #     print(f'yes: {yes}, no: {no}, avg_dist: {sumdist/1000}')


        ################################
        # network = Networks.objects.get(short='OPTI')
        # swapevents = SwapEvent.objects.filter(pool_address__network=network)

        # print(swapevents.aggregate(Max('transaction_meta__blockNumber')).values())

        # bt.aggregate(Max("datetime"))
        # bt.aggregate(Min("datetime"))

        ####
        import matplotlib.pyplot as plt

        x = [i+1 for i in range(1000)]

        for network in Networks.objects.all():
            y = []    
            for bt in BlockTimes.objects.filter(network=network):
                y.append(bt.timestamp)

            plt.plot(x,y,label=network.short)

        plt.ylabel('Unix Timestamp')
        plt.xlabel('Sample block #')
        plt.legend()
        plt.show()


        ################

        # url = secrets[f'OPTI_URL']
        # headers = {"Content-Type": "application/json"}
        # data = {"jsonrpc":"2.0","method":"eth_getBlockByNumber","params": [f'{hex(14046673)}',False],"id":1}

        
        # r = requests.post(url=url, headers=headers, data=json.dumps(data))
        # print(json.dumps(data))
        # temp = str(json.loads(r.text)['result']["timestamp"])
        # timestamp = int(temp,16)

        # dt_object = datetime.fromtimestamp(timestamp)

        # print("dt_object =", dt_object)
        # print(response)

        ###############        
        # print(BlockTimes.objects.filter(network__short='OPTI').count())

        # print(SwapEvent.objects.aggregate(Max('transaction_meta__blockNumber')))
        # print(BlockTimes.objects.filter(network=Networks.objects.get(short='OPTI')).aggregate(Min('blockNumber')))
        # swap_topic = "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67"
        
        # pool = PoolAddresses.objects.filter(network=Networks.objects.get(short='OPTI')).first()
        # data = {"jsonrpc":"2.0","method":"eth_getLogs","params":[{'address': pool.address , 'fromBlock': hex(int(14046373)), 'toBlock': hex(int(14046673)) , 'topics': [swap_topic]}],"id":1}
            
           
        # r = requests.post(url=secrets[f'OPTI_URL'], headers={"Content-Type": "application/json"}, data=json.dumps(data))
        # swap_events = json.loads(r.text)["result"]

        # print(swap_events)


        # for network in Networks.objects.all():
        #     values = []
        #     t0 = 0
        #     t1 = 0
        #     for i, bt in enumerate(BlockTimes.objects.filter(network=network)):
        #         if i == 0:
        #             t1 = bt.blockNumber
        #         else:
        #             t0 = t1
        #             t1 = bt.blockNumber
        #             # print(t1-t0)
        #             values.append(t1-t0)

        #     print(network.short, int(1+math.floor(sum(values)/len(values))))

            
        


