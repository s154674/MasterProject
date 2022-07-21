from email.policy import Policy
from multiprocessing import Pool
from xml.dom import UserDataHandler
from django.core.management.base import BaseCommand, CommandError
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from events.models import PoolAddresses, ERC20, Networks, SwapEvent, TransactionMeta
from modules.connector import UniConnector
from django.db.models import Count, F, Q
from web3 import Web3
from itertools import combinations


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

        networks = [MAIN, ARBI, OPTI, POLY]

        USDT = ERC20.objects.get(symbol="USDT")
        USDC = ERC20.objects.get(symbol="USDC")
        DAI  = ERC20.objects.get(symbol="DAI" )
        WETH = ERC20.objects.get(symbol="WETH")
        WBTC = ERC20.objects.get(symbol="WBTC")

        ERC20s = [USDT,USDC,DAI,WETH,WBTC]


        print("June data")

        june_main_senders = SwapEvent.objects.filter(~Q(transaction_meta=None), pool_address__network = MAIN).values("sender").distinct()
        print(len(june_main_senders))

        june_arbi_senders = SwapEvent.objects.filter(~Q(transaction_meta=None), pool_address__network = ARBI).values("sender").distinct()
        print(len(june_arbi_senders))

        june_opti_senders = SwapEvent.objects.filter(~Q(transaction_meta=None), pool_address__network = OPTI).values("sender").distinct()
        print(len(june_opti_senders), june_opti_senders)

        june_poly_senders = SwapEvent.objects.filter(~Q(transaction_meta=None), pool_address__network = POLY).values("sender").distinct()
        print(len(june_poly_senders))

        temp=TransactionMeta.objects.all()[0].removed
        print(type(temp), temp)

        

        for network1, network2 in combinations(networks, 2):
            for coin1, coin2 in combinations(ERC20s, 2):
                if coin1 in [WBTC, WETH] or coin2 in [WBTC, WETH]:
                    q1 = Q(pool_address__token0=coin1) | Q(pool_address__token0=coin2)
                    q2 = Q(pool_address__token1=coin1) | Q(pool_address__token1=coin2)
                    n1_swaps = SwapEvent.objects.filter(q1, q2, pool_address__network=network1)
                    n2_swaps = SwapEvent.objects.filter(q1, q2, pool_address__network=network2)

                    print(n1_swaps[0].pool_address.token0)
                    # If pair has swaps on both networks
                    
                    n1_swaps_coin1 = []
                    n1_swaps_coin2 = []
                    n2_swaps_coin1 = []
                    n2_swaps_coin2 = []

                    crosschain_arb = []


                    if n1_swaps and n2_swaps:
                        if n1_swaps[0].pool_address.token0 == coin1:
                            for swap in n1_swaps:
                                n1_swaps_coin1.append((swap.pk, swap.amount0))
                                n1_swaps_coin2.append((swap.pk, swap.amount1))
                        else:
                            for swap in n1_swaps:
                                n1_swaps_coin1.append((swap.pk, swap.amount1))
                                n1_swaps_coin2.append((swap.pk, swap.amount0))
                        if n2_swaps[0].pool_address.token1 == coin2:
                            for swap in n2_swaps:
                                n2_swaps_coin1.append((swap.pk, swap.amount0))
                                n2_swaps_coin2.append((swap.pk, swap.amount1))
                        else:
                            for swap in n2_swaps:
                                n2_swaps_coin1.append((swap.pk, swap.amount1))
                                n2_swaps_coin2.append((swap.pk, swap.amount0))

                        
                        for i in range(len(n1_swaps)):
                            n1_coin1_amount = n1_swaps_coin1[i][1]
                            n1_coin2_amount = n1_swaps_coin2[i][1]
                            for j in range(len(n2_swaps)):
                                n2_coin1_amount = n2_swaps_coin1[j][1]
                                n2_coin2_amount = n2_swaps_coin2[j][1]

                                if n1_coin1_amount == - n2_coin1_amount:
                                    crosschain_arb.append((n1_swaps[i], n2_swaps[j]))
                                if n1_coin2_amount == - n2_coin2_amount:
                                    crosschain_arb.append((n1_swaps[i], n2_swaps[j]))
                        print(crosschain_arb)
                    else:
                        pass # we pass if no swaps in one of the networks


        
    def check_erc20_pair_ordering(self):
        """ the pair ordering is not consistent across networks.
        """
        USDT = ERC20.objects.get(symbol="USDT")
        USDC = ERC20.objects.get(symbol="USDC")
        DAI  = ERC20.objects.get(symbol="DAI" )
        WETH = ERC20.objects.get(symbol="WETH")
        WBTC = ERC20.objects.get(symbol="WBTC")

        ERC20s = [USDT,USDC,DAI,WETH,WBTC]

        for coin1, coin2 in combinations(ERC20s, 2):
            temp1 = PoolAddresses.objects.filter(token0=coin1,token1=coin2)
            temp2 = PoolAddresses.objects.filter(token0=coin2,token1=coin1)

            if bool(temp1) != bool(temp2):
                print('yes')
            else:
                print("NOOOOOOOOOOOOOOOO")