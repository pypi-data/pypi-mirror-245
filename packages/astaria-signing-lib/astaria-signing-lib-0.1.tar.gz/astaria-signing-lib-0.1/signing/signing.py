from web3 import Web3
from eth_account.messages import encode_defunct

def sign_message(encoded_data, private_key):
    signable_message = encode_defunct(encoded_data)
    signed_message = Web3().eth.account.sign_message(signable_message, private_key=private_key)
    return signed_message