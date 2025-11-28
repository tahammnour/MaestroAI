# ⚡ MaestroAI Quick Start Guide

Get up and running with MaestroAI in 5 minutes!

## 🎯 Prerequisites

- Azure subscription
- Azure CLI installed
- Python 3.9+

## 🚀 Quick Setup

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/tahammnour/MaestroAI.git
cd MaestroAI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp env.example .env

# Edit .env with your Azure credentials
nano .env  # or use your favorite editor
```

### 3. Deploy to Azure

```bash
# Option 1: Use automated script
./deploy.sh

# Option 2: Follow manual steps
# See DEPLOYMENT.md for detailed instructions
```

### 4. Seed Knowledge Base

```bash
# Populate Cosmos DB with sample data
python scripts/seed_knowledge_base.py

# Index documents in Cognitive Search
python scripts/index_documents.py
```

### 5. Test the System

```bash
# Test intent classification
curl -X POST https://your-function-app.azurewebsites.net/api/intent_classifier \
  -H "Content-Type: application/json" \
  -d '{"message": "I need to take 3 days of sick leave"}'
```

## 📚 Next Steps

- Read [ARCHITECTURE.md](./ARCHITECTURE.md) to understand the system
- Check [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment
- Review [README.md](./README.md) for full documentation

## 🆘 Need Help?

- Open an issue on GitHub
- Check the Discussions forum
- Email: msdev@microsoft.com

---

**Happy Hacking! 🎉**

