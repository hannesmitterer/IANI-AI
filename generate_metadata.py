#!/usr/bin/env python3
"""
ERC-721 Metadata Generator for Resonance Validation Certificate
This script generates NFT metadata for the intellectual property validation certificate.
"""

import json
import time
import sys
from datetime import datetime
from pathlib import Path

def generate_metadata():
    """
    Generate ERC-721 compatible JSON metadata for Resonance Validation Certificate
    """
    # Get current epoch timestamp
    timestamp = int(time.time())
    
    # Create metadata structure
    metadata = {
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
                "value": timestamp,
                "display_type": "date"
            }
        ]
    }
    
    return metadata, timestamp

def save_metadata(metadata, output_path="metadata"):
    """
    Save metadata to JSON file
    """
    # Create metadata directory if it doesn't exist
    metadata_dir = Path(output_path)
    metadata_dir.mkdir(exist_ok=True)
    
    # Save the metadata
    metadata_file = metadata_dir / "resonance_validation_certificate.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    return metadata_file

def print_metadata_info(metadata, metadata_file, timestamp):
    """
    Print information about the generated metadata
    """
    print("\n" + "="*60)
    print("ERC-721 METADATA GENERATED SUCCESSFULLY")
    print("="*60)
    print(f"\nFile Location: {metadata_file}")
    print(f"Timestamp (Epoch): {timestamp}")
    print(f"Timestamp (Human): {datetime.fromtimestamp(timestamp).isoformat()}")
    print("\nMetadata Content:")
    print("-"*60)
    print(json.dumps(metadata, indent=2, ensure_ascii=False))
    print("-"*60)
    print("\nNext Steps:")
    print("1. Review the metadata file")
    print("2. Upload the metadata JSON to IPFS")
    print("3. Note the CID returned by IPFS")
    print("4. Update the 'image' field with actual image CID when available")
    print("5. Update the 'Root CID' attribute with actual repository CID")
    print("\nIPFS Upload Commands:")
    print(f"  ipfs add {metadata_file}")
    print("  OR use a pinning service like Pinata, NFT.Storage, or Web3.Storage")
    print("="*60 + "\n")

def main():
    """
    Main execution function
    """
    try:
        # Generate metadata
        metadata, timestamp = generate_metadata()
        
        # Save to file
        metadata_file = save_metadata(metadata)
        
        # Print information
        print_metadata_info(metadata, metadata_file, timestamp)
        
        return 0
    
    except Exception as e:
        print(f"Error generating metadata: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
