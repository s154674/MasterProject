from json import load
from modules.addresses import UniswapV3Addresses, PolygonAddresses, EthereumAddresses, ArbitrumAddresses, OptimismAddresses
import sys, os
from web3 import Web3
from itertools import combinations
from modules.fees import MainPolyFees, OptiArbiFees

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.secrets import secrets

def get_abi(abi_name: str) -> dict:
    with open(f'../abis/{abi_name}.abi') as f:
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

    def get_pair(self, token0, token1, fee):
        """ Given a token pair and a fee, returns the pool
        """
        pass


    def __get_pairs(self):
        """ Return all token pairs at all fee levels as 
        """
        pass

    def get_pool_addresses(self) -> dict:
        """ Return the pool addresses. 
        """
        # For all unique ERC20 pairs
        for pair in combinations(self.ERC20addresses, 2):
            # For each fee tier
            for fee in self.fees:
                # print(pair[0].value, pair[1].value, fee.value)
                print(self.factory.functions.getPool(pair[0].value, pair[1].value, fee.value).call())
            
        # For all unique pairs in enumerator

    def event_parser(self):
        """ Parses events into models and stores them in the database.
        """
        pass