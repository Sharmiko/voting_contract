// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";


contract FruitVotingContract is Ownable {

    enum Fruit { NO_WINNER, APPLE, BANANA, WATERMELON, STRAWBERRY} 

    uint256 public contractCreationTime;
    uint256 public constant votingDuration = 3 days;
    mapping(Fruit => uint256) public fruitVotes;
    mapping(address => bool) public votedAddresses;

    constructor(address initialOwner) Ownable(initialOwner) {
        contractCreationTime = block.timestamp;
    }

    modifier isVotingTime() {
        require(block.timestamp < contractCreationTime + votingDuration, "Voting has ended.");
        _;
    }

    modifier votingEnded() {
        require(block.timestamp > contractCreationTime + votingDuration, "Voting has not ended");
        _;
    }

    modifier oneVotePerAddress() {
        require(!votedAddresses[msg.sender], "Cannot make more than 1 vote");
        _;
    }

    function setContractCreationTime(uint256 newTime) public onlyOwner {
        contractCreationTime = newTime;
    }

    function voteForFruit(Fruit fruit) public isVotingTime oneVotePerAddress {
        fruitVotes[fruit] += 1;
        votedAddresses[msg.sender] = true;
    }

    function getWinner() public votingEnded view returns (Fruit) {
        uint256 maxVote = 0;
        Fruit winningFruit = Fruit.NO_WINNER;

        for (uint8 i = 0; i < uint8(Fruit.STRAWBERRY) + 1; ++i) {
            Fruit _fruit = Fruit(i);
            if (fruitVotes[_fruit] > maxVote) {
                maxVote = fruitVotes[_fruit];
                winningFruit = _fruit;
            }
        }

        require(maxVote > 0, "No voting have been cast");

        return winningFruit;
    }
}