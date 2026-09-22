# SBTAuth-FL

Proof-of-concept implementation and experimental artifact for:

**SBTAuth-FL: A Blockchain-Assisted Anonymous Authentication Protocol Using Soulbound Tokens for Secure Healthcare Federated Learning**

## Overview

SBTAuth-FL provides blockchain-assisted authentication for healthcare
federated learning participants using non-transferable Soulbound Token
(SBT) credential bindings.

The proof of concept integrates:

- Solidity smart contracts
- Web3.py
- EthereumTesterProvider
- ML-DSA-44 digital signatures
- P-256 ephemeral ECDH
- SHA-256 transcript hashing
- PyTorch federated learning
- MNIST
- FedAvg

ML-DSA-44 is used for entity authentication. The current prototype uses
classical P-256 ECDH for session-key establishment and therefore does not
claim full post-quantum key establishment.

## Architecture

A trusted Registration Authority (RA) is used only during initial entity
registration.

For each authorized hospital, the smart contract records the SBT
credential binding, including:

- TokenID
- DID
- registered blockchain owner address
- hash of the Verifiable Credential
- ML-DSA public key
- validity status
- expiry information

The full Verifiable Credential is maintained off-chain.

During routine authentication, the RA is not contacted.

The hospital and Federated Learning Server perform a two-message mutual
authentication protocol. Each party verifies the counterparty's
blockchain-registered credential and ML-DSA signature before deriving an
ECDH shared secret and session key.

## Repository Structure

```text
SBTAuth-FL/
├── SBTAuth_FL_PoC.ipynb
├── README.md
├── requirements.txt
├── environment.txt
├── contracts/
│   └── SBTRegistry.sol
├── src/
│   ├── __init__.py
│   ├── crypto_utils.py
│   ├── blockchain.py
│   ├── registration.py
│   └── authentication.py
├── experiments/
│   ├── README.md
│   └── protocol_smoke_test.py
└── results/
