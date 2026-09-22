import json
import secrets
import time

from eth_account import Account

from src.crypto_utils import (
    H,
    random_token_id,
    generate_pqc_keypair
)


def vc_to_bytes(vc):
    """
    Canonical JSON serialization used before hashing
    the demonstrator Verifiable Credential.
    """
    return json.dumps(
        vc,
        sort_keys=True,
        separators=(",", ":")
    ).encode()


def create_hospital_identity(
    hospital_id,
    x_ra,
    role="Healthcare Provider",
    access_level="FL Participant",
    expiry=None
):
    if expiry is None:
        expiry = int(time.time()) + 86400

    pk, sk = generate_pqc_keypair()

    owner_account = Account.create()
    owner = owner_account.address

    did = H(
        hospital_id,
        x_ra
    )

    pid = H(
        did,
        x_ra
    )

    vc = {
        "PID": pid.hex(),
        "Role": role,
        "Hospital": hospital_id,
        "AccessLevel": access_level,
        "Expiry": expiry
    }

    vc_bytes = vc_to_bytes(vc)
    vc_hash = H(vc_bytes)

    token_id = random_token_id()

    return {
        "ID": hospital_id,
        "pk": pk,
        "sk": sk,
        "Owner": owner,
        "DID": did,
        "PID": pid,
        "VC": vc,
        "VC_bytes": vc_bytes,
        "VC_hash": vc_hash,
        "TokenID": token_id,
        "expiry": expiry
    }


def create_fls_identity(
    fls_id,
    x_ra,
    expiry=None
):
    if expiry is None:
        expiry = int(time.time()) + 86400

    pk, sk = generate_pqc_keypair()

    owner_account = Account.create()
    owner = owner_account.address

    did = H(
        fls_id,
        x_ra
    )

    vc = {
        "DID": did.hex(),
        "Role": "Federated Learning Server",
        "AccessLevel": "FL Coordinator",
        "Expiry": expiry
    }

    vc_bytes = vc_to_bytes(vc)
    vc_hash = H(vc_bytes)

    token_id = random_token_id()

    return {
        "ID": fls_id,
        "pk": pk,
        "sk": sk,
        "Owner": owner,
        "DID": did,
        "VC": vc,
        "VC_bytes": vc_bytes,
        "VC_hash": vc_hash,
        "TokenID": token_id,
        "expiry": expiry
    }


def register_hospital(
    contract,
    registrar,
    hospital
):
    tx = contract.functions.registerHospital(
        hospital["TokenID"],
        hospital["DID"],
        hospital["Owner"],
        hospital["VC_hash"],
        hospital["pk"],
        hospital["expiry"]
    ).transact(
        {
            "from": registrar
        }
    )

    return tx


def register_fls(
    contract,
    registrar,
    fls
):
    tx = contract.functions.registerFLS(
        fls["TokenID"],
        fls["DID"],
        fls["Owner"],
        fls["VC_hash"],
        fls["pk"],
        fls["expiry"]
    ).transact(
        {
            "from": registrar
        }
    )

    return tx


def generate_ra_secret():
    return secrets.token_bytes(32)
