# Manual IPFS Upload Instructions

## Current Status

✅ **Metadata Generated**: `metadata/resonance_validation_certificate.json`
✅ **Validation Passed**: ERC-721 compliant
⏳ **Pending**: IPFS Upload

## Why Manual Upload?

The automated IPFS upload requires either:
- A local IPFS daemon running (not available in this environment)
- API keys for IPFS pinning services (requires account setup)

Therefore, the upload must be completed manually using one of the methods below.

## Recommended Upload Method: Pinata

### Step-by-Step Instructions

1. **Create Account**
   - Visit https://pinata.cloud
   - Click "Sign Up" (free tier available)
   - Verify your email

2. **Upload File**
   - Log in to your Pinata account
   - Click on "Files" in the left menu
   - Click "Upload" button
   - Select "File"
   - Choose: `/home/runner/work/IANI-AI/IANI-AI/metadata/resonance_validation_certificate.json`
   - (Optional) Add a name like "Resonance Validation Certificate Metadata"
   - Click "Upload"

3. **Get CID**
   - After upload completes, you'll see the file in your list
   - Copy the CID (Content Identifier) - it looks like: `QmXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx`

4. **Verify Upload**
   - Visit: `https://ipfs.io/ipfs/[YOUR_CID]`
   - You should see the JSON metadata displayed

5. **Save CID**
   - Update `metadata/IPFS_UPLOAD_INFO.txt` with:
     ```
     CID: [Your CID]
     IPFS URL: ipfs://[Your CID]
     HTTP Gateway: https://ipfs.io/ipfs/[Your CID]
     ```

## Alternative Method 1: NFT.Storage

1. Visit https://nft.storage
2. Sign up for free account
3. Go to "Files" section
4. Click "Upload"
5. Select the metadata JSON file
6. Copy the CID returned
7. Verify at: `https://nft.storage/ipfs/[CID]`

## Alternative Method 2: Web3.Storage

1. Visit https://web3.storage
2. Sign up for free account
3. Navigate to upload interface
4. Upload the metadata JSON file
5. Copy the CID
6. Verify at: `https://[CID].ipfs.w3s.link/`

## Alternative Method 3: IPFS Desktop

1. Download IPFS Desktop from https://docs.ipfs.tech/install/ipfs-desktop/
2. Install and launch IPFS Desktop
3. Drag and drop the metadata JSON file into IPFS Desktop
4. Copy the CID from the interface
5. The file is now available on the IPFS network

## What You'll Get

After uploading, you'll receive a CID that looks like:
```
QmXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXxXx
```

Your metadata will be accessible at:
- **IPFS Protocol**: `ipfs://QmXxX...`
- **IPFS.io Gateway**: `https://ipfs.io/ipfs/QmXxX...`
- **Pinata Gateway**: `https://gateway.pinata.cloud/ipfs/QmXxX...`
- **Cloudflare Gateway**: `https://cloudflare-ipfs.com/ipfs/QmXxX...`

## After Upload - Next Steps

1. **Document the CID**
   - Save CID to `metadata/IPFS_UPLOAD_INFO.txt`
   - Commit the update to the repository

2. **Optional: Update Placeholders**
   - Create and upload a certificate image
   - Update the `image` field with the image CID
   - Update the `Root CID` attribute with repository snapshot CID
   - Re-upload the updated metadata to get final CID

3. **Use in NFT Contract**
   - When minting the NFT, use the metadata CID
   - Most NFT platforms expect: `ipfs://[CID]` or just the CID

## Verification Checklist

After upload, verify:
- [ ] CID is accessible via HTTP gateway
- [ ] JSON displays correctly when accessed
- [ ] All metadata fields are present and correct
- [ ] CID is saved to IPFS_UPLOAD_INFO.txt
- [ ] Can access via multiple gateways

## Example CID Documentation

Once you have the CID, document it like this:

```
=== IPFS Upload Complete ===
CID: QmYourActualCIDHere123456789
IPFS URL: ipfs://QmYourActualCIDHere123456789
HTTP Gateway: https://ipfs.io/ipfs/QmYourActualCIDHere123456789
Upload Date: 2026-02-03
Service Used: Pinata
Status: Active and Pinned
```

## Troubleshooting

**Problem**: "Gateway timeout" when accessing
- Solution: Try a different gateway (IPFS.io, Pinata, Cloudflare)
- The file may need a few minutes to propagate

**Problem**: "File not found"
- Solution: Verify the CID is correct
- Check that the file was actually uploaded
- Try accessing via the service's own gateway first

**Problem**: "JSON not displaying correctly"
- Solution: Add `.json` extension or set proper content-type
- Some gateways auto-detect, others may need help

## Support

For IPFS-related questions:
- IPFS Documentation: https://docs.ipfs.tech
- Pinata Support: https://docs.pinata.cloud
- NFT.Storage Docs: https://nft.storage/docs

---

**File to Upload**: `metadata/resonance_validation_certificate.json`
**Expected Result**: A permanent, decentralized CID for your NFT metadata
**Next Action**: Choose a method above and upload the file
