import os

from web3 import Web3

from compile import compile
from consts import PUBLIC_ADDRESS, PRIVATE_ADDRESS

web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))


def deploy_contract():
    contract_location = "./contracts/voting.sol"
    compiled_sol = compile(contract_location)
    bytecode = compiled_sol["contracts"][contract_location]["FruitVotingContract"]["evm"]["bytecode"]["object"]
    abi = compiled_sol["contracts"][contract_location]["FruitVotingContract"]["abi"]

    fruit_contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    nonceA = web3.eth.get_transaction_count(PUBLIC_ADDRESS)

    transactionA = fruit_contract.constructor().build_transaction(
        {
            "gasPrice": web3.eth.gas_price,
            "chainId": 1337,
            "from": PUBLIC_ADDRESS,
            "nonce": nonceA
        }
    )

    signed_transaction = web3.eth.account.sign_transaction(
        transactionA, private_key=PRIVATE_ADDRESS
    )

    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    transaction_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

    return web3.eth.contract(abi=abi, address=transaction_receipt["contractAddress"])
