from src.crypto_utils import (
    H,
    random_nonce,
    generate_ecdh_keypair,
    ecdh_shared_secret,
    pqc_sign,
    pqc_verify
)


def authenticate(
    contract,
    hospital,
    fls,
    replay_cache=None
):
    """
    Execute one complete SBTAuth-FL mutual
    authentication session.

    Returns:
        success,
        hospital_session_key,
        fls_session_key
    """

    if replay_cache is None:
        replay_cache = set()

    # ==================================================
    # Step 1: Hospital creates ephemeral session values
    # ==================================================

    a_private, X_i = generate_ecdh_keypair()

    N1 = random_nonce()

    SPID_i = H(
        hospital["PID"],
        N1
    )

    # ==================================================
    # Step 2: Hospital creates M1 and ML-DSA signature
    # ==================================================

    M1 = H(
        SPID_i,
        hospital["TokenID"],
        X_i,
        N1
    )

    sigma_i = pqc_sign(
        hospital["sk"],
        M1
    )

    # ==================================================
    # Step 3: FLS verifies SBT and hospital signature
    # ==================================================

    valid_hospital, registered_pk_i, _ = (
        contract.functions.verifyHospital(
            hospital["TokenID"]
        ).call()
    )

    if not valid_hospital:
        return False, None, None

    if N1.hex() in replay_cache:
        return False, None, None

    if not pqc_verify(
        registered_pk_i,
        M1,
        sigma_i
    ):
        return False, None, None

    replay_cache.add(
        N1.hex()
    )

    # ==================================================
    # Step 4: FLS creates its ephemeral values
    # ==================================================

    b_private, Y_F = generate_ecdh_keypair()

    N2 = random_nonce()

    K_F = ecdh_shared_secret(
        b_private,
        X_i
    )

    # ==================================================
    # Step 5: FLS generates M2
    # ==================================================

    M2 = H(
        fls["DID"],
        fls["TokenID"],
        SPID_i,
        X_i,
        Y_F,
        N1,
        N2
    )

    sigma_F = pqc_sign(
        fls["sk"],
        M2
    )

    # ==================================================
    # Step 6: Hospital verifies FLS SBT
    # ==================================================

    valid_fls, registered_pk_f, _ = (
        contract.functions.verifyFLS(
            fls["DID"],
            fls["TokenID"]
        ).call()
    )

    if not valid_fls:
        return False, None, None

    expected_M2 = H(
        fls["DID"],
        fls["TokenID"],
        SPID_i,
        X_i,
        Y_F,
        N1,
        N2
    )

    if expected_M2 != M2:
        return False, None, None

    if not pqc_verify(
        registered_pk_f,
        M2,
        sigma_F
    ):
        return False, None, None

    # ==================================================
    # Step 7: Hospital derives ECDH shared secret
    # ==================================================

    K_i = ecdh_shared_secret(
        a_private,
        Y_F
    )

    # ==================================================
    # Step 8: Both sides derive session key
    # ==================================================

    SK_i = H(
        K_i,
        SPID_i,
        hospital["TokenID"],
        fls["TokenID"],
        X_i,
        Y_F,
        N1,
        N2
    )

    SK_F = H(
        K_F,
        SPID_i,
        hospital["TokenID"],
        fls["TokenID"],
        X_i,
        Y_F,
        N1,
        N2
    )

    success = (
        SK_i == SK_F
    )

    return success, SK_i, SK_F
