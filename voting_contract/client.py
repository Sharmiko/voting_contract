from voting_contract.choices import Fruit


class FruitContractClient:

    def __init__(self, contract_instance, web3):
        self.contract = contract_instance
        self.web3 = web3

    
    def vote_for_fruit(self, from_address: str, fruit: Fruit) -> None:
        tx_hash = self.contract.functions.voteForFruit(fruit.value).transact({
            "from": from_address
        })

        self.web3.eth.wait_for_transaction_receipt(tx_hash)


    def get_fruit_votes(self, fruit: Fruit) -> int:
        return self.contract.functions.fruitVotes(fruit.value).call()

    def account_already_voted(self, account: str) -> bool:
        return self.contract.functions.votedAddresses(account).call()

    def change_contract_creation_time(self, account: str, new_time: int):
        tx_hash = self.contract.functions.setContractCreationTime(new_time).transact({
            "from": account
        })

        self.web3.eth.wait_for_transaction_receipt(tx_hash)
