## Fruit Voting Contract

Contains simple fruit voting contract, that contains functions to vote and get winner, once voting has ended.

### Project Layout

`contract` - directory contains solidity contract. <br>
`voting_contract` - directory contains python client to interact with contract.<br>
`test` - directory contains test cases for contract code.


#### Compiling solidity code:
```
solc contracts/voting.sol  --bin --abi --optimize -o ./
```


#### Running tests
Don't forget to export `PYTHONPATH`:
```
export PYTHONPATH="${PYTHONPATH}:../"
```

now just run tests:
```
pytest
```
