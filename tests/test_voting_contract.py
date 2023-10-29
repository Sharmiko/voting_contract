from enum import Enum
from datetime import datetime, timedelta

import pytest
from web3.exceptions import ContractLogicError

from deploy import deploy_contract, PUBLIC_ADDRESS, web3
from voting_contract.client import FruitContractClient
from voting_contract.choices import Fruit


def test_only_owner_can_change_auction_creation_date():
    client = FruitContractClient(deploy_contract(), web3)
    client.change_contract_creation_time(PUBLIC_ADDRESS, int(datetime.utcnow().timestamp()))

    with pytest.raises(ContractLogicError) as e:
        client.change_contract_creation_time(web3.eth.accounts[1], int(datetime.utcnow().timestamp()))

    assert "Only owner can perform this action" in str(e)


def test_account_cannot_make_more_than_one_vote():
    client = FruitContractClient(deploy_contract(), web3)

    client.vote_for_fruit(PUBLIC_ADDRESS, Fruit.APPLE)

    assert client.get_fruit_votes(Fruit.APPLE) == 1
    for fruit in Fruit:
        if fruit.value != Fruit.APPLE.value:
            assert client.get_fruit_votes(fruit) == 0

    assert client.account_already_voted(PUBLIC_ADDRESS) is True

    with pytest.raises(ContractLogicError) as e:
        client.vote_for_fruit(PUBLIC_ADDRESS, Fruit.APPLE)

    assert "Cannot make more than 1 vote" in str(e)


def test_cannot_make_vote_when_it_is_ended():
    client = FruitContractClient(deploy_contract(), web3)

    new_timestamp = (datetime.utcnow() - timedelta(days=5)).timestamp()
    client.change_contract_creation_time(PUBLIC_ADDRESS, int(new_timestamp))

    with pytest.raises(ContractLogicError) as e:
        client.vote_for_fruit(PUBLIC_ADDRESS, Fruit.APPLE)

    assert "Voting has ended." in str(e)


def test_cannot_get_winner_until_voting_is_ended():
    client = FruitContractClient(deploy_contract(), web3)

    with pytest.raises(ValueError) as e:
        client.get_winner()

    assert "Voting has not ended" in str(e)


def test_correct_winner_is_calculated():
    client = FruitContractClient(deploy_contract(), web3)

    votes_for_fruits = {
        Fruit.APPLE: 2,
        Fruit.WATERMELON: 1,
        Fruit.BANANA: 3
    }

    account_idx = 1
    for fruit, num_votes in votes_for_fruits.items():
        for _ in range(num_votes):
            client.vote_for_fruit(web3.eth.accounts[account_idx], fruit)
            account_idx += 1

    new_timestamp = (datetime.utcnow() - timedelta(days=5)).timestamp()
    client.change_contract_creation_time(PUBLIC_ADDRESS, int(new_timestamp))

    assert client.get_winner() == Fruit.BANANA.value
