from json import load

from urllib3 import Retry
from events.models import SwapEvent, TransactionMeta
from modules.addresses import UniswapV3Addresses, PolygonAddresses, EthereumAddresses, ArbitrumAddresses, OptimismAddresses
import sys, os
from web3 import Web3
from itertools import combinations
from modules.fees import MainPolyFees, OptiArbiFees
import requests
from json import dumps,loads
from modules.blocktimes import MainBlocks, ArbiBlocks, OptiBlocks, PolyBlocks
import math
from attributedict.collections import AttributeDict
from hexbytes import HexBytes
from collections.abc import Sequence
from time import sleep
from requests import ConnectionError

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.secrets import secrets

def get_abi(abi_name: str) -> dict:
    with open(f'C:/Users/Johan/Desktop/MasterProject/MasterProject/abis/{abi_name}.abi') as f:
        return load(f)


class UniConnector:
    """ Class to connect to and extract data from Uniswap. Is chain agnostic.
    """
    def __init__(self, network) -> None:
        """ Initialize connector
        """
        self.network = network
        
        # Check valid network
        if network in ["ARBI", "OPTI", "MAIN", "POLY"]:
            
            # Fetch correct addresses
            if self.network == "ARBI":
                temp = ArbitrumAddresses
            if self.network == "OPTI":
                temp = OptimismAddresses
            if self.network == "MAIN":
                temp = EthereumAddresses
            if self.network == 'POLY':
                temp = PolygonAddresses
            
            self.ERC20addresses = temp
        else:
            raise Exception(f"Not valid network name: {network}")
        
        # Set fee tiers (only main and poly has 0.01 % tier)
        if self.network in ["MAIN", "POLY"]:
            self.fees = MainPolyFees
        else:
            self.fees = OptiArbiFees

        # Get W3 object
        self.w3 = Web3(Web3.HTTPProvider(secrets[f'{network}_URL']))

        # These are static, because they are deployed at the same addresses across networks
        self.router = self.w3.eth.contract(UniswapV3Addresses["ROUTER"].value, abi=get_abi("uniswapV3/router"))
        self.factory = self.w3.eth.contract(UniswapV3Addresses["FACTORY"].value, abi=get_abi("uniswapV3/factory"))

        # Pools are deployed by the factory, so we save the ABI here to use in the future.
        self.pool_abi = get_abi("uniswapV3/pool")
        self.pool_event_parser_contract = self.w3.eth.contract(abi=self.pool_abi)


    def get_pool_addresses(self):
        """ Return the pool addresses. 
        """
        # For all unique ERC20 pairs
        for pair in combinations(self.ERC20addresses, 2):
            # For each fee tier
            for fee in self.fees:
                # print(pair[0].value, pair[1].value, fee.value)
                pool_address = self.factory.functions.getPool(pair[0].value, pair[1].value, fee.value).call()
                pool = self.w3.eth.contract(pool_address, abi=self.pool_abi)
                
                if pool_address != "0x0000000000000000000000000000000000000000":
                    yield self.ERC20addresses(pool.functions.token0().call()).name, self.ERC20addresses(pool.functions.token1().call()).name, fee, pool_address
                else:
                    pass # Pool doesnt exists/hasn't been created yet
                

    def event_parser(self, event):
        """ Parses events into models and stores them in the database.
        """
        
        temp = AttributeDict({'address': event["address"], 
        'blockHash': HexBytes(event["blockHash"]), 
        'blockNumber': int(event['blockNumber'], 16), 
        'data': event['data'],
        'logIndex': int(event['logIndex'],16), 
        'removed': event['removed'], 
        'topics': [HexBytes(topic) for topic in event['topics']],
        'transactionHash': HexBytes(event['transactionHash']), 
        'transactionIndex': int(event['transactionIndex'],16)})

        return temp, self.pool_event_parser_contract.events.Swap().processLog(temp)


    def get_block_range(self):
        if self.network == "MAIN":
            return MainBlocks.ALL.value
        elif self.network == "ARBI":
            return ArbiBlocks.ALL.value
        elif self.network == "OPTI":
            return OptiBlocks.ALL.value
        elif self.network == "POLY":
            return PolyBlocks.ALL.value
        else:
            return None


    def get_swap_events(self, pool):
        # found by keccak256(b'Swap(address,address,int256,int256,uint160,uint128,int24)')
        swap_topic = "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67"
        
        # Init list of block ranges
        block_ranges = []

        block_ranges.append(self.get_block_range())
        
        def split_ranges(lst, n):
            "Splits range into n smaller chunks to get less API timeouts/too big response erros"
            item = lst.pop()
            if (item[1] - item[0]) > n:
                amount = int(math.floor((item[1]-item[0])/n))
                temp = item[0]
                for i in range(n):
                    if i != (n-1):
                        temp = temp + amount
                        lst.append(((temp-amount),temp))
                    else:
                        lst.append((temp, item[1]))
            else:
                lst.append((item[0],item[1]))

        split_ranges(block_ranges, 6)
        
        while block_ranges:
            current_range = block_ranges.pop()
            
            # params = [{'address': pool.address , 'fromBlock': hex(current_range[0]), 'toBlock': hex(current_range[1]) , 'topics': [swap_topic]}]
            
            # params = [{'address': pool.address , 'fromBlock': f'{current_range[0]:x}', 'toBlock': f'{current_range[1]:x}', 'topics': [swap_topic]}]
            # print(pool.address, hex(int(current_range[0])), hex(int(current_range[1])), swap_topic)
            data = {"jsonrpc":"2.0","method":"eth_getLogs","params":[{'address': pool.address , 'fromBlock': hex(int(current_range[0])), 'toBlock': hex(int(current_range[1])) , 'topics': [swap_topic]}],"id":1}
            
           
            try:
                r = requests.post(url=secrets[f'{self.network}_URL'], headers={"Content-Type": "application/json"}, data=dumps(data))
                swap_events = loads(r.text)["result"]


                if type(swap_events) != list:
                    raise Exception(f'Swap_events type: {type(swap_events)}')

                swaps_list = []
                transaction_list = []

                # print(len(swap_events))
                for event in swap_events:
                    parsed_event = self.event_parser(event)
                    event["blockNumber"] = int(event['blockNumber'], 16)
                    event["logIndex"] = int(event['logIndex'], 16)
                    obj = TransactionMeta(**event)

                    transaction_list.append(obj)
                    swaps_list.append(SwapEvent(transaction_meta=obj, pool_address=pool, **parsed_event.args))
                    # Bulk insert every 1000 objects
                    if len(swaps_list) > 1000:
                        # print('Hi')
                        idk = TransactionMeta.objects.bulk_create(transaction_list)
                        # print(idk)
                        transaction_list = []
                        SwapEvent.objects.bulk_create(swaps_list)
                        swaps_list = []

                # insert tail if present
                if transaction_list:
                    TransactionMeta.objects.bulk_create(transaction_list)
                if swaps_list:
                    SwapEvent.objects.bulk_create(swaps_list)

            except KeyError:
                if loads(r.text)['error']['code'] in [-32005, -32605]:
                    #split blockrange
                    span = current_range[1] - current_range[0]
                    if span == 1:
                        raise Exception("Span is 1")
                    half = span/2
                    if half.is_integer():
                        block_ranges.append((current_range[0],current_range[0]+half))
                        block_ranges.append((current_range[1]-(half-1),current_range[1]))
                    else:
                        block_ranges.append((current_range[0],current_range[0]+math.floor(half)))
                        block_ranges.append((current_range[1]-math.floor(half),current_range[1]))
                    pass
                else:
                    raise Exception(f"Unkown infura respons for params:\n{data}\n Response was \n{r.status_code, r.text}\n")

            except ConnectionError as ex:
                print("body: ", r.request.body)
                print("url: ", r.request.url)
                print("headers: ", r.request.headers)
                raise ex
            


    def test_token(self):
        pool = self.w3.eth.contract("0xbb256c2F1B677e27118b0345FD2b3894D2E6D487", abi=self.pool_abi) 

        print(pool.functions.token0().call(), pool.functions.token1().call())