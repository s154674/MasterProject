from configparser import SectionProxy
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.secrets import secrets
from web3 import Web3
from json import load


def get_abi(abi_name: str) -> dict:
    with open(f'../abis/{abi_name}.abi') as f:
        return load(f)['abi']


# w3 = Web3(Web3.HTTPProvider(f'http://{secrets["SERVER_IP"]}:{secrets["L1_RPC"]}'))
w3 = Web3(Web3.HTTPProvider(secrets["INFURA_URL"]))


print(w3.isConnected())


UniSwapV2Factory = w3.eth.contract("0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f", abi=get_abi("uniswapV2/factory"))

print(UniSwapV2Factory.address, UniSwapV2Factory.abi, UniSwapV2Factory.functions.allPairsLength().call())

print(UniSwapV2Factory.functions.allPairs(1).call())

print(UniSwapV2Factory.functions.getPair("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2").call())

arbi = Web3(Web3.HTTPProvider(secrets['ARBITRUM_URL']))

print(arbi.isConnected())

opti = Web3(Web3.HTTPProvider(secrets['OPTIMISM_URL']))

print(opti.isConnected())


networks = ["MAIN", "ARBI", "OPTI"]

from modules.connector import Connector

arbi = Connector('ARBI', arbi)

