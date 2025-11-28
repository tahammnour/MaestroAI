# 🚀 MaestroAI Azure CLI Setup Guide

Complete command-line guide to set up all Azure resources, download datasets, and deploy MaestroAI.

---

## 📋 Prerequisites

```bash
# Install Azure CLI (if not installed)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Set your subscription
az account set --subscription "YOUR_SUBSCRIPTION_ID"

# Verify
az account show
```

---

## 🎯 Step 1: Create Resource Group

```bash
# Set variables
RESOURCE_GROUP="maestroai-rg"
LOCATION="eastus"  # Change to your preferred region

# Create resource group
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION

# Verify
az group show --name $RESOURCE_GROUP
```

---

## 🤖 Step 2: Create Azure OpenAI Service

```bash
# Set variables
OPENAI_NAME="maestroai-openai"
OPENAI_SKU="S0"

# Create OpenAI resource
az cognitiveservices account create \
  --name $OPENAI_NAME \
  --resource-group $RESOURCE_GROUP \
  --kind OpenAI \
  --sku $OPENAI_SKU \
  --location $LOCATION

# Get API key
OPENAI_KEY=$(az cognitiveservices account keys list \
  --name $OPENAI_NAME \
  --resource-group $RESOURCE_GROUP \
  --query key1 -o tsv)

# Get endpoint
OPENAI_ENDPOINT=$(az cognitiveservices account show \
  --name $OPENAI_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.endpoint -o tsv)

echo "OpenAI Endpoint: $OPENAI_ENDPOINT"
echo "OpenAI Key: $OPENAI_KEY"

# Deploy GPT-4 model (or use gpt-35-turbo if GPT-4 not available)
az cognitiveservices account deployment create \
  --name $OPENAI_NAME \
  --resource-group $RESOURCE_GROUP \
  --deployment-name gpt-4 \
  --model-name gpt-4 \
  --model-version "0613" \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name "Standard"
```

---

## 💾 Step 3: Create Azure Cosmos DB

```bash
# Set variables
COSMOS_ACCOUNT="maestroai-cosmos"
COSMOS_DB="maestroai-db"

# Create Cosmos DB account
az cosmosdb create \
  --name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --default-consistency-level Session \
  --locations regionName=$LOCATION failoverPriority=0

# Get connection details
COSMOS_KEY=$(az cosmosdb keys list \
  --name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --query primaryMasterKey -o tsv)

COSMOS_ENDPOINT=$(az cosmosdb show \
  --name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --query documentEndpoint -o tsv)

echo "Cosmos Endpoint: $COSMOS_ENDPOINT"
echo "Cosmos Key: $COSMOS_KEY"

# Create database
az cosmosdb sql database create \
  --account-name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --name $COSMOS_DB

# Create containers
az cosmosdb sql container create \
  --account-name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --database-name $COSMOS_DB \
  --name hr_policies \
  --partition-key-path "/category" \
  --throughput 400

az cosmosdb sql container create \
  --account-name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --database-name $COSMOS_DB \
  --name tickets \
  --partition-key-path "/user_id" \
  --throughput 400

az cosmosdb sql container create \
  --account-name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --database-name $COSMOS_DB \
  --name conversations \
  --partition-key-path "/conversation_id" \
  --throughput 400
```

---

## 🔍 Step 4: Create Azure Cognitive Search

```bash
# Set variables
SEARCH_SERVICE="maestroai-search"
SEARCH_SKU="basic"

# Create search service
az search service create \
  --name $SEARCH_SERVICE \
  --resource-group $RESOURCE_GROUP \
  --sku $SEARCH_SKU \
  --location $LOCATION

# Get admin keys
SEARCH_KEY=$(az search admin-key show \
  --resource-group $RESOURCE_GROUP \
  --service-name $SEARCH_SERVICE \
  --query primaryKey -o tsv)

SEARCH_ENDPOINT="https://$SEARCH_SERVICE.search.windows.net"

echo "Search Endpoint: $SEARCH_ENDPOINT"
echo "Search Key: $SEARCH_KEY"
```

---

## ⚡ Step 5: Create Azure Storage Account

```bash
# Set variables
STORAGE_ACCOUNT="maestroaistorage$(date +%s | cut -b1-10)"

# Create storage account
az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard_LRS

# Get storage connection string
STORAGE_CONNECTION=$(az storage account show-connection-string \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --query connectionString -o tsv)

echo "Storage Connection: $STORAGE_CONNECTION"

# Create containers
az storage container create \
  --name hr-documents \
  --connection-string "$STORAGE_CONNECTION"

az storage container create \
  --name runbooks \
  --connection-string "$STORAGE_CONNECTION"

az storage container create \
  --name logs \
  --connection-string "$STORAGE_CONNECTION"
```

