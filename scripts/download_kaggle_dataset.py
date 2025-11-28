#!/usr/bin/env python3
"""
Download Kaggle Datasets for HR Analytics
Requires Kaggle API credentials
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


def download_kaggle_dataset(dataset_name: str, output_dir: str = "data"):
    """
    Download a dataset from Kaggle.
    
    Args:
        dataset_name: Dataset name in format 'username/dataset-name'
        output_dir: Directory to save the dataset
    """
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        
        print(f"📥 Downloading Kaggle dataset: {dataset_name}")
        
        # Initialize Kaggle API
        api = KaggleApi()
        api.authenticate()
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Download dataset
        api.dataset_download_files(
            dataset=dataset_name,
            path=str(output_path),
            unzip=True
        )
        
        print(f"✅ Dataset downloaded to: {output_path}")
        
        # List downloaded files
        files = list(output_path.glob("*"))
        print(f"📁 Files downloaded: {len(files)}")
        for file in files[:10]:  # Show first 10 files
            print(f"   - {file.name}")
        
    except ImportError:
        print("❌ Error: kaggle library not installed")
        print("💡 Install with: pip install kaggle")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error downloading dataset: {str(e)}")
        print("\n💡 Make sure you have:")
        print("   1. Kaggle API token set up (kaggle.json)")
        print("   2. Dataset name is correct (format: username/dataset-name)")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Download Kaggle datasets")
    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="Dataset name (format: username/dataset-name)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data",
        help="Output directory (default: data)"
    )
    
    args = parser.parse_args()
    
    download_kaggle_dataset(args.dataset, args.output)


if __name__ == "__main__":
    main()

