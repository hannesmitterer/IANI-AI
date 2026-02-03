# Resonance Validation Certificate - ERC-721 Metadata

This directory contains the ERC-721 compatible NFT metadata for the Resonance AI intellectual property validation certificate.

## Overview

The Resonance Validation Certificate is an NFT that represents the intellectual property validation for the **Resonance AI** repository, created by Hannes Mitterer.

## Files

- `resonance_validation_certificate.json` - The ERC-721 compatible metadata file
- `IPFS_CID.txt` - Contains the IPFS CID after upload (generated post-upload)

## Metadata Structure

The metadata follows the ERC-721 standard and includes:

```json
{
  "name": "Resonance Validation Certificate",
  "description": "NFT di Validazione Intellettuale per il Repository Resonance AI",
  "image": "ipfs://QmPlaceholder_ImageCID_ToBeReplaced",
  "external_url": "ipns://resonance-project",
  "attributes": [
    {
      "trait_type": "Author",
      "value": "Hannes Mitterer"
    },
    {
      "trait_type": "Repository",
      "value": "https://github.com/hannesmitterer/IANI-AI"
    },
    {
      "trait_type": "Root CID",
      "value": "QmResonanceHannesMitterer2026..."
    },
    {
      "trait_type": "Protocol",
      "value": "Peace Protocols v1.1"
    },
    {
      "trait_type": "Validation",
      "value": "Triple-Signature Anchor"
    },
    {
      "trait_type": "Timestamp",
      "value": 1770135145,
      "display_type": "date"
    }
  ]
}
```

## Attributes Explained

- **Author**: The creator of the Resonance AI project (Hannes Mitterer)
- **Repository**: The GitHub repository URL for IANI-AI
- **Root CID**: Placeholder for the IPFS CID of the repository snapshot (to be updated with actual CID)
- **Protocol**: The Peace Protocols version used for validation (v1.1)
- **Validation**: The validation method used (Triple-Signature Anchor)
- **Timestamp**: Unix epoch timestamp when the metadata was created

## Uploading to IPFS

### Option 1: Using IPFS CLI

If you have IPFS installed locally:

```bash
ipfs add resonance_validation_certificate.json
```

This will output a CID (Content Identifier) like:
```
added QmXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx resonance_validation_certificate.json
```

### Option 2: Using Pinata (Recommended)

1. Sign up for a free account at [https://pinata.cloud](https://pinata.cloud)
2. Go to the "Upload" section
3. Click "Upload File" and select `resonance_validation_certificate.json`
4. Copy the CID provided after upload
5. Save the CID to `IPFS_CID.txt`

### Option 3: Using NFT.Storage

1. Sign up for a free account at [https://nft.storage](https://nft.storage)
2. Navigate to the "Files" section
3. Click "Upload" and select `resonance_validation_certificate.json`
4. Copy the CID provided
5. Save the CID to `IPFS_CID.txt`

### Option 4: Using Web3.Storage

1. Sign up at [https://web3.storage](https://web3.storage)
2. Use their web interface to upload the file
3. Copy the CID provided
4. Save the CID to `IPFS_CID.txt`

## After Upload

Once uploaded to IPFS, the metadata will be accessible via:

- IPFS Protocol: `ipfs://[YOUR_CID]`
- HTTP Gateway: `https://ipfs.io/ipfs/[YOUR_CID]`
- Pinata Gateway: `https://gateway.pinata.cloud/ipfs/[YOUR_CID]`
- Cloudflare Gateway: `https://cloudflare-ipfs.com/ipfs/[YOUR_CID]`

## Updating Placeholders

After uploading:

1. **Image CID**: Once you have an image for the certificate, upload it to IPFS and update the `image` field with the actual CID
2. **Root CID**: Update the "Root CID" attribute with the actual IPFS CID of the repository snapshot
3. Re-upload the updated metadata to IPFS to get a new CID

## ERC-721 Compatibility

This metadata file is fully compatible with:
- ERC-721 NFT standard
- OpenSea metadata standards
- Rarible metadata standards
- Other NFT marketplaces that support ERC-721

## License

This metadata represents intellectual property of the Resonance AI project and follows the Peace Protocols v1.1.

---

**Generated**: 2026-02-03  
**Protocol**: Peace Protocols v1.1  
**Validation**: Triple-Signature Anchor