---

## ⚡ Step 6: Create Azure Functions

```bash
# Set variables
FUNCTION_APP="maestroai-functions"
FUNCTION_PLAN="maestroai-functions-plan"

# Create App Service Plan
az functionapp plan create \
  --name $FUNCTION_PLAN \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku B1

# Create Function App
az functionapp create \
  --name $FUNCTION_APP \
  --storage-account $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --plan $FUNCTION_PLAN \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4

# Configure app settings
az functionapp config appsettings set \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --settings \
    AzureWebJobsStorage="$STORAGE_CONNECTION" \
    OPENAI_ENDPOINT="$OPENAI_ENDPOINT" \
    OPENAI_API_KEY="$OPENAI_KEY" \
    COSMOS_ENDPOINT="$COSMOS_ENDPOINT" \
    COSMOS_KEY="$COSMOS_KEY" \
    COSMOS_DATABASE="$COSMOS_DB" \
    SEARCH_ENDPOINT="$SEARCH_ENDPOINT" \
    SEARCH_KEY="$SEARCH_KEY" \
    FUNCTIONS_WORKER_RUNTIME=python
```

---

## 🔐 Step 7: Create Azure Key Vault

```bash
# Set variables
KEY_VAULT="maestroai-kv-$(date +%s | cut -b1-10)"

# Create Key Vault
az keyvault create \
  --name $KEY_VAULT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --enable-soft-delete true \
  --enable-purge-protection true

# Store secrets
az keyvault secret set \
  --vault-name $KEY_VAULT \
  --name "OpenAI-Key" \
  --value "$OPENAI_KEY"

az keyvault secret set \
  --vault-name $KEY_VAULT \
  --name "Cosmos-Key" \
  --value "$COSMOS_KEY"

az keyvault secret set \
  --vault-name $KEY_VAULT \
  --name "Search-Key" \
  --value "$SEARCH_KEY"
```

---

## 📊 Step 8: Create Application Insights

```bash
# Set variables
APPINSIGHTS_NAME="maestroai-insights"

# Create Application Insights
az monitor app-insights component create \
  --app $APPINSIGHTS_NAME \
  --location $LOCATION \
  --resource-group $RESOURCE_GROUP \
  --application-type web

# Get instrumentation key
INSTRUMENTATION_KEY=$(az monitor app-insights component show \
  --app $APPINSIGHTS_NAME \
  --resource-group $RESOURCE_GROUP \
  --query instrumentationKey -o tsv)

# Update Function App with instrumentation key
az functionapp config appsettings set \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --settings \
    APPINSIGHTS_INSTRUMENTATION_KEY="$INSTRUMENTATION_KEY"
```

---

## 📥 Step 9: Download and Prepare Datasets

### 9.1 Install Required Python Packages

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install datasets pandas kaggle azure-cosmos azure-search-documents
```

### 9.2 Download Hugging Face Dataset

```bash
# Download IT Help Desk Synthetic Tickets
python scripts/download_hf_dataset.py

# This creates: data/hr_tickets_synthetic.json
```

### 9.3 Download Kaggle Datasets

```bash
# Setup Kaggle API (if not done)
# 1. Go to https://www.kaggle.com/account
# 2. Create API token
# 3. Place kaggle.json in ~/.kaggle/

# Download HR Analytics dataset
python scripts/download_kaggle_dataset.py --dataset arashnic/hr-ana

# Download Human Resources dataset
python scripts/download_kaggle_dataset.py --dataset rhuebner/human-resources-data-set
```

### 9.4 Generate Synthetic Tickets

```bash
# Generate synthetic HR tickets using Azure OpenAI
python scripts/generate_synthetic_tickets.py --count 200

# This creates: data/synthetic_hr_tickets.json
```

---

## 📤 Step 10: Upload Datasets to Azure

### 10.1 Upload to Azure Storage (Blob)

```bash
# Upload HR tickets to blob storage
az storage blob upload \
  --account-name $STORAGE_ACCOUNT \
  --container-name hr-documents \
  --name hr_tickets_synthetic.json \
  --file data/hr_tickets_synthetic.json \
  --connection-string "$STORAGE_CONNECTION"

# Upload synthetic tickets
az storage blob upload \
  --account-name $STORAGE_ACCOUNT \
  --container-name hr-documents \
  --name synthetic_hr_tickets.json \
  --file data/synthetic_hr_tickets.json \
  --connection-string "$STORAGE_CONNECTION"

