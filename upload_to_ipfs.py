#!/usr/bin/env python3
"""
IPFS Uploader for Resonance Validation Certificate Metadata
Uses IPFS HTTP API to upload the metadata file to a public gateway.
"""

import json
import sys
import requests
from pathlib import Path

# Public IPFS gateways that accept uploads
IPFS_GATEWAYS = [
    {
        "name": "Local IPFS",
        "upload_url": "http://127.0.0.1:5001/api/v0/add",
        "gateway_url": "http://127.0.0.1:8080/ipfs/"
    },
    {
        "name": "Infura IPFS",
        "upload_url": "https://ipfs.infura.io:5001/api/v0/add",
        "gateway_url": "https://ipfs.io/ipfs/"
    }
]

def upload_to_ipfs(file_path, gateway_config):
    """
    Upload file to IPFS using HTTP API
    
    Args:
        file_path: Path to the file to upload
        gateway_config: Configuration dict for IPFS gateway
    
    Returns:
        dict: Upload result with CID and URLs
    """
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                gateway_config['upload_url'],
                files=files,
                timeout=30
            )
        
        if response.status_code == 200:
            result = response.json()
            cid = result.get('Hash')
            return {
                'success': True,
                'cid': cid,
                'gateway_name': gateway_config['name'],
                'ipfs_url': f"ipfs://{cid}",
                'http_url': f"{gateway_config['gateway_url']}{cid}"
            }
        else:
            return {
                'success': False,
                'error': f"HTTP {response.status_code}: {response.text}",
                'gateway_name': gateway_config['name']
            }
    
    except requests.exceptions.ConnectionError:
        return {
            'success': False,
            'error': 'Connection refused - gateway not available',
            'gateway_name': gateway_config['name']
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'gateway_name': gateway_config['name']
        }

def try_upload(file_path):
    """
    Try uploading to available IPFS gateways
    """
    print(f"\nAttempting to upload: {file_path}")
    print("="*60)
    
    for gateway in IPFS_GATEWAYS:
        print(f"\nTrying {gateway['name']}...")
        result = upload_to_ipfs(file_path, gateway)
        
        if result['success']:
            print(f"✓ Upload successful!")
            print(f"\nCID: {result['cid']}")
            print(f"IPFS URL: {result['ipfs_url']}")
            print(f"HTTP Gateway URL: {result['http_url']}")
            return result
        else:
            print(f"✗ Failed: {result['error']}")
    
    return None

def print_manual_instructions():
    """
    Print manual upload instructions
    """
    print("\n" + "="*60)
    print("MANUAL UPLOAD INSTRUCTIONS")
    print("="*60)
    print("\nSince automatic upload was not successful, please upload manually:")
    print("\nOption 1: Using IPFS CLI (if installed)")
    print("  ipfs add metadata/resonance_validation_certificate.json")
    print("\nOption 2: Using Pinata (https://pinata.cloud)")
    print("  1. Sign up for a free account")
    print("  2. Go to 'Upload' section")
    print("  3. Upload the metadata JSON file")
    print("  4. Copy the CID provided")
    print("\nOption 3: Using NFT.Storage (https://nft.storage)")
    print("  1. Sign up for a free account")
    print("  2. Go to 'Upload' section")
    print("  3. Upload the metadata JSON file")
    print("  4. Copy the CID provided")
    print("\nOption 4: Using Web3.Storage (https://web3.storage)")
    print("  1. Sign up for a free account")
    print("  2. Use their web interface to upload")
    print("  3. Copy the CID provided")
    print("="*60 + "\n")

def main():
    """
    Main execution function
    """
    metadata_file = Path("metadata/resonance_validation_certificate.json")
    
    if not metadata_file.exists():
        print(f"Error: Metadata file not found at {metadata_file}")
        print("Please run generate_metadata.py first")
        return 1
    
    # Try automatic upload
    result = try_upload(metadata_file)
    
    if result:
        print("\n" + "="*60)
        print("UPLOAD COMPLETE")
        print("="*60)
        print("\nSave these details:")
        print(f"CID: {result['cid']}")
        print(f"IPFS URL: {result['ipfs_url']}")
        print(f"HTTP Gateway: {result['http_url']}")
        print("\nYou can access your metadata at:")
        print(f"  https://ipfs.io/ipfs/{result['cid']}")
        print(f"  https://gateway.pinata.cloud/ipfs/{result['cid']}")
        print(f"  https://cloudflare-ipfs.com/ipfs/{result['cid']}")
        print("="*60 + "\n")
        
        # Save CID to a file for reference
        cid_file = Path("metadata/IPFS_CID.txt")
        with open(cid_file, 'w') as f:
            f.write(f"CID: {result['cid']}\n")
            f.write(f"IPFS URL: {result['ipfs_url']}\n")
            f.write(f"HTTP Gateway: {result['http_url']}\n")
        print(f"CID information saved to: {cid_file}\n")
        
        return 0
    else:
        print_manual_instructions()
        return 1

if __name__ == "__main__":
    sys.exit(main())
