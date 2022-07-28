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

        router_addresses = ['0xE592427A0AEce92De3Edee1F18E0157C05861564', '0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45', '0x1111111254fb6c44bAC0beD2854e76F90643097d']

        print(f'Main ex router: {SwapEvent.objects.filter(pool_address__network = MAIN ).exclude(sender__in=router_addresses).count()}')
        print(f'Arbi ex router: {SwapEvent.objects.filter(pool_address__network = ARBI ).exclude(sender__in=router_addresses).count()}')
        print(f'Opti ex router: {SwapEvent.objects.filter(pool_address__network = OPTI ).exclude(sender__in=router_addresses).count()}')
        print(f'Poly ex router: {SwapEvent.objects.filter(pool_address__network = POLY ).exclude(sender__in=router_addresses).count()}')

        # print(SwapEvent.objects.all().count(Q(sender=F('recipient'))))
        print('Same sender and recipiant', SwapEvent.objects.filter(sender=F('recipient')).count())

        main_senders = SwapEvent.objects.filter(pool_address__network = MAIN).values("sender").distinct()
        arbi_senders = SwapEvent.objects.filter(pool_address__network = ARBI).values("sender").distinct()
        opti_senders = SwapEvent.objects.filter(pool_address__network = OPTI).values("sender").distinct()
        poly_senders = SwapEvent.objects.filter(pool_address__network = POLY).values("sender").distinct()
        
        print('main senders: ',len(main_senders))
        print('arbi senders: ',len(arbi_senders))
        print('opti senders: ',len(opti_senders))
        print('poly senders: ',len(poly_senders))

        # main_recipient = SwapEvent.objects.filter(pool_address__network = MAIN).values("recipient").distinct()
        # arbi_recipient = SwapEvent.objects.filter(pool_address__network = ARBI).values("recipient").distinct()
        # opti_recipient = SwapEvent.objects.filter(pool_address__network = OPTI).values("recipient").distinct()
        # poly_recipient = SwapEvent.objects.filter(pool_address__network = POLY).values("recipient").distinct()
        
        

        # print('main recipient: ',len(main_recipient))
        # print('arbi recipient: ',len(arbi_recipient))
        # print('opti recipient: ',len(opti_recipient))
        # print('poly recipient: ',len(poly_recipient))
        # print(len(main_senders.intersection(arbi_senders).intersection(opti_senders).intersection(poly_senders)))

        # print(main_senders.intersection(arbi_senders))

        print('Tolo',SwapEvent.objects.filter(pool_address__network = OPTI).distinct('event_hash').count())

        

        print('main arbi senders', main_senders.intersection(arbi_senders))
        print('main opti senders', main_senders.intersection(opti_senders))
        print('main poly senders', main_senders.intersection(poly_senders))
        print('arbi opti senders', arbi_senders.intersection(opti_senders))
        print('arbi poly senders', arbi_senders.intersection(poly_senders))
        print('opti poly senders', opti_senders.intersection(poly_senders))

        
        descriptor = ['main arbi senders','main opti senders','main poly senders','arbi opti senders','arbi poly senders','opti poly senders']
        q_set = [main_senders.intersection(arbi_senders), main_senders.intersection(opti_senders), main_senders.intersection(poly_senders), arbi_senders.intersection(opti_senders), arbi_senders.intersection(poly_senders),  opti_senders.intersection(poly_senders)]

        for i in range(6):
            print(descriptor[i])
            for j in q_set[i]:
                if j['sender'] not in router_addresses:
                    print(j['sender'])
           
        # print('main arbi senders', main_senders.intersection(arbi_senders))
        # print('main opti senders', main_senders.intersection(opti_senders))
        # print('main poly senders', main_senders.intersection(poly_senders))
        # print('arbi opti senders', arbi_senders.intersection(opti_senders))
        # print('arbi poly senders', arbi_senders.intersection(poly_senders))
        # print('opti poly senders', arbi_senders.intersection(opti_senders))

        # print('main arbi recipient', main_recipient.intersection(arbi_recipient))
        # print('main poly recipient', main_recipient.intersection(poly_recipient))
        # print('arbi poly recipient', arbi_recipient.intersection(poly_recipient))

        
        # for obj in SwapEvent.objects.filter(recipient = '0x6ae03D1d3A9b161ec264C76AD73999EE25AbEC5a'):
        #     print(obj.sender, obj.recipient, obj.pool_address.address, obj.amount0, obj.amount1, obj.transaction_meta.transactionHash)

        # Decently usefull
        # count = 0
        # for idk in main_recipient.intersection(arbi_recipient):
        #     if idk['recipient'] in PoolAddresses.objects.all().values('address'):
        #         count += 1

        # print(f'count: {count}, len of recipiants: {len(main_recipient.intersection(arbi_recipient))}')
        main_list = []

        for sender in main_senders:
            main_list.append(sender["sender"])

        arbi_list = []

        for sender in arbi_senders:
            arbi_list.append(sender["sender"])


        # print(SwapEvent.objects.filter(sender='0xF25d1CeA9772e2584E0A1d4c11AbEa2AEB9B077b'))
        
        # another address 0x00000000000B69eC332f49b7c4d2b101f93c3bed
        # 0xF25d1CeA9772e2584E0A1d4c11AbEa2AEB9B077b
            
        # print(SwapEvent.objects.get(pk=207136).values())

        # Mev bot that gets cuts from other addresses transactions 0x0000e0ca771e21bd00057f54a68c30d400000000