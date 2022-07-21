from email.policy import Policy
from multiprocessing import Pool
from xml.dom import UserDataHandler
from django.core.management.base import BaseCommand, CommandError
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from events.models import PoolAddresses, ERC20, Networks, SwapEvent, TransactionMeta, Networks
from modules.connector import UniConnector
from django.db.models import Count, F, Q
from web3 import Web3
from itertools import combinations
from hexbytes import HexBytes
import base64

class Command(BaseCommand):
    help = 'used for testing stuff'

    def add_arguments(self, parser):
        parser.add_argument('pk_one' , nargs='+' , type=int, 
        help='primary key of first SwapEvent')
        parser.add_argument('pk_two', nargs='+', type=int, 
        help='primary key of second SwapEvent')

    def handle(self, *args, **options):
        # print(options)
        one = SwapEvent.objects.get(pk=int(options["pk_one"][0]))
        two = SwapEvent.objects.get(pk=int(options['pk_two'][0]))

        # print(vars(one))
        n1 = Networks.objects.get(pk=PoolAddresses.objects.get(pk=one.pool_address_id).network_id).short
        t1 = TransactionMeta.objects.get(pk=one.transaction_meta_id).transactionHash
        n2 = Networks.objects.get(pk=PoolAddresses.objects.get(pk=two.pool_address_id).network_id).short
        t2 = TransactionMeta.objects.get(pk=two.transaction_meta_id).transactionHash

        # print(vars(t2))
        # print(vars(TransactionMeta.objects.get(pk=two.transaction_meta_id)))

        
        # print(t2)

        # temp3 = ""
        # for i in t2[2:-1]:
        #     temp3 += i
        
        # print(str(temp3))
        # print(bytes(str(temp3).encode('utf-8'),'utf-8'))
        # temp = base64.b64decode(t2[1:-1]).hex()
        # print("temp: ", temp)
        print((n1,t1),(n2,t2))