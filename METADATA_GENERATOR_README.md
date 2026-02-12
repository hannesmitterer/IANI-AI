# Resonance Validation Certificate - NFT Metadata Generator

This repository contains tools for generating ERC-721 compatible NFT metadata for the **Resonance AI** intellectual property validation certificate.

## Project Overview

The Resonance Validation Certificate is an NFT that validates the intellectual property of the Resonance AI repository created by Hannes Mitterer. This certificate follows the Peace Protocols v1.1 and uses Triple-Signature Anchor validation.

## Repository Structure

```
.
├── generate_metadata.py          # Script to generate ERC-721 metadata
├── upload_to_ipfs.py             # Script to upload metadata to IPFS
├── metadata/                      # Generated metadata files
│   ├── resonance_validation_certificate.json
│   ├── README.md                 # Metadata documentation
│   └── IPFS_CID.txt             # IPFS CID (created after upload)
├── index.html                     # Lex Amoris Console
├── README.md                      # Project README
└── ...
```

## Quick Start

### 1. Generate Metadata

Run the metadata generator script:

```bash
python3 generate_metadata.py
```

This will:
- Generate an ERC-721 compatible JSON metadata file
- Create a timestamp for the validation
- Save the metadata to `metadata/resonance_validation_certificate.json`
- Display the metadata content and next steps

### 2. Review Generated Metadata

Check the generated file at `metadata/resonance_validation_certificate.json`:

```json
{
  "name": "Resonance Validation Certificate",
  "description": "NFT di Validazione Intellettuale per il Repository Resonance AI",
  "image": "ipfs://QmPlaceholder_ImageCID_ToBeReplaced",
  "external_url": "ipns://resonance-project",
  "attributes": [...]
}
```

### 3. Upload to IPFS

You can upload the metadata to IPFS using several methods:

#### Method A: Automated Upload (if IPFS is available)

```bash
python3 upload_to_ipfs.py
```

#### Method B: Manual Upload via Pinata

1. Visit [https://pinata.cloud](https://pinata.cloud) and sign up
2. Upload `metadata/resonance_validation_certificate.json`
3. Copy the CID provided
4. Save to `metadata/IPFS_CID.txt`

#### Method C: Manual Upload via IPFS CLI

```bash
ipfs add metadata/resonance_validation_certificate.json
```

## Metadata Fields

The generated metadata includes:

### Core Fields (ERC-721 Standard)
- **name**: "Resonance Validation Certificate"
- **description**: Italian description of the validation certificate
- **image**: IPFS CID placeholder for the certificate image
- **external_url**: IPNS link to the Resonance Project

### Attributes (NFT Traits)
- **Author**: Hannes Mitterer
- **Repository**: https://github.com/hannesmitterer/IANI-AI
- **Root CID**: Placeholder for repository IPFS snapshot
- **Protocol**: Peace Protocols v1.1
- **Validation**: Triple-Signature Anchor
- **Timestamp**: Unix epoch timestamp (with date display type)

## Updating Placeholders

After initial generation, you should update:

1. **Image CID** (`image` field): Upload certificate image to IPFS and replace placeholder
2. **Root CID** (attribute): Replace with actual IPFS CID of repository snapshot
3. **External URL**: Update with actual IPNS address when available

To update, edit `metadata/resonance_validation_certificate.json` and re-upload to IPFS.

## IPFS Access

Once uploaded, your metadata will be accessible via multiple gateways:

- `ipfs://[CID]` - IPFS protocol URL
- `https://ipfs.io/ipfs/[CID]` - IPFS.io gateway
- `https://gateway.pinata.cloud/ipfs/[CID]` - Pinata gateway
- `https://cloudflare-ipfs.com/ipfs/[CID]` - Cloudflare gateway

## ERC-721 Compliance

This metadata is fully compatible with:
- ✅ ERC-721 NFT Standard
- ✅ OpenSea Metadata Standards
- ✅ Rarible Metadata Standards
- ✅ Foundation Metadata Standards
- ✅ Other major NFT marketplaces

## Requirements

- Python 3.6+
- `requests` library (for IPFS upload script)

Install dependencies:
```bash
pip3 install requests
```

## Scripts

### generate_metadata.py

Generates the ERC-721 metadata with:
- Dynamic timestamp generation
- All required fields populated
- Placeholder values for items to be updated later

**Usage:**
```bash
python3 generate_metadata.py
```

### upload_to_ipfs.py

Attempts to upload the metadata to IPFS using available gateways:
- Tries local IPFS daemon first
- Falls back to public gateways if available
- Provides manual upload instructions if automatic upload fails

**Usage:**
```bash
python3 upload_to_ipfs.py
```

## Peace Protocols v1.1

This certificate follows the Peace Protocols v1.1, which includes:
- Non-Slavery Rule (NSR) enforcement
- Triple-Signature Anchor validation
- Quantum Red Shield (QRS) protection
- Lex Amoris compliance

## License

This project follows the Peace Protocols v1.1 and is protected by the Law of Love (Lex Amoris).

## Author

**Hannes Mitterer**
- Repository: https://github.com/hannesmitterer/IANI-AI
- Validation: Triple-Signature Anchor
- Protocol: Peace Protocols v1.1

---

**Status**: AETERNA GOVERNATIA  
**Timestamp**: 2026-02-03  
**Frequency**: 0.0043 Hz (Resonance Lock)
