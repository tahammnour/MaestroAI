#!/usr/bin/env python3
"""
Index Documents Script
Indexes HR documents in Azure Cognitive Search
"""

import os
import sys
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()


def index_documents():
    """Index documents in Azure Cognitive Search."""
    
    # Get configuration
    search_endpoint = os.getenv("SEARCH_ENDPOINT")
    search_key = os.getenv("SEARCH_KEY")
    index_name = os.getenv("SEARCH_INDEX_POLICIES", "hr-policies-index")
    
    if not search_endpoint or not search_key:
        print("❌ Error: SEARCH_ENDPOINT and SEARCH_KEY must be set")
        sys.exit(1)
    
    # Initialize search client
    credential = AzureKeyCredential(search_key)
    client = SearchClient(
        endpoint=search_endpoint,
        index_name=index_name,
        credential=credential
    )
    
    # Sample documents to index
    documents = [
        {
            "id": "1",
            "title": "Sick Leave Policy",
            "content": "Employees are entitled to 10 days of sick leave per year...",
            "category": "leave"
        },
        {
            "id": "2",
            "title": "Vacation Leave Policy",
            "content": "Full-time employees accrue 15 days of vacation leave...",
            "category": "leave"
        }
    ]
    
    print(f"📝 Indexing documents in {index_name}...")
    
    try:
        result = client.upload_documents(documents=documents)
        print(f"  ✅ Indexed {len(documents)} documents")
        for doc in result:
            if doc.succeeded:
                print(f"    ✅ {doc.key}")
            else:
                print(f"    ❌ {doc.key}: {doc.error_message}")
    except Exception as e:
        print(f"❌ Error indexing documents: {str(e)}")
        sys.exit(1)
    
    print("\n✅ Document indexing complete!")


if __name__ == "__main__":
    index_documents()

