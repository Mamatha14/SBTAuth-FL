import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.blockchain import (
    create_test_blockchain,
    deploy_registry
)

from src.registration import (
    generate_ra_secret,
    create_hospital_identity,
    create_fls_identity,
    register_hospital,
    register_fls
)

from src.authentication import authenticate


def main():

    contract_path = (
        ROOT
        / "contracts"
        / "SBTRegistry.sol"
    )

    w3 = create_test_blockchain()

    contract, registrar, _ = (
        deploy_registry(
            w3,
            contract_path
        )
    )

    x_ra = generate_ra_secret()

    hospital = create_hospital_identity(
        "Hospital-A",
        x_ra
    )

    fls = create_fls_identity(
        "Federated-Learning-Server",
        x_ra
    )

    tx_h = register_hospital(
        contract,
        registrar,
        hospital
    )

    w3.eth.wait_for_transaction_receipt(
        tx_h
    )

    tx_f = register_fls(
        contract,
        registrar,
        fls
    )

    w3.eth.wait_for_transaction_receipt(
        tx_f
    )

    success, sk_h, sk_f = authenticate(
        contract,
        hospital,
        fls
    )

    assert success
    assert sk_h == sk_f

    print(
        "SBTAuth-FL protocol smoke test: PASS"
    )


if __name__ == "__main__":
    main()
