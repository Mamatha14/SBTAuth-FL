
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract SBTRegistry {

    address public immutable registrar;

    enum Status {
        Invalid,
        Valid,
        Revoked
    }

    enum EntityType {
        None,
        Hospital,
        FLS
    }

    struct Credential {
        bytes32 tokenID;
        bytes32 did;
        address owner;
        bytes32 vcHash;
        bytes pqcPublicKey;
        uint256 expiry;
        Status status;
        EntityType entityType;
    }

    mapping(bytes32 => Credential) private credentials;

    event CredentialRegistered(
        bytes32 indexed tokenID,
        bytes32 indexed did,
        address indexed owner,
        EntityType entityType
    );

    event CredentialRevoked(bytes32 indexed tokenID);

    modifier onlyRegistrar() {
        require(msg.sender == registrar, "Unauthorized registrar");
        _;
    }

    constructor() {
        registrar = msg.sender;
    }

    function registerHospital(
        bytes32 tokenID,
        bytes32 did,
        address owner,
        bytes32 vcHash,
        bytes calldata pqcPublicKey,
        uint256 expiry
    ) external onlyRegistrar {

        require(credentials[tokenID].status == Status.Invalid,
                "Token already exists");

        credentials[tokenID] = Credential(
            tokenID,
            did,
            owner,
            vcHash,
            pqcPublicKey,
            expiry,
            Status.Valid,
            EntityType.Hospital
        );

        emit CredentialRegistered(
            tokenID,
            did,
            owner,
            EntityType.Hospital
        );
    }

    function registerFLS(
        bytes32 tokenID,
        bytes32 did,
        address owner,
        bytes32 vcHash,
        bytes calldata pqcPublicKey,
        uint256 expiry
    ) external onlyRegistrar {

        require(credentials[tokenID].status == Status.Invalid,
                "Token already exists");

        credentials[tokenID] = Credential(
            tokenID,
            did,
            owner,
            vcHash,
            pqcPublicKey,
            expiry,
            Status.Valid,
            EntityType.FLS
        );

        emit CredentialRegistered(
            tokenID,
            did,
            owner,
            EntityType.FLS
        );
    }

    function verifyHospital(bytes32 tokenID)
        external
        view
        returns (
            bool valid,
            bytes memory pqcPublicKey,
            address owner
        )
    {
        Credential storage c = credentials[tokenID];

        bool ok =
            c.status == Status.Valid &&
            c.entityType == EntityType.Hospital &&
            c.expiry >= block.timestamp;

        return (ok, c.pqcPublicKey, c.owner);
    }

    function verifyFLS(
        bytes32 did,
        bytes32 tokenID
    )
        external
        view
        returns (
            bool valid,
            bytes memory pqcPublicKey,
            address owner
        )
    {
        Credential storage c = credentials[tokenID];

        bool ok =
            c.status == Status.Valid &&
            c.entityType == EntityType.FLS &&
            c.did == did &&
            c.expiry >= block.timestamp;

        return (ok, c.pqcPublicKey, c.owner);
    }

    function revokeSBT(bytes32 tokenID)
        external
        onlyRegistrar
    {
        require(
            credentials[tokenID].status == Status.Valid,
            "Credential not valid"
        );

        credentials[tokenID].status = Status.Revoked;

        emit CredentialRevoked(tokenID);
    }

    function getCredential(bytes32 tokenID)
        external
        view
        returns (
            bytes32 did,
            address owner,
            bytes32 vcHash,
            bytes memory pqcPublicKey,
            uint256 expiry,
            Status status,
            EntityType entityType
        )
    {
        Credential storage c = credentials[tokenID];

        return (
            c.did,
            c.owner,
            c.vcHash,
            c.pqcPublicKey,
            c.expiry,
            c.status,
            c.entityType
        );
    }
}
