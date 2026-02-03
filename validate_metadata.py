#!/usr/bin/env python3
"""
Test script to validate the ERC-721 metadata format
"""

import json
import sys
from pathlib import Path

def validate_metadata(metadata_path):
    """
    Validate that the metadata follows ERC-721 standards
    """
    print("="*60)
    print("ERC-721 METADATA VALIDATION")
    print("="*60)
    
    # Load the metadata
    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        print(f"✓ Valid JSON format")
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON: {e}")
        return False
    except FileNotFoundError:
        print(f"✗ File not found: {metadata_path}")
        return False
    
    # Check required ERC-721 fields
    required_fields = ['name', 'description', 'image']
    optional_fields = ['external_url', 'attributes', 'background_color']
    
    all_valid = True
    
    print("\nRequired Fields:")
    for field in required_fields:
        if field in metadata:
            print(f"  ✓ {field}: Present")
            if not metadata[field]:
                print(f"    ⚠ Warning: {field} is empty")
        else:
            print(f"  ✗ {field}: Missing")
            all_valid = False
    
    print("\nOptional Fields:")
    for field in optional_fields:
        if field in metadata:
            print(f"  ✓ {field}: Present")
    
    # Validate attributes structure
    if 'attributes' in metadata:
        print("\nAttributes Validation:")
        if isinstance(metadata['attributes'], list):
            print(f"  ✓ Attributes is an array ({len(metadata['attributes'])} items)")
            
            for i, attr in enumerate(metadata['attributes']):
                if isinstance(attr, dict):
                    if 'trait_type' in attr and 'value' in attr:
                        print(f"  ✓ Attribute {i+1}: {attr['trait_type']} = {attr['value']}")
                    else:
                        print(f"  ✗ Attribute {i+1}: Missing trait_type or value")
                        all_valid = False
                else:
                    print(f"  ✗ Attribute {i+1}: Not a dictionary")
                    all_valid = False
        else:
            print("  ✗ Attributes is not an array")
            all_valid = False
    
    # Check for IPFS/IPNS URLs
    print("\nIPFS/IPNS URL Validation:")
    if metadata.get('image', '').startswith('ipfs://'):
        print(f"  ✓ Image uses IPFS protocol")
    else:
        print(f"  ⚠ Image does not use IPFS protocol (using: {metadata.get('image', 'N/A')})")
    
    if metadata.get('external_url', '').startswith(('ipfs://', 'ipns://', 'https://')):
        print(f"  ✓ External URL uses valid protocol")
    else:
        print(f"  ⚠ External URL protocol: {metadata.get('external_url', 'N/A')}")
    
    # Summary
    print("\n" + "="*60)
    if all_valid:
        print("VALIDATION RESULT: ✓ PASSED")
        print("The metadata is valid ERC-721 format!")
    else:
        print("VALIDATION RESULT: ✗ FAILED")
        print("The metadata has validation errors.")
    print("="*60 + "\n")
    
    return all_valid

def main():
    """
    Main function
    """
    metadata_file = Path("metadata/resonance_validation_certificate.json")
    
    if not metadata_file.exists():
        print(f"Error: Metadata file not found at {metadata_file}")
        print("Please run generate_metadata.py first")
        return 1
    
    valid = validate_metadata(metadata_file)
    return 0 if valid else 1

if __name__ == "__main__":
    sys.exit(main())
