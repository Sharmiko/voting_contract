from enum import Enum

import pytest
from web3.exceptions import ContractLogicError

from deploy import deploy_contract, public_address, web3


contract = deploy_contract()


class Fruit(Enum):
    APPLE = 0
    BANANA = 1
    WATERMELON = 2
    STRAWBERRY = 3


def test_contract_voting():

    tx_hash = contract.functions.voteForFruit(Fruit.APPLE.value).transact({
        "from": public_address
    })

    web3.eth.wait_for_transaction_receipt(tx_hash)

    assert contract.functions.fruitVotes(Fruit.APPLE.value).call() == 1
    for fruit in Fruit:
        if fruit.value != Fruit.APPLE.value:
            assert contract.functions.fruitVotes(fruit.value).call() == 0

    assert contract.functions.votedAddresses(public_address).call() is True

    with pytest.raises(ContractLogicError) as e:
        tx_hash = contract.functions.voteForFruit(Fruit.APPLE.value).transact({
            "from": public_address
        })

        web3.eth.wait_for_transaction_receipt(tx_hash)

    assert "Cannot make more than 1 vote" in str(e)
