from json import load
from modules.addresses import UniswapV3RouterAdresses

def get_abi(abi_name: str) -> dict:
    with open(f'../abis/{abi_name}.abi') as f:
        return load(f)


class Connector:
    def __init__(self, network, w3) -> None:
        """ Initialize connector
        """
        self.network = network
        self.w3 = w3

        self.v3router = self.w3.eth.contract(UniswapV3RouterAdresses[self.network].value, abi=get_abi("uniswapV3/router"))


    def get_pair(self, token0, token1, fee):
        """ Given a token pair and a fee, returns the pool
        """
        pass


    def __get_pairs(self):
        """ Return all token pairs at all fee levels as 
        """
        pass