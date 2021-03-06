from django.core.management.base import BaseCommand, CommandError
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from events.models import PoolAddresses, ERC20, ERC20Addresses, Networks, SwapEvent, TransactionMeta
from modules.connector import UniConnector
from modules.addresses import EthereumAddresses, ArbitrumAddresses, OptimismAddresses, PolygonAddresses
from attributedict.collections import AttributeDict
import time


class Command(BaseCommand):
    help = 'Used to populate tables with swap event data'

    def add_arguments(self, parser):
        # parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        
        # Get or create ERC20's
        WETH = ERC20.objects.get_or_create(name="Wrapped Ether", symbol="WETH")[0]
        WBTC = ERC20.objects.get_or_create(name="Wrapped Bitcoin", symbol="WBTC", decimals=8)[0]
        DAI  = ERC20.objects.get_or_create(name="DAI stablecoin", symbol="DAI")[0]
        USDC = ERC20.objects.get_or_create(name="USDC stablecoin", symbol="USDC", decimals=6)[0]
        USDT = ERC20.objects.get_or_create(name="USDT stablecoin", symbol="USDT", decimals=6)[0]

        # Get or create networks
        MAIN = Networks.objects.get_or_create(name="Mainnet Ethereum", chain_id=1, short="MAIN")[0]
        ARBI = Networks.objects.get_or_create(name="Arbitrum One", chain_id=42161, short="ARBI")[0]
        OPTI = Networks.objects.get_or_create(name="Optimism", chain_id=10, short="OPTI")[0]
        POLY = Networks.objects.get_or_create(name="Mainnet Polygon", chain_id=137, short="POLY")[0]

        # Load ERC20 addresses form Enums
        AddressEnums = [EthereumAddresses, ArbitrumAddresses, OptimismAddresses, PolygonAddresses]
        networks = [MAIN, ARBI, OPTI, POLY]
        for i in range(4):
            for coin in ERC20.objects.all():
                ERC20Addresses.objects.get_or_create(network=networks[i], ERC20=coin, address=AddressEnums[i][coin.symbol].value)

        # Fetch all the pool addresses
        if not PoolAddresses.objects.all().exists():
            for network in ["MAIN", "ARBI", "OPTI", "POLY"]:
                con = UniConnector(network)
                for token0, token1, fee, address in con.get_pool_addresses():
                    PoolAddresses.objects.create(network=Networks.objects.get(short=network), token0=ERC20.objects.get(symbol=token0), token1=ERC20.objects.get(symbol=token1), fee_tier=fee.value, address=address)

        if not SwapEvent.objects.all().exists():
            for i, network in enumerate(networks):
                print(f"Parsing swap events for network {network.short} - {i+1} of {len(networks)}")
                pool_addresses = PoolAddresses.objects.filter(network=network)
                for i, pool in enumerate(pool_addresses):

                    print(f"Parsing swap events for pool address id {pool.pk} - {i+1} of {len(pool_addresses)}")
                    start = time.time()
                    con = UniConnector(network.short)
                    con.get_swap_events(pool)
                    print(f'Took {time.time()-start}')

        
