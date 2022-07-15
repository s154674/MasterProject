from django.core.management.base import BaseCommand, CommandError
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from events.models import PoolAddresses, ERC20, ERC20Addresses, Networks
from modules.connector import UniConnector
from modules.addresses import EthereumAddresses, ArbitrumAddresses, OptimismAddresses, PolygonAddresses


class Command(BaseCommand):
    help = 'used for testing stuff'

    def add_arguments(self, parser):
        # parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        
        WETH = ERC20.objects.get_or_create(name="Wrapped Ether", symbol="WETH")[0]
        WBTC = ERC20.objects.get_or_create(name="Wrapped Bitcoin", symbol="WBTC")[0]
        DAI  = ERC20.objects.get_or_create(name="DAI stablecoin", symbol="DAI")[0]
        USDC = ERC20.objects.get_or_create(name="USDC stablecoin", symbol="USDC")[0]
        USDT = ERC20.objects.get_or_create(name="USDT stablecoin", symbol="USDT")[0]

        MAIN = Networks.objects.get_or_create(name="Mainnet Ethereum", chain_id=1, short="MAIN")[0]
        ARBI = Networks.objects.get_or_create(name="Arbitrum One", chain_id=42161, short="ARBI")[0]
        OPTI = Networks.objects.get_or_create(name="Optimism", chain_id=10, short="OPTI")[0]
        POLY = Networks.objects.get_or_create(name="Mainnet Polygon", chain_id=137, short="POLY")[0]

        
        AddressEnums = [EthereumAddresses, ArbitrumAddresses, OptimismAddresses, PolygonAddresses]
        networks = [MAIN, ARBI, OPTI, POLY]
        for i in range(4):
            for coin in ERC20.objects.all():
                ERC20Addresses.objects.get_or_create(network=networks[i], ERC20=coin, address=AddressEnums[i][coin.symbol].value)