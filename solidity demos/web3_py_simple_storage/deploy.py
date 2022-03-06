from wsgiref.handlers import SimpleHandler
from solcx import compile_standard, install_solc
import json
import os
from web3 import Web3
from dotenv import load_dotenv


load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)
#pipfile.close()
# solidity compile

install_solc("0.6.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

#get bytecode from the json
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]
#get abi

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

#for connecting to rinkeby

w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/a09214ad1d3f4c9883126699737e28c0"))
chain_id = 4
my_address = "0x8F59747e6461b90c7129475163f818302BA12406"

#bad practice to hard code private key... anyone can steal funds if public
private_key = os.getenv("PRIVATE_KEY")
#print(private_key)

#Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
#print(SimpleStorage)

#1. build transaction, 2. sign & 3. send transaction
#Get latest transaction with nonce
nonce = w3.eth.getTransactionCount(my_address)
#print(nonce)
transaction = SimpleStorage.constructor().buildTransaction( {
    "gasPrice": w3.eth.gas_price, 
    "chainId": chain_id, 
    "from": my_address, 
    "nonce": nonce, 
})
#2. signing
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
#print(signed_txn)
print("deploying contract...")
#3. sending signed
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

#working with contract on chain, you ALWAYS NEED:
# Contract Address
# Contract ABI

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

#Call -> simulate making the call and getting return value. Calls don't make a state change to BC
#Transact -> "orange buttons" actually make a state change

#initial value of fav number
print("Updating contract!")
store_transaction = simple_storage.functions.store(15).buildTransaction({
    "chainId":chain_id, "from":my_address, "nonce":nonce + 1,  "gasPrice": w3.eth.gas_price   
})

signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)

send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Contract updated")
print(simple_storage.functions.retrieve().call())