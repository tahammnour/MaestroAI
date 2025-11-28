# 📚 Challenge Resources & Datasets

This document lists all the resources provided for the Microsoft Innovation Challenge Hackathon that MaestroAI uses.

---

## 🎯 Challenge Resources

### 1. IT Help Desk Synthetic Tickets Dataset

**Source**: [Hugging Face - Console-AI/IT-helpdesk-synthetic-tickets](https://huggingface.co/datasets/Console-AI/IT-helpdesk-synthetic-tickets)

**Description**: Synthetic IT help desk tickets dataset with 500 rows containing:
- Ticket IDs
- Subjects
- Descriptions
- Priority levels (Low, Medium, High)
- Categories (Network, Software, Account, Communication, RemoteWork, etc.)
- Requester emails
- Timestamps

**Usage in MaestroAI**:
- Training intent classifier with real-world ticket patterns
- Testing escalation logic with various priority levels
- Generating synthetic HR tickets for testing
- Understanding ticket categorization patterns

**How to Use**:
```bash
# Download and process the dataset
python scripts/download_hf_dataset.py
```

---

### 2. Azure Automation Runbooks

**Source**: [GitHub - azureautomation/runbooks](https://github.com/azureautomation/runbooks/tree/master)

**Description**: Collection of Azure Automation runbooks for various automation scenarios including:
- Account management
- Resource management
- Monitoring and diagnostics
- Security operations

**Usage in MaestroAI**:
- Reference implementation for HR runbooks
- Patterns for safe automation execution
- Examples of runbook structure and error handling
- Integration patterns with Azure services

**How to Use**:
```bash
# Clone and reference runbooks
git clone https://github.com/azureautomation/runbooks.git runbooks-reference
# Adapt runbooks for HR scenarios in runbooks/ directory
```

---

### 3. HR Analytics Dataset

**Source**: [Kaggle - HR Analytics Dataset](https://www.kaggle.com/datasets/arashnic/hr-ana)

**Description**: HR analytics dataset containing employee information useful for:
- Employee promotion predictions
- Performance analytics
- Employee data lookups
- HR decision support

**Usage in MaestroAI**:
- Employee data retrieval automation
- Leave balance calculations
- Promotion eligibility checks
- Employee profile lookups

**How to Use**:
```bash
# Download from Kaggle (requires API token)
python scripts/download_kaggle_dataset.py --dataset arashnic/hr-ana
```

---

### 4. Human Resources Data Set

**Source**: [Kaggle - Human Resources Data Set](https://www.kaggle.com/datasets/rhuebner/human-resources-data-set)

**Description**: Comprehensive HR dataset with:
- Employee demographics
- Employment details
- Department information
- Salary data
- Performance metrics

**Usage in MaestroAI**:
- Knowledge base for employee queries
- Policy compliance checking
- Benefits eligibility verification
- HR analytics and reporting

**How to Use**:
```bash
# Download from Kaggle
python scripts/download_kaggle_dataset.py --dataset rhuebner/human-resources-data-set
```

---

### 5. Synthetic Data for AI Agents

**Source**: [Microsoft Tech Community - Kickstarting AI Agent Development with Synthetic Data](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/kickstarting-ai-agent-development-with-synthetic-data-a-genai-approach-on-azure/4399235)

**Description**: Blog post and methodology for:
- Generating synthetic data using Azure OpenAI
- Training AI agents with synthetic datasets
- Best practices for synthetic data generation
- Azure AI Foundry integration

**Usage in MaestroAI**:
- Generating synthetic HR tickets for training
- Creating test scenarios
- Augmenting training data
- Improving agent performance

**How to Use**:
```bash
# Generate synthetic HR tickets
python scripts/generate_synthetic_tickets.py --count 1000
```

---

## 🔧 Integration Scripts

### Download All Resources

```bash
# Run the setup script to download all resources
./scripts/setup_resources.sh
```

### Individual Downloads

```bash
# Hugging Face dataset
python scripts/download_hf_dataset.py

# Kaggle datasets (requires kaggle API)
python scripts/download_kaggle_dataset.py --dataset arashnic/hr-ana
python scripts/download_kaggle_dataset.py --dataset rhuebner/human-resources-data-set

# Generate synthetic tickets
python scripts/generate_synthetic_tickets.py
```

---

## 📊 Data Processing

### Processing IT Help Desk Tickets

```python
from datasets import load_dataset

# Load Hugging Face dataset
dataset = load_dataset("Console-AI/IT-helpdesk-synthetic-tickets")

# Convert to HR context
hr_tickets = convert_to_hr_tickets(dataset)
```

### Processing HR Datasets

```python
import pandas as pd

# Load HR analytics dataset
hr_data = pd.read_csv("data/hr_analytics.csv")

# Process for knowledge base
process_for_knowledge_base(hr_data)
```

---

## 🎯 How MaestroAI Uses These Resources

### 1. Training & Development
- **Synthetic Tickets**: Train intent classifier with diverse ticket patterns
- **HR Datasets**: Build knowledge base for employee queries

### 2. Testing & Validation
- **Synthetic Data**: Generate test scenarios for all agents
- **Real Patterns**: Validate against real-world ticket structures

### 3. Runbook Development
- **Azure Runbooks**: Reference for automation patterns
- **Adaptation**: Convert IT runbooks to HR scenarios

### 4. Knowledge Base
- **HR Datasets**: Populate Cosmos DB with employee data
- **Policies**: Extract policy information from datasets

---

## 📝 Data Privacy & Compliance

⚠️ **Important**: When using these datasets:
- Remove or anonymize PII (Personally Identifiable Information)
- Follow GDPR and data protection regulations
- Use synthetic data for production testing
- Implement proper access controls

---

## 🔗 Quick Links

- [Hugging Face Dataset](https://huggingface.co/datasets/Console-AI/IT-helpdesk-synthetic-tickets)
- [Azure Runbooks GitHub](https://github.com/azureautomation/runbooks/tree/master)
- [HR Analytics Dataset](https://www.kaggle.com/datasets/arashnic/hr-ana)
- [HR Data Set](https://www.kaggle.com/datasets/rhuebner/human-resources-data-set)
- [Synthetic Data Blog](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/kickstarting-ai-agent-development-with-synthetic-data-a-genai-approach-on-azure/4399235)

---

<div align="center">

**All resources are used in compliance with their respective licenses** 📜

</div>

