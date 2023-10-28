import json

import solcx
from solcx import compile_standard
from semantic_version import Version


def compile(contract_location: str, solc_version: str = "0.8.21") -> dict:

    if Version(solc_version) not in solcx.get_installed_solc_versions():
        solcx.install_solc(solc_version)

    with open(contract_location, "r") as f:
        contract_file = f.read()

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {
                f"{contract_location}": {
                    "content": contract_file
                }
            },
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            }
        },
        solc_version=solc_version
    )

    return compiled_sol
