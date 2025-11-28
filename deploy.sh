#!/bin/bash

# MaestroAI Azure Deployment Script
# This script automates the deployment of MaestroAI to Azure

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
RESOURCE_GROUP="maestroai-rg"
LOCATION="eastus"
DEPLOYMENT_NAME="maestroai-deployment-$(date +%s)"

echo -e "${GREEN}🚀 Starting MaestroAI Azure Deployment${NC}"
echo "=========================================="

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if logged in
echo -e "${YELLOW}📋 Checking Azure login status...${NC}"
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in. Please login...${NC}"
    az login
fi

# Get current subscription
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
echo -e "${GREEN}✅ Using subscription: $SUBSCRIPTION_ID${NC}"

# Create resource group
echo -e "${YELLOW}📦 Creating resource group...${NC}"
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION \
    --output none

echo -e "${GREEN}✅ Resource group created: $RESOURCE_GROUP${NC}"

# Deploy using Bicep template (if available)
if [ -f "infrastructure/main.bicep" ]; then
    echo -e "${YELLOW}🏗️  Deploying infrastructure using Bicep...${NC}"
    az deployment group create \
        --resource-group $RESOURCE_GROUP \
        --template-file infrastructure/main.bicep \
        --parameters location=$LOCATION \
        --name $DEPLOYMENT_NAME
    
    echo -e "${GREEN}✅ Infrastructure deployed successfully${NC}"
else
    echo -e "${YELLOW}⚠️  Bicep template not found. Using manual deployment steps.${NC}"
    echo -e "${YELLOW}📖 Please follow the steps in DEPLOYMENT.md${NC}"
fi

# Deploy Function App code
if [ -d "agents" ]; then
    echo -e "${YELLOW}⚡ Deploying Azure Functions...${NC}"
    
    # Check if Azure Functions Core Tools is installed
    if command -v func &> /dev/null; then
        cd agents
        func azure functionapp publish maestroai-functions --python
        cd ..
        echo -e "${GREEN}✅ Functions deployed${NC}"
    else
        echo -e "${YELLOW}⚠️  Azure Functions Core Tools not installed. Skipping function deployment.${NC}"
        echo -e "${YELLOW}   Install with: npm install -g azure-functions-core-tools@4${NC}"
    fi
fi

# Display deployment summary
echo ""
echo -e "${GREEN}=========================================="
echo "🎉 Deployment Complete!"
echo "==========================================${NC}"
echo ""
echo "Resource Group: $RESOURCE_GROUP"
echo "Location: $LOCATION"
echo ""
echo -e "${YELLOW}📋 Next Steps:${NC}"
echo "1. Configure environment variables in Azure Portal"
echo "2. Seed the knowledge base with HR policies"
echo "3. Index documents in Cognitive Search"
echo "4. Test the API endpoints"
echo ""
echo -e "${YELLOW}🔗 Useful Commands:${NC}"
echo "  View resources: az resource list -g $RESOURCE_GROUP -o table"
echo "  View logs: az functionapp log tail -n maestroai-functions -g $RESOURCE_GROUP"
echo "  Delete all: az group delete -n $RESOURCE_GROUP --yes"
echo ""

