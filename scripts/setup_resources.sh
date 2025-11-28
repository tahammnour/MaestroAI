#!/bin/bash

# Setup Resources Script
# Downloads and sets up all challenge resources for MaestroAI

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Setting up MaestroAI Resources${NC}"
echo "=========================================="

# Create data directory
mkdir -p data

# 1. Download Hugging Face dataset
echo -e "\n${YELLOW}1. Downloading Hugging Face IT Help Desk Dataset...${NC}"
python scripts/download_hf_dataset.py

# 2. Generate synthetic tickets
echo -e "\n${YELLOW}2. Generating synthetic HR tickets...${NC}"
if [ -f ".env" ] && grep -q "OPENAI_API_KEY" .env; then
    python scripts/generate_synthetic_tickets.py --count 200
else
    echo "⚠️  Skipping synthetic ticket generation (OPENAI_API_KEY not set)"
fi

# 3. Download Kaggle datasets (if kaggle is configured)
echo -e "\n${YELLOW}3. Downloading Kaggle datasets...${NC}"
if command -v kaggle &> /dev/null || [ -f ~/.kaggle/kaggle.json ]; then
    echo "  Downloading HR Analytics dataset..."
    python scripts/download_kaggle_dataset.py --dataset arashnic/hr-ana || echo "  ⚠️  Failed to download HR Analytics dataset"
    
    echo "  Downloading Human Resources dataset..."
    python scripts/download_kaggle_dataset.py --dataset rhuebner/human-resources-data-set || echo "  ⚠️  Failed to download HR dataset"
else
    echo "⚠️  Kaggle API not configured. Skipping Kaggle datasets."
    echo "   To configure: https://www.kaggle.com/docs/api"
fi

# 4. Clone Azure Runbooks reference
echo -e "\n${YELLOW}4. Cloning Azure Runbooks reference...${NC}"
if [ ! -d "runbooks-reference" ]; then
    git clone https://github.com/azureautomation/runbooks.git runbooks-reference || echo "  ⚠️  Failed to clone runbooks"
else
    echo "  ✅ Runbooks reference already exists"
fi

echo -e "\n${GREEN}✅ Resource setup complete!${NC}"
echo "📁 Check the 'data' directory for downloaded datasets"

