from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
import requests
import json
import time

bayc_address = "0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D"
contract_address = Web3.to_checksum_address(bayc_address)

#You will need the ABI to connect to the contract
#The file 'abi.json' has the ABI for the bored ape contract
#In general, you can get contract ABIs from etherscan
#https://api.etherscan.io/api?module=contract&action=getabi&address=0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D
with open('/home/codio/workspace/abi.json', 'r') as f:
	abi = json.load(f) 

############################
#Connect to an Ethereum node
api_url = "https://mainnet.infura.io/v3/1ca518b0b5c2414ca764e1d1dba11465" #YOU WILL NEED TO TO PROVIDE THE URL OF AN ETHEREUM NODE
provider = HTTPProvider(api_url)
web3 = Web3(provider)

contract = web3.eth.contract(address=contract_address, abi=abi)

	#YOUR CODE HERE	

def get_ape_info(apeID):
    assert isinstance(apeID, int), f"{apeID} is not an int"
    assert 1 <= apeID <= 10000, f"{apeID} must be between 1 and 10,000"

    data = {'owner': "", 'image': "", 'eyes': ""}

    owner = contract.functions.ownerOf(apeID).call()
    token_uri = contract.functions.tokenURI(apeID).call()

    ipfs_gateway = "https://gateway.pinata.cloud/ipfs/"
    ipfs_hash = token_uri.split("ipfs://")[1]
    metadata_url = ipfs_gateway + ipfs_hash

    response = requests.get(metadata_url)
    metadata = response.json()

    image_uri = metadata["image"]
    eyes = next(attr["value"] for attr in metadata["attributes"] if attr["trait_type"] == "Eyes")

    data['owner'] = owner
    data['image'] = image_uri
    data['eyes'] = eyes

    assert isinstance(data, dict), f'get_ape_info({apeID}) should return a dict'
    assert all([a in data.keys() for a in ['owner', 'image', 'eyes']]), f"return value should include the keys 'owner','image' and 'eyes'"
    
    return data
