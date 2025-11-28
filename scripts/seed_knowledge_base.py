#!/usr/bin/env python3
"""
Seed Knowledge Base Script
Populates Azure Cosmos DB with sample HR policies and FAQs
"""

import os
import sys
import json
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

load_dotenv()


def seed_knowledge_base():
    """Seed the knowledge base with sample HR data."""
    
    # Get configuration from environment
    cosmos_endpoint = os.getenv("COSMOS_ENDPOINT")
    cosmos_key = os.getenv("COSMOS_KEY")
    database_name = os.getenv("COSMOS_DATABASE", "maestroai-db")
    
    if not cosmos_endpoint or not cosmos_key:
        print("❌ Error: COSMOS_ENDPOINT and COSMOS_KEY must be set")
        sys.exit(1)
    
    # Initialize Cosmos DB client
    client = CosmosClient(cosmos_endpoint, cosmos_key)
    database = client.get_database_client(database_name)
    
    # Sample HR policies
    policies = [
        {
            "id": "policy_leave_sick",
            "category": "leave",
            "title": "Sick Leave Policy",
            "content": "Employees are entitled to 10 days of sick leave per year. Sick leave over 2 consecutive days requires manager approval and may require a doctor's note.",
            "tags": ["leave", "sick", "approval"],
            "last_updated": "2024-01-15"
        },
        {
            "id": "policy_leave_vacation",
            "category": "leave",
            "title": "Vacation Leave Policy",
            "content": "Full-time employees accrue 15 days of vacation leave per year. Vacation requests should be submitted at least 2 weeks in advance. Manager approval is required for all vacation requests.",
            "tags": ["leave", "vacation", "approval"],
            "last_updated": "2024-01-15"
        },
        {
            "id": "policy_maternity",
            "category": "benefits",
            "title": "Maternity Leave Policy",
            "content": "Eligible employees are entitled to 12 weeks of paid maternity leave. Requests must be submitted at least 30 days in advance with appropriate documentation.",
            "tags": ["maternity", "leave", "benefits"],
            "last_updated": "2024-01-15"
        },
        {
            "id": "policy_remote_work",
            "category": "workplace",
            "title": "Remote Work Policy",
            "content": "Remote work is available for eligible positions with manager approval. Employees must have a dedicated workspace and reliable internet connection.",
            "tags": ["remote", "workplace", "approval"],
            "last_updated": "2024-01-15"
        }
    ]
    
    # Get or create container
    try:
        container = database.get_container_client("hr_policies")
    except:
        database.create_container(
            id="hr_policies",
            partition_key=PartitionKey(path="/category")
        )
        container = database.get_container_client("hr_policies")
    
    # Insert policies
    print("📝 Seeding HR policies...")
    for policy in policies:
        try:
            container.upsert_item(policy)
            print(f"  ✅ Inserted: {policy['title']}")
        except Exception as e:
            print(f"  ❌ Error inserting {policy['title']}: {str(e)}")
    
    print("\n✅ Knowledge base seeding complete!")


if __name__ == "__main__":
    seed_knowledge_base()