# Upload PDF documents
az storage blob upload \
  --account-name $STORAGE_ACCOUNT \
  --container-name hr-documents \
  --name "MaestroAI Intelligent HR Service Desk.pdf" \
  --file "MaestroAI Intelligent HR Service Desk.pdf" \
  --connection-string "$STORAGE_CONNECTION"
```

### 10.2 Seed Cosmos DB with Knowledge Base

```bash
# Set environment variables
export COSMOS_ENDPOINT="$COSMOS_ENDPOINT"
export COSMOS_KEY="$COSMOS_KEY"
export COSMOS_DATABASE="$COSMOS_DB"

# Seed knowledge base
python scripts/seed_knowledge_base.py
```

### 10.3 Upload HR Datasets to Cosmos DB

```bash
# Create Python script to upload datasets
cat > scripts/upload_datasets_to_cosmos.py << 'EOF'
#!/usr/bin/env python3
import os
import json
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

load_dotenv()

client = CosmosClient(os.getenv("COSMOS_ENDPOINT"), os.getenv("COSMOS_KEY"))
database = client.get_database_client(os.getenv("COSMOS_DATABASE"))
container = database.get_container_client("hr_policies")

# Load and upload HR tickets
with open("data/hr_tickets_synthetic.json", "r") as f:
    tickets = json.load(f)
    for ticket in tickets[:100]:  # Upload first 100
        ticket["id"] = f"ticket_{ticket.get('id', 'unknown')}"
        ticket["category"] = ticket.get("category", "General")
        container.upsert_item(ticket)
        print(f"Uploaded: {ticket['id']}")

print("✅ Datasets uploaded to Cosmos DB")
EOF

# Run upload script
python scripts/upload_datasets_to_cosmos.py
```

### 10.4 Index Documents in Cognitive Search

```bash
# Create search index definition
cat > search-index-policies.json << 'EOF'
{
  "name": "hr-policies-index",
  "fields": [
    {"name": "id", "type": "Edm.String", "key": true},
    {"name": "title", "type": "Edm.String", "searchable": true},
    {"name": "content", "type": "Edm.String", "searchable": true},
    {"name": "category", "type": "Edm.String", "filterable": true},
    {"name": "tags", "type": "Collection(Edm.String)", "filterable": true}
  ]
}
EOF

# Create index
az search index create \
  --resource-group $RESOURCE_GROUP \
  --service-name $SEARCH_SERVICE \
  --name hr-policies-index \
  --body @search-index-policies.json

# Index documents
python scripts/index_documents.py
```

---

## 🔄 Step 11: Deploy Function App Code

```bash
# Install Azure Functions Core Tools
npm install -g azure-functions-core-tools@4 --unsafe-perm true

# Navigate to agents directory
cd agents

# Deploy functions
func azure functionapp publish $FUNCTION_APP --python

cd ..
```

---

## ✅ Step 12: Verify Deployment

```bash
# List all resources
az resource list \
  --resource-group $RESOURCE_GROUP \
  --output table

# Test Function App
curl "https://$FUNCTION_APP.azurewebsites.net/api/health"

# Check Cosmos DB containers
az cosmosdb sql container list \
  --account-name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --database-name $COSMOS_DB

# Check Storage containers
az storage container list \
  --account-name $STORAGE_ACCOUNT \
  --connection-string "$STORAGE_CONNECTION"
```

---

## 📝 Step 13: Save Configuration

```bash
# Create .env file with all configuration
cat > .env << EOF
# Azure OpenAI
OPENAI_ENDPOINT=$OPENAI_ENDPOINT
OPENAI_API_KEY=$OPENAI_KEY
OPENAI_DEPLOYMENT_NAME=gpt-4
OPENAI_API_VERSION=2024-02-15-preview

# Cosmos DB
COSMOS_ENDPOINT=$COSMOS_ENDPOINT
COSMOS_KEY=$COSMOS_KEY
COSMOS_DATABASE=$COSMOS_DB

# Cognitive Search
SEARCH_ENDPOINT=$SEARCH_ENDPOINT
SEARCH_KEY=$SEARCH_KEY
SEARCH_INDEX_POLICIES=hr-policies-index

# Storage
STORAGE_ACCOUNT_NAME=$STORAGE_ACCOUNT
STORAGE_CONNECTION_STRING=$STORAGE_CONNECTION

# Key Vault
KEY_VAULT_NAME=$KEY_VAULT

