# Quick Reference: Resonance Validation Certificate NFT

## 📋 Quick Commands

### Generate Metadata
```bash
python3 generate_metadata.py
```

### Validate Metadata
```bash
python3 validate_metadata.py
```

### Upload to IPFS (Automatic)
```bash
python3 upload_to_ipfs.py
```

## 📁 Key Files

| File | Description |
|------|-------------|
| `metadata/resonance_validation_certificate.json` | The ERC-721 metadata file |
| `generate_metadata.py` | Metadata generator script |
| `upload_to_ipfs.py` | IPFS upload helper |
| `validate_metadata.py` | Metadata validator |

## 🔗 IPFS Upload Options

### Option 1: Pinata (Recommended)
1. Go to https://pinata.cloud
2. Upload `resonance_validation_certificate.json`
3. Copy the CID

### Option 2: NFT.Storage
1. Go to https://nft.storage
2. Upload the file
3. Copy the CID

### Option 3: Web3.Storage
1. Go to https://web3.storage
2. Upload the file
3. Copy the CID

### Option 4: IPFS CLI
```bash
ipfs add metadata/resonance_validation_certificate.json
```

## 📊 Metadata Summary

- **Name**: Resonance Validation Certificate
- **Author**: Hannes Mitterer
- **Repository**: https://github.com/hannesmitterer/IANI-AI
- **Protocol**: Peace Protocols v1.1
- **Validation**: Triple-Signature Anchor
- **Timestamp**: 1770135145 (2026-02-03T16:12:25)

## ✅ Validation Status

```
✓ Valid JSON format
✓ All required ERC-721 fields present
✓ Attributes properly structured
✓ IPFS URLs correctly formatted
✓ Compatible with major NFT marketplaces
```

## 🔄 Update Workflow

1. Edit `metadata/resonance_validation_certificate.json`
2. Update placeholder values:
   - `image`: Replace with actual image CID
   - `Root CID` attribute: Replace with repository CID
3. Run validator: `python3 validate_metadata.py`
4. Re-upload to IPFS
5. Save new CID to `metadata/IPFS_UPLOAD_INFO.txt`

## 📖 Full Documentation

- **Main README**: `METADATA_GENERATOR_README.md`
- **Metadata Docs**: `metadata/README.md`
- **Implementation Summary**: `IMPLEMENTATION_SUMMARY.md`

## 🌐 Access Your Metadata

Once uploaded, access via:
- `ipfs://[CID]`
- `https://ipfs.io/ipfs/[CID]`
- `https://gateway.pinata.cloud/ipfs/[CID]`
- `https://cloudflare-ipfs.com/ipfs/[CID]`

---
**Status**: Ready for IPFS upload 🚀
