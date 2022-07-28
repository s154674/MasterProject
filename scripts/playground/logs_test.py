import requests
import sys, os
from Crypto.Hash import keccak
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.secrets import secrets
from json import dumps, loads

# body = {}

# filter_params = [{"address":"0x6B175474E89094C44Da98b954EedeAC495271d0F"},{"fromBlock":"earliest"},{"topics": ["ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"]}]
# filter_data = {"jsonrpc":"2.0","method":"eth_newFilter","params":filter_params,"id":1}
# # Make new filter 
# response = requests.post(url=secrets['MAIN_URL'], headers={"Content-Type": "application/json"}, data=dumps(filter_data))
# print(response.status_code, response.text)
# filter_id = loads(response.text)['result']
# print(filter_id)

# r = requests.post(url=secrets['MAIN_URL'], headers={"Content-Type": "application/json"}, data='{"jsonrpc":"2.0","method":"eth_getFilterLogs","params":["0x10ff0f5cef4cfa7aa83251a0689b83d5951afac9a4e9", {"fromBlock":"earliest"}, {"topics":["ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"]}],"id":1}')
# print(r.text)

# r = requests.post(url=secrets['MAIN_URL'], headers={"Content-Type": "application/json"}, data='{"jsonrpc":"2.0","method":"eth_getLogs","params":["0x6B175474E89094C44Da98b954EedeAC495271d0F", "fromBlock":"earliest", "topics":["ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"]],"id":1}')

# r = requests.post(url=secrets['MAIN_URL'], headers={"Content-Type": "application/json"}, data='{"jsonrpc":"2.0","method":"eth_getLogs","params":[{"blockHash": "0xa7dccc655f6a042a791005ccb27978627fba6542c82a66a347d44a9479d65f6c", "topics":["0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67"]}],"id":1}')
# print(r.status_code,r.text)



# Find the hash of the swap event 
k = keccak.new(digest_bits=256)
k.update(b'Swap(address,address,int256,int256,uint160,uint128,int24)')
topic_swap = "0x" + k.hexdigest()

print(topic_swap)