# Function App
FUNCTION_APP_NAME=$FUNCTION_APP
FUNCTION_APP_URL=https://$FUNCTION_APP.azurewebsites.net

# Application Insights
APPINSIGHTS_KEY=$INSTRUMENTATION_KEY

# Resource Group
RESOURCE_GROUP=$RESOURCE_GROUP
LOCATION=$LOCATION
EOF

echo "✅ Configuration saved to .env"
```

---

## 🚀 Complete Setup Script

Save all commands in one script:

```bash
# Create complete setup script
cat > setup_azure_resources.sh << 'EOF'
#!/bin/bash
set -e

# Load variables
source .env 2>/dev/null || true

RESOURCE_GROUP="${RESOURCE_GROUP:-maestroai-rg}"
LOCATION="${LOCATION:-eastus}"

echo "🚀 Setting up MaestroAI Azure Resources..."

# Run all setup steps above
# (Copy commands from steps 1-13)

echo "✅ Setup complete!"
EOF

chmod +x setup_azure_resources.sh
```

---

## 📊 Dataset Usage Guide

### Using Hugging Face Dataset

```bash
# Download dataset
python scripts/download_hf_dataset.py

# Process and convert to HR context
# Output: data/hr_tickets_synthetic.json
```

### Using Kaggle Datasets

```bash
# Download HR Analytics
python scripts/download_kaggle_dataset.py --dataset arashnic/hr-ana
# Files saved to: data/hr_analytics/

# Download HR Data Set
python scripts/download_kaggle_dataset.py --dataset rhuebner/human-resources-data-set
# Files saved to: data/hr_dataset/
```

### Generating Synthetic Data

```bash
# Generate 200 synthetic tickets
python scripts/generate_synthetic_tickets.py --count 200

# Output: data/synthetic_hr_tickets.json
```

### Uploading to Azure

```bash
# Upload to Storage
az storage blob upload-batch \
  --account-name $STORAGE_ACCOUNT \
  --source data/ \
  --destination hr-documents \
  --connection-string "$STORAGE_CONNECTION"

# Upload to Cosmos DB
python scripts/seed_knowledge_base.py
python scripts/upload_datasets_to_cosmos.py
```

---

## 🔍 Monitoring Commands

```bash
# View Function App logs
az functionapp log tail \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP

# View Application Insights
az monitor app-insights query \
  --app $APPINSIGHTS_NAME \
  --resource-group $RESOURCE_GROUP \
  --analytics-query "requests | take 10"

# Check resource costs
az consumption usage list \
  --start-date $(date -d "1 month ago" +%Y-%m-%d) \
  --end-date $(date +%Y-%m-%d)
```

---

## 🧹 Cleanup Commands

```bash
# Delete entire resource group (removes all resources)
az group delete \
  --name $RESOURCE_GROUP \
  --yes --no-wait

# Delete individual resources
az cognitiveservices account delete \
  --name $OPENAI_NAME \
  --resource-group $RESOURCE_GROUP

az cosmosdb delete \
  --name $COSMOS_ACCOUNT \
  --resource-group $RESOURCE_GROUP
```

---

## 📚 Quick Reference

### Essential Variables
```bash
RESOURCE_GROUP="maestroai-rg"
LOCATION="eastus"
OPENAI_NAME="maestroai-openai"
COSMOS_ACCOUNT="maestroai-cosmos"
SEARCH_SERVICE="maestroai-search"
STORAGE_ACCOUNT="maestroaistorage..."
FUNCTION_APP="maestroai-functions"
KEY_VAULT="maestroai-kv-..."
```

### Common Commands
```bash
# List resources
az resource list -g $RESOURCE_GROUP -o table

# Get connection strings
az storage account show-connection-string -n $STORAGE_ACCOUNT -g $RESOURCE_GROUP

# View logs
az functionapp log tail -n $FUNCTION_APP -g $RESOURCE_GROUP

# Restart function app
az functionapp restart -n $FUNCTION_APP -g $RESOURCE_GROUP
```

---

## 🎯 Next Steps

1. ✅ All resources created
2. ✅ Datasets downloaded
3. ✅ Data uploaded to Azure
4. ✅ Functions deployed
5. 🚀 Test the system!

```bash
# Test API
curl -X POST "https://$FUNCTION_APP.azurewebsites.net/api/process" \
  -H "Content-Type: application/json" \
  -d '{"message": "I need to take 3 days of sick leave", "user_id": "test@example.com"}'
```

---

<div align="center">

**All Azure resources created and ready! 🎉**

</div>

