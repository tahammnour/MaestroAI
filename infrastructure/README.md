# Infrastructure as Code

This directory contains infrastructure definitions for deploying MaestroAI to Azure.

## Files

- `main.bicep` - Main Bicep template for Azure resources (to be created)
- `azure-pipelines.yml` - CI/CD pipeline configuration (to be created)

## Deployment

### Using Bicep

```bash
az deployment group create \
  --resource-group maestroai-rg \
  --template-file main.bicep \
  --parameters @parameters.json
```

### Using Azure CLI

See [DEPLOYMENT.md](../DEPLOYMENT.md) for step-by-step instructions.

