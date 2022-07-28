from email.policy import Policy
from math import comb
from multiprocessing import Pool
from xml.dom import UserDataHandler
from django.core.management.base import BaseCommand, CommandError
import sys, os

from eth_typing import BlockNumber
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from events.models import PoolAddresses, ERC20, Networks, SwapEvent, TransactionMeta, BlockTimes
from modules.connector import UniConnector
from modules.blocktimes import Blocktimes
from django.db.models import Count, F, Q
from web3 import Web3
from itertools import combinations
from attributedict.collections import AttributeDict
from tqdm import tqdm

# def print_verbose(string):
    
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

        def get_min_value(amount,erc20):
            return int(amount*10**erc20.decimals)
        
        # Minimum values, around 100 $ USD
        min_value = {USDT:get_min_value(1000, USDT), USDC:get_min_value(1000, USDC), DAI:get_min_value(1000, DAI), WETH:get_min_value(1, WETH), WBTC:get_min_value(0.05, WBTC)}
        
        block_range = {MAIN:218, ARBI:3841, OPTI: 4468, POLY:1453}

        router_addresses = ['0x1111111254fb6c44bAC0beD2854e76F90643097d', '0xE592427A0AEce92De3Edee1F18E0157C05861564', '0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45']
        # print(get_min_value(100, USDC))
        # for i in ERC20s:
        #     print(i.decimals)
        # pools = PoolAddresses.objects.filter(token0=USDC)
        # print(SwapEvent.objects.filter(pool_address=pools[0], amount0__gte=min_value[USDC]).count())

        print(SwapEvent.objects.filter(pool_address__network = OPTI).values('recipient').distinct().count())   

        
        # for networks network pairs
        for network1, network2 in combinations(networks, 2):
            print(f'n1: {network1.short}, n2: {network2.short}')
            n1 = AttributeDict()
            n2 = AttributeDict()
            # for coins
            for coin0, coin1 in combinations(ERC20s, 2):
                if not (coin1 == WETH or coin0 == WETH):
                    continue
                
                q1 = Q(token0=coin0) | Q(token0=coin1)
                q2 = Q(token1=coin0) | Q(token1=coin1)

                n1.pools = [i for i in PoolAddresses.objects.filter(q1, q2, network=network1)]
                n2.pools = [i for i in PoolAddresses.objects.filter(q1, q2, network=network2)]
                # n1_swaps = SwapEvent.objects.filter(q1, q2, pool_address__network=network1)
                # n2_swaps = [SwapEvent.objects.filter(q1, q2, pool_address__network=network2).first()]

                if n1.pools[0].token0 == coin0:
                    n1.coins = ("amount0", "amount1")
                    n1.coins = (coin0, coin1)
                else:
                    n1.coins_amount = ("amount1", "amount0")
                    n1.coins = (coin1, coin0)

                if n2.pools[0].token0 == coin0:
                    n2.coins_amount = ("amount0", "amount1")
                    n2.coins = (coin0, coin1)
                else:
                    n2.coins_amount = ("amount1", "amount0")
                    n2.coins = (coin1, coin0)

                
                # If pair has swaps on both networks

                n1.blocktimes = BlockTimes.objects.filter(network=network1)
                n2.blocktimes = BlockTimes.objects.filter(network=network2)
                n1_swaps =  SwapEvent.objects.filter(pool_address__in=n1.pools).exclude(recipient__in=router_addresses, sender__in=router_addresses)
                print(f'Amount {n1_swaps.count()}', coin0.symbol, coin1.symbol)
                # for swap event
                for i, n1_swap in enumerate(n1_swaps):
                    if i % 100 == 0 and i != 0:
                        print(f'done with: {i}')
                    
                    # find timestamps from blockNumber
                    lower = n1.blocktimes.filter(blockNumber__lte=n1_swap.transaction_meta.blockNumber-block_range[network1])[::-1]
                    upper = n1.blocktimes.filter(blockNumber__gte=n1_swap.transaction_meta.blockNumber+block_range[network1])
                    if lower:
                        if len(lower) >= 2:
                            lower = lower[1].timestamp
                        else:
                            lower = lower[0].timestamp
                    else:
                        print('1 not expected lower')
                        lower = n2.blocktimes.first().timestamp
                    
                    if upper:
                        if len(upper) >= 2:
                            upper = upper[1].timestamp
                        else:
                            upper = upper[0].timestamp

                    else:
                        print('1 not expected upper')
                        upper = n2.blocktimes.last().timestamp
                    
                    # lower = n1_swap.transaction_meta.timestamp - 3600
                    # upper = n1_swap.transaction_meta.timestamp + 3600

                    # print((lower, upper), upper-lower, "count: ",TransactionMeta.objects.filter(blockNumber__gte=lower, blockNumber__lte=upper).count())
                    # find other networks block numbers
                    lower = n2.blocktimes.filter(timestamp__lte = lower)[::-1]
                    upper = n2.blocktimes.filter(timestamp__gte = upper)
                    
                    if lower:
                        if len(lower) >= 2:
                            lower = lower[1].blockNumber
                        else:
                            lower = lower[0].blockNumber
                    else:
                        print('2 not expected lower')
                        lower = n2.blocktimes.first().blockNumber
                    
                    if upper:
                        if len(upper) >= 2:
                            upper = upper[1].blockNumber
                        else:
                            upper = upper[0].blockNumber

                    else:
                        print('2 not expected higher')
                        upper = n2.blocktimes.last().blockNumber
                    
                        
                    # print((lower, upper), upper-lower, "count: ",TransactionMeta.objects.filter(blockNumber__gte=lower, blockNumber__lte=upper).count())
                    
                    # Select events from second network in range with coin0, coin1
                    for n2_swap in SwapEvent.objects.filter(pool_address__in=n2.pools, transaction_meta__blockNumber__gte=lower, transaction_meta__blockNumber__lte=upper).exclude(recipient__in=router_addresses, sender__in=router_addresses):
                        n1.amounts=(n1_swap.amount0, n1_swap.amount1)
                        n2.amounts=(n2_swap.amount0, n2_swap.amount1)
                        # print('jaskhjjkdsa',n1.coins, n2.coins)
                        if n1.coins == n2.coins:
                            pass
                        else:
                            n1.amounts = (n1.amounts[1], n1.amounts[0])

                        if n1.amounts[0] == - n2.amounts[0]:
                            print('first', n1_swap.transaction_meta.transactionHash, n2_swap.transaction_meta.transactionHash)
                        if n1.amounts[1] == - n2.amounts[1]:
                            print('second', n1_swap.transaction_meta.transactionHash, n2_swap.transaction_meta.transactionHash)
                        # print(n2_swap.values(n2.coin1_amount, n2.coin2_amount))
                        # print('idk', n2_swap)

        # return
                
        # n1_swaps_coin1 = []
        # n1_swaps_coin2 = []
        # n2_swaps_coin1 = []
        # n2_swaps_coin2 = []

        # crosschain_arb = []


        # if n1_swaps and n2_swaps:
        #     if n1_swaps[0].pool_address.token0 == coin1:
        #         for swap in n1_swaps:
        #             n1_swaps_coin1.append((swap.pk, swap.amount0))
        #             n1_swaps_coin2.append((swap.pk, swap.amount1))
        #     else:
        #         for swap in n1_swaps:
        #             n1_swaps_coin1.append((swap.pk, swap.amount1))
        #             n1_swaps_coin2.append((swap.pk, swap.amount0))
        #     if n2_swaps[0].pool_address.token1 == coin2:
        #         for swap in n2_swaps:
        #             n2_swaps_coin1.append((swap.pk, swap.amount0))
        #             n2_swaps_coin2.append((swap.pk, swap.amount1))
        #     else:
        #         for swap in n2_swaps:
        #             n2_swaps_coin1.append((swap.pk, swap.amount1))
        #             n2_swaps_coin2.append((swap.pk, swap.amount0))

            
        #     for i in range(len(n1_swaps)):
        #         n1_coin1_amount = n1_swaps_coin1[i][1]
        #         n1_coin2_amount = n1_swaps_coin2[i][1]
        #         for j in range(len(n2_swaps)):
        #             n2_coin1_amount = n2_swaps_coin1[j][1]
        #             n2_coin2_amount = n2_swaps_coin2[j][1]

        #             if n1_coin1_amount == - n2_coin1_amount:
        #                 crosschain_arb.append((n1_swaps[i], n2_swaps[j]))
        #             if n1_coin2_amount == - n2_coin2_amount:
        #                 crosschain_arb.append((n1_swaps[i], n2_swaps[j]))
        #     print(crosschain_arb)
        # else:
        #     pass # we pass if no swaps in one of the networks


        
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