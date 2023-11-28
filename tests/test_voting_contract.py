from enum import Enum
from datetime import datetime, timedelta

import pytest
from brownie import FruitVotingContract
from brownie.exceptions import VirtualMachineError


class Fruit(Enum):
    APPLE = 0
    BANANA = 1
    WATERMELON = 2
    STRAWBERRY = 3


@pytest.fixture
def fruit_contract(FruitVotingContract, accounts):
    yield FruitVotingContract.deploy(accounts[-1], {"from": accounts[-1]})


def test_only_owner_can_change_auction_creation_date(fruit_contract, accounts):

    fruit_contract.setContractCreationTime(int(datetime.utcnow().timestamp()), {"from": accounts[-1]})

    with pytest.raises(VirtualMachineError) as e:
        fruit_contract.setContractCreationTime(int(datetime.utcnow().timestamp()), {"from": accounts[1]})


def test_account_cannot_make_more_than_one_vote(fruit_contract, accounts):
    fruit_contract.voteForFruit(Fruit.APPLE.value, {"from": accounts[-1]})

    assert fruit_contract.fruitVotes(Fruit.APPLE.value) == 1
    for fruit in Fruit:
        if fruit.value != Fruit.APPLE.value:
            assert fruit_contract.fruitVotes(fruit.value) == 0

    assert fruit_contract.votedAddresses(accounts[-1]) is True

    with pytest.raises(VirtualMachineError) as e:
        fruit_contract.voteForFruit(Fruit.APPLE.value, {"from": accounts[-1]})


def test_cannot_make_vote_when_it_is_ended(fruit_contract, accounts):
    new_timestamp = (datetime.utcnow() - timedelta(days=5)).timestamp()
    fruit_contract.setContractCreationTime(int(new_timestamp), {"from": accounts[-1]})

    with pytest.raises(VirtualMachineError) as e:
        fruit_contract.voteForFruit(Fruit.APPLE.value, {"from": accounts[-1]})


def test_cannot_get_winner_until_voting_is_ended(fruit_contract):
    with pytest.raises(VirtualMachineError) as e:
        fruit_contract.getWinner()


def test_correct_winner_is_calculated(fruit_contract, accounts):

    votes_for_fruits = {
        Fruit.APPLE: 2,
        Fruit.WATERMELON: 1,
        Fruit.BANANA: 3
    }

    account_idx = 1
    for fruit, num_votes in votes_for_fruits.items():
        for _ in range(num_votes):
            fruit_contract.voteForFruit(fruit.value, {"from": accounts[account_idx]})
            account_idx += 1

    new_timestamp = (datetime.utcnow() - timedelta(days=5)).timestamp()
    fruit_contract.setContractCreationTime(int(new_timestamp), {"from": accounts[-1]})

    assert fruit_contract.getWinner() == Fruit.BANANA.value
