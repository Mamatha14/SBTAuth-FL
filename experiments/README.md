# SBTAuth-FL Experiments

The complete evaluated experiment workflow is provided in:

`../SBTAuth_FL_PoC.ipynb`

The notebook is the canonical executable artifact used to generate the
reported experimental results.

## Experiments

### Cryptographic Benchmark
Measures ML-DSA-44 key generation, signing and verification, ECDH
operations, and SHA-256 transcript hashing.

Output:

`../results/crypto_benchmark.csv`

### Authentication Latency
Measures the end-to-end two-message SBTAuth-FL authentication protocol,
including smart-contract verification, ML-DSA signature verification,
ECDH, and session-key establishment.

Output:

`../results/authentication_latency.csv`

### Communication Overhead
Measures the actual serialized field sizes of protocol messages M1 and M2,
including ML-DSA-44 signatures.

Output:

`../results/communication_overhead.csv`

### Blockchain Overhead
Measures smart-contract registration, verification, and revocation
latencies and transaction gas where applicable.

Output:

`../results/blockchain_overhead.csv`

### Authentication Scalability
Measures authentication latency as the number of participating clients
increases.

Outputs:

`../results/authentication_scalability.csv`

`../results/authentication_scalability.pdf`

### Blockchain Scalability
Measures smart-contract credential-verification behavior as the number
of registered credentials increases.

Outputs:

`../results/blockchain_scalability.csv`

`../results/blockchain_scalability.pdf`

### Security Attack Validation
Evaluates implemented attack cases including hospital impersonation,
FLS impersonation, transcript tampering, replay, and invalid SBT TokenID.

Output:

`../results/security_attack_results.csv`

### Session-Key Consistency
Repeatedly verifies that the hospital and FLS independently derive the
same ECDH shared secret and final session key.

Output:

`../results/session_key_consistency.csv`

### Storage Overhead
Reports the logical credential payload sizes used by the PoC.

Output:

`../results/storage_overhead.csv`

### Federated Learning Experiment
Runs authenticated federated learning using MNIST and FedAvg.

Output:

`../results/fl_results.csv`

## Important

The security attack experiments constitute implementation-level validation
of the tested attack cases. They are not a substitute for formal
cryptographic security analysis.

The local EthereumTesterProvider deployment emulates the blockchain
functionality required by the proof of concept; it should not be
interpreted as a performance model of a production consortium network.
