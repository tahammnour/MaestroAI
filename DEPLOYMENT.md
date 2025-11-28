# 🚀 MaestroAI Azure Deployment Guide

This guide provides step-by-step instructions to deploy MaestroAI on Azure.

---

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ Azure subscription with Owner or Contributor role
- ✅ Azure CLI installed ([Install Guide](https://learn.microsoft.com/cli/azure/install-azure-cli))
- ✅ Python 3.9+ installed
- ✅ Git installed
- ✅ Azure CLI logged in (`az login`)
- ✅ Azure OpenAI Service access (request access if needed)

---

## 🎯 Step 1: Initial Setup

### 1.1 Login to Azure

```bash
# Login to Azure
az login

# Set your subscription (replace with your subscription ID)
az account set --subscription "YOUR_SUBSCRIPTION_ID"

# Verify current subscription
az account show
```

### 1.2 Create Resource Group

```bash
# Set variables
RESOURCE_GROUP="maestroai-rg"
LOCATION="eastus"  # Change to your preferred region

# Create resource group
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION

# Verify creation
az group show --name $RESOURCE_GROUP
```

---

## 🤖 Step 2: Deploy Azure OpenAI Service

### 2.1 Create OpenAI Resource

```bash
# Set variables
OPENAI_NAME="maestroai-openai"
OPENAI_SKU="S0"  # Standard tier

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
```

### 2.2 Deploy GPT-4 Model

```bash
# Deploy GPT-4 model (requires access)
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

**Note**: If GPT-4 is not available, use `gpt-35-turbo` as fallback.

---

## 💾 Step 3: Deploy Azure Cosmos DB

### 3.1 Create Cosmos DB Account

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

# Get connection string
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
```

### 3.2 Create Database and Containers

```bash
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

## 🔍 Step 4: Deploy Azure Cognitive Search

### 4.1 Create Search Service

```bash
# Set variables
SEARCH_SERVICE="maestroai-search"
SEARCH_SKU="basic"  # Change to standard for production

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

### 4.2 Create Search Indexes

```bash
# Create index for HR policies
az search index create \
  --resource-group $RESOURCE_GROUP \
  --service-name $SEARCH_SERVICE \
  --name hr-policies-index \
  --body @infrastructure/search-index-policies.json

# Create index for FAQs
az search index create \
  --resource-group $RESOURCE_GROUP \
  --service-name $SEARCH_SERVICE \
  --name faq-index \
  --body @infrastructure/search-index-faq.json
```

**Note**: Create the JSON files for index definitions (see infrastructure folder).

---

## ⚡ Step 5: Deploy Azure Functions

### 5.1 Create Storage Account

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
```

### 5.2 Create Function App

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

### 5.3 Deploy Function Code

```bash
# Install Azure Functions Core Tools (if not installed)
# npm install -g azure-functions-core-tools@4 --unsafe-perm true

# Deploy functions
cd agents
func azure functionapp publish $FUNCTION_APP
cd ..
```

---

## 🔐 Step 6: Deploy Azure Key Vault

### 6.1 Create Key Vault

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

### 6.2 Grant Access to Function App

```bash
# Get Function App managed identity
FUNCTION_PRINCIPAL=$(az functionapp identity show \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --query principalId -o tsv)

# Grant access to Key Vault
az keyvault set-policy \
  --name $KEY_VAULT \
  --object-id $FUNCTION_PRINCIPAL \
  --secret-permissions get list
```

---

## 🔄 Step 7: Deploy Azure Logic Apps

### 7.1 Create Logic App

```bash
# Set variables
LOGIC_APP="maestroai-orchestrator"

# Create Logic App
az logicapp create \
  --name $LOGIC_APP \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --plan $FUNCTION_PLAN

# Configure app settings
az logicapp config appsettings set \
  --name $LOGIC_APP \
  --resource-group $RESOURCE_GROUP \
  --settings \
    OPENAI_ENDPOINT="$OPENAI_ENDPOINT" \
    FUNCTION_APP_URL="https://$FUNCTION_APP.azurewebsites.net"
```

**Note**: Logic App workflows need to be configured through Azure Portal or ARM templates.

---

## 🌐 Step 8: Deploy Azure API Management

### 8.1 Create API Management Service

```bash
# Set variables
APIM_NAME="maestroai-apim"
APIM_SKU="Developer"  # Use Standard for production

# Create API Management
az apim create \
  --name $APIM_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku-name $APIM_SKU \
  --publisher-email "tahammnour@outlook.com" \
  --publisher-name "MaestroAI Team"
```

### 8.2 Configure API

```bash
# Create API
az apim api create \
  --resource-group $RESOURCE_GROUP \
  --service-name $APIM_NAME \
  --api-id maestroai-api \
  --path "maestroai" \
  --display-name "MaestroAI HR Service Desk API" \
  --service-url "https://$FUNCTION_APP.azurewebsites.net/api"
```

---

## 📊 Step 9: Deploy Application Insights

### 9.1 Create Application Insights

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

## 📦 Step 10: Deploy Azure Blob Storage

### 10.1 Create Containers

```bash
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

## 🎨 Step 11: Deploy Frontend (Optional)

### 11.1 Create Static Web App

```bash
# Set variables
WEB_APP="maestroai-web"

# Create Static Web App
az staticwebapp create \
  --name $WEB_APP \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Free
```

---

## ✅ Step 12: Verify Deployment

### 12.1 Test Function App

```bash
# Get Function App URL
FUNCTION_URL="https://$FUNCTION_APP.azurewebsites.net"

# Test health endpoint
curl "$FUNCTION_URL/api/health"
```

### 12.2 List All Resources

```bash
# List all resources in resource group
az resource list \
  --resource-group $RESOURCE_GROUP \
  --output table
```

---

## 🔧 Step 13: Post-Deployment Configuration

### 13.1 Seed Knowledge Base

```bash
# Upload sample HR policies to Cosmos DB
python scripts/seed_knowledge_base.py \
  --cosmos-endpoint "$COSMOS_ENDPOINT" \
  --cosmos-key "$COSMOS_KEY" \
  --database "$COSMOS_DB"
```

### 13.2 Index Documents in Search

```bash
# Index HR policies in Cognitive Search
python scripts/index_documents.py \
  --search-endpoint "$SEARCH_ENDPOINT" \
  --search-key "$SEARCH_KEY"
```

---

## 📝 Step 14: Environment Variables

Create a `.env` file with all configuration:

```bash
cat > .env << EOF
# Azure OpenAI
OPENAI_ENDPOINT=$OPENAI_ENDPOINT
OPENAI_API_KEY=$OPENAI_KEY

# Cosmos DB
COSMOS_ENDPOINT=$COSMOS_ENDPOINT
COSMOS_KEY=$COSMOS_KEY
COSMOS_DATABASE=$COSMOS_DB

# Cognitive Search
SEARCH_ENDPOINT=$SEARCH_ENDPOINT
SEARCH_KEY=$SEARCH_KEY

# Storage
STORAGE_CONNECTION_STRING=$STORAGE_CONNECTION

# Key Vault
KEY_VAULT_NAME=$KEY_VAULT

# Function App
FUNCTION_APP_NAME=$FUNCTION_APP
FUNCTION_APP_URL=https://$FUNCTION_APP.azurewebsites.net

# API Management
APIM_NAME=$APIM_NAME

# Application Insights
APPINSIGHTS_KEY=$INSTRUMENTATION_KEY
EOF
```

---

## 🚨 Troubleshooting

### Common Issues

1. **OpenAI Access Denied**
   ```bash
   # Request access to Azure OpenAI
   # Visit: https://aka.ms/oai/access
   ```

2. **Function App Deployment Fails**
   ```bash
   # Check function app logs
   az functionapp log tail --name $FUNCTION_APP --resource-group $RESOURCE_GROUP
   ```

3. **Cosmos DB Connection Issues**
   ```bash
   # Verify firewall rules
   az cosmosdb update \
     --name $COSMOS_ACCOUNT \
     --resource-group $RESOURCE_GROUP \
     --ip-range-filter "0.0.0.0/0"
   ```

---

## 💰 Cost Estimation

Approximate monthly costs (1000 tickets/day):

| Service | Cost |
|---------|------|
| Azure Functions | ~$50 |
| Azure OpenAI | ~$200 |
| Cognitive Search | ~$100 |
| Cosmos DB | ~$150 |
| Storage | ~$20 |
| **Total** | **~$520/month** |

---

## 🧹 Cleanup

To remove all resources:

```bash
# Delete entire resource group
az group delete \
  --name $RESOURCE_GROUP \
  --yes --no-wait
```

---

## 📚 Next Steps

1. ✅ Configure Logic App workflows
2. ✅ Set up Teams Bot integration
3. ✅ Deploy frontend application
4. ✅ Configure monitoring alerts
5. ✅ Set up CI/CD pipeline
6. ✅ Load test the system

---

## 🔗 Useful Commands

```bash
# View all resources
az resource list --resource-group $RESOURCE_GROUP --output table

# View Function App logs
az functionapp log tail --name $FUNCTION_APP --resource-group $RESOURCE_GROUP

# Restart Function App
az functionapp restart --name $FUNCTION_APP --resource-group $RESOURCE_GROUP

# Scale Function App
az functionapp plan update --name $FUNCTION_PLAN --resource-group $RESOURCE_GROUP --sku S1
```

---

<div align="center">

**Deployment Complete! 🎉**

For questions, check the [README](./README.md) or open an issue.

</div>

