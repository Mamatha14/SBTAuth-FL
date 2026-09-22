from hashlib import sha256
import secrets

from pqcrypto.sign.ml_dsa_44 import (
    keygen as mldsa_keygen,
    sign as mldsa_sign,
    verify as mldsa_verify
)

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization


def to_bytes(value):
    if isinstance(value, bytes):
        return value

    if isinstance(value, str):
        return value.encode()

    if isinstance(value, int):
        return value.to_bytes(
            max(1, (value.bit_length() + 7) // 8),
            "big"
        )

    raise TypeError(
        f"Unsupported value type: {type(value)}"
    )


def H(*values):
    """
    SHA-256 transcript hash using explicit length separation.
    """
    encoded = b""

    for value in values:
        value = to_bytes(value)

        encoded += (
            len(value).to_bytes(4, "big")
            + value
        )

    return sha256(encoded).digest()


def random_nonce(size=32):
    return secrets.token_bytes(size)


def random_token_id():
    return secrets.token_bytes(32)


def generate_pqc_keypair():
    """
    Generate an ML-DSA-44 signing key pair.
    """
    return mldsa_keygen()


def pqc_sign(secret_key, message):
    return mldsa_sign(
        secret_key,
        message
    )


def pqc_verify(public_key, message, signature):
    try:
        result = mldsa_verify(
            public_key,
            message,
            signature
        )

        return (
            result is None
            or result is True
        )

    except Exception:
        return False


def generate_ecdh_keypair():
    """
    Generate ephemeral P-256 ECDH key pair.
    """
    private_key = ec.generate_private_key(
        ec.SECP256R1()
    )

    public_bytes = (
        private_key.public_key()
        .public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
    )

    return private_key, public_bytes


def ecdh_shared_secret(
    private_key,
    peer_public_bytes
):
    peer_public_key = (
        ec.EllipticCurvePublicKey
        .from_encoded_point(
            ec.SECP256R1(),
            peer_public_bytes
        )
    )

    return private_key.exchange(
        ec.ECDH(),
        peer_public_key
    )
