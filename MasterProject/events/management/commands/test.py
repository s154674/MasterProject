from django.core.management.base import BaseCommand, CommandError
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from events.models import PoolAddresses, ERC20, Networks
from modules.connector import UniConnector

class Command(BaseCommand):
    help = 'used for testing stuff'

    def add_arguments(self, parser):
        # parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def handle(self, *args, **options):

        for network in ["OPTI"]:
            con = UniConnector(network)
            for token0, token1, fee, address in con.get_pool_addresses():
                PoolAddresses.objects.create(network=Networks.objects.get(short=network), token0=ERC20.objects.get(symbol=token0), token1=ERC20.objects.get(symbol=token1), fee_tier=fee.value, address=address)
