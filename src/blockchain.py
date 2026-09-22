from pathlib import Path

from web3 import Web3
from solcx import (
    compile_standard,
    install_solc
)


SOLC_VERSION = "0.8.24"


def create_test_blockchain():
    """
    Create the local EVM blockchain used in the PoC.

    EthereumTesterProvider is used only to emulate the
    permissioned consortium blockchain behavior required
    by the prototype.
    """
    from web3.providers.eth_tester import (
        EthereumTesterProvider
    )

    w3 = Web3(
        EthereumTesterProvider()
    )

    if not w3.is_connected():
        raise RuntimeError(
            "EthereumTesterProvider connection failed."
        )

    return w3


def compile_contract(
    contract_path,
    solc_version=SOLC_VERSION
):
    install_solc(solc_version)

    contract_path = Path(contract_path)

    source = contract_path.read_text()

    compiled = compile_standard(
        {
            "language": "Solidity",
            "sources": {
                contract_path.name: {
                    "content": source
                }
            },
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": [
                            "abi",
                            "evm.bytecode"
                        ]
                    }
                }
            }
        },
        solc_version=solc_version
    )

    contract_data = (
        compiled[
            "contracts"
        ][
            contract_path.name
        ][
            "SBTRegistry"
        ]
    )

    abi = contract_data["abi"]

    bytecode = (
        contract_data[
            "evm"
        ][
            "bytecode"
        ][
            "object"
        ]
    )

    return abi, bytecode


def deploy_registry(
    w3,
    contract_path
):
    abi, bytecode = compile_contract(
        contract_path
    )

    registrar = w3.eth.accounts[0]

    Contract = w3.eth.contract(
        abi=abi,
        bytecode=bytecode
    )

    tx_hash = Contract.constructor().transact(
        {
            "from": registrar
        }
    )

    receipt = (
        w3.eth.wait_for_transaction_receipt(
            tx_hash
        )
    )

    contract = w3.eth.contract(
        address=receipt.contractAddress,
        abi=abi
    )

    return contract, registrar, receipt
