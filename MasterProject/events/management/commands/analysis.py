from django.core.management.base import BaseCommand, CommandError
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from events.models import PoolAddresses, ERC20, Networks, SwapEvent
from modules.connector import UniConnector
from django.db.models import Count, F, Q
from web3 import Web3


class Command(BaseCommand):
    help = 'used for testing stuff'

    def add_arguments(self, parser):
        # parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        
        MAIN = Networks.objects.get_or_create(name="Mainnet Ethereum", chain_id=1, short="MAIN")[0]
        ARBI = Networks.objects.get_or_create(name="Arbitrum One", chain_id=42161, short="ARBI")[0]
        OPTI = Networks.objects.get_or_create(name="Optimism", chain_id=10, short="OPTI")[0]
        POLY = Networks.objects.get_or_create(name="Mainnet Polygon", chain_id=137, short="POLY")[0]
        
        print(f'All : {SwapEvent.objects.all().count()}')

        print(f'Main: {SwapEvent.objects.filter(pool_address__network = MAIN ).count()}')
        print(f'Arbi: {SwapEvent.objects.filter(pool_address__network = ARBI ).count()}')
        print(f'Opti: {SwapEvent.objects.filter(pool_address__network = OPTI ).count()}')
        print(f'Poly: {SwapEvent.objects.filter(pool_address__network = POLY ).count()}')

        print(SwapEvent.objects.all().values("sender").annotate(total=Count('sender')))

        # print(SwapEvent.objects.all().count(Q(sender=F('recipient'))))
        print(SwapEvent.objects.filter(transaction_meta = None, sender=F('recipient')).count())

        main_senders = SwapEvent.objects.filter(transaction_meta = None, pool_address__network = MAIN).values("sender").distinct()
        print(len(main_senders))
        
        arbi_senders = SwapEvent.objects.filter(transaction_meta = None, pool_address__network = ARBI).values("sender").distinct()

        print(len(arbi_senders))


        opti_senders = SwapEvent.objects.filter(transaction_meta = None, pool_address__network = OPTI).values("sender").distinct()

        print(len(opti_senders))


        poly_senders = SwapEvent.objects.filter(transaction_meta = None, pool_address__network = POLY).values("sender").distinct()

        print(len(poly_senders))
        
        print(len(main_senders.intersection(arbi_senders).intersection(opti_senders).intersection(poly_senders)))

        print(main_senders.intersection(arbi_senders))

        main_list = []

        for sender in main_senders:
            main_list.append(sender["sender"])

        arbi_list = []

        for sender in arbi_senders:
            arbi_list.append(sender["sender"])


        print(SwapEvent.objects.filter(sender='0xF25d1CeA9772e2584E0A1d4c11AbEa2AEB9B077b'))
        
        # another address 0x00000000000B69eC332f49b7c4d2b101f93c3bed
            
        # print(SwapEvent.objects.get(pk=207136).values())

        print("June data")

        june_main_senders = SwapEvent.objects.filter(~Q(transaction_meta=None), pool_address__network = MAIN).values("sender").distinct()
        print(len(june_main_senders))

        june_arbi_senders = SwapEvent.objects.filter(~Q(transaction_meta=None), pool_address__network = ARBI).values("sender").distinct()
        print(len(june_arbi_senders))

        june_opti_senders = SwapEvent.objects.filter(~Q(transaction_meta=None), pool_address__network = OPTI).values("sender").distinct()
        print(len(june_opti_senders), june_opti_senders)

        june_poly_senders = SwapEvent.objects.filter(~Q(transaction_meta=None), pool_address__network = POLY).values("sender").distinct()
        print(len(june_poly_senders))