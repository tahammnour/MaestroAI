#!/usr/bin/env python3
"""
Download Hugging Face IT Help Desk Synthetic Tickets Dataset
Converts IT tickets to HR context for MaestroAI
"""

import os
import sys
import json
from pathlib import Path
from datasets import load_dataset
from dotenv import load_dotenv

load_dotenv()


def download_and_process_dataset():
    """Download and process the Hugging Face IT help desk dataset."""
    
    print("📥 Downloading IT Help Desk Synthetic Tickets Dataset...")
    
    try:
        # Load dataset from Hugging Face
        dataset = load_dataset("Console-AI/IT-helpdesk-synthetic-tickets")
        
        print(f"✅ Dataset loaded: {len(dataset['train'])} tickets")
        
        # Create data directory
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Convert to HR context
        hr_tickets = []
        category_mapping = {
            "Network": "IT_Support",
            "Software": "Software_Access",
            "Account": "Account_Management",
            "Communication": "Communication_Tools",
            "RemoteWork": "Remote_Work",
            "Hardware": "Hardware_Request"
        }
        
        for ticket in dataset['train']:
            # Convert IT ticket to HR ticket format
            hr_ticket = {
                "id": ticket.get("id", ""),
                "subject": convert_subject_to_hr(ticket.get("subject", "")),
                "description": convert_description_to_hr(ticket.get("description", "")),
                "priority": ticket.get("priority", "Medium"),
                "category": category_mapping.get(ticket.get("category", ""), "General"),
                "created_at": ticket.get("createdAt", ""),
                "requester_email": ticket.get("requesterEmail", ""),
                "original_category": ticket.get("category", "")
            }
            hr_tickets.append(hr_ticket)
        
        # Save processed tickets
        output_file = data_dir / "hr_tickets_synthetic.json"
        with open(output_file, 'w') as f:
            json.dump(hr_tickets, f, indent=2)
        
        print(f"✅ Processed {len(hr_tickets)} tickets")
        print(f"💾 Saved to: {output_file}")
        
        # Also save as CSV for easy viewing
        import pandas as pd
        df = pd.DataFrame(hr_tickets)
        csv_file = data_dir / "hr_tickets_synthetic.csv"
        df.to_csv(csv_file, index=False)
        print(f"💾 Also saved as CSV: {csv_file}")
        
        return hr_tickets
        
    except Exception as e:
        print(f"❌ Error downloading dataset: {str(e)}")
        print("💡 Make sure you have 'datasets' library installed: pip install datasets")
        sys.exit(1)


def convert_subject_to_hr(subject: str) -> str:
    """Convert IT ticket subject to HR context."""
    # Simple conversion - replace IT terms with HR terms
    replacements = {
        "IT": "HR",
        "network": "employee",
        "printer": "benefits",
        "email": "leave",
        "software": "policy",
        "access": "request"
    }
    
    converted = subject
    for old, new in replacements.items():
        converted = converted.replace(old, new)
    
    return converted


def convert_description_to_hr(description: str) -> str:
    """Convert IT ticket description to HR context."""
    # Convert common IT issues to HR scenarios
    conversions = {
        "printer": "leave request",
        "network": "employee data",
        "email": "benefits inquiry",
        "software": "policy question",
        "access": "information request"
    }
    
    converted = description
    for it_term, hr_term in conversions.items():
        converted = converted.replace(it_term, hr_term)
    
    return converted


if __name__ == "__main__":
    download_and_process_dataset()

