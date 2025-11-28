#!/usr/bin/env python3
"""
Generate Synthetic HR Tickets using Azure OpenAI
Based on Microsoft Tech Community blog methodology
"""

import os
import sys
import json
import argparse
from pathlib import Path
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()


def generate_synthetic_tickets(count: int = 100, output_file: str = "data/synthetic_hr_tickets.json"):
    """
    Generate synthetic HR service desk tickets using Azure OpenAI.
    
    Args:
        count: Number of tickets to generate
        output_file: Output file path
    """
    
    # Initialize Azure OpenAI client
    client = AzureOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        api_version=os.getenv("OPENAI_API_VERSION", "2024-02-15-preview"),
        azure_endpoint=os.getenv("OPENAI_ENDPOINT")
    )
    
    deployment_name = os.getenv("OPENAI_DEPLOYMENT_NAME", "gpt-4")
    
    print(f"🤖 Generating {count} synthetic HR tickets using Azure OpenAI...")
    
    system_prompt = """You are a synthetic data generator for HR Service Desk tickets.
Generate realistic HR service desk tickets with the following structure:
- id: unique identifier
- subject: brief ticket subject
- description: detailed description of the HR request
- priority: Low, Medium, or High
- category: One of LEAVE_REQUEST, POLICY_QUESTION, EMPLOYEE_DATA, BENEFITS_QUERY, ACCOUNT_MANAGEMENT, GENERAL
- requester_email: realistic email address
- created_at: ISO timestamp

Make the tickets diverse and realistic. Include various HR scenarios like:
- Leave requests (sick, vacation, maternity)
- Policy questions
- Benefits inquiries
- Employee data requests
- Account access requests

Return ONLY valid JSON array, no other text."""

    tickets = []
    batch_size = 10  # Generate in batches
    
    for i in range(0, count, batch_size):
        current_batch = min(batch_size, count - i)
        print(f"  Generating batch {i//batch_size + 1} ({current_batch} tickets)...")
        
        user_prompt = f"Generate {current_batch} HR service desk tickets. Return as JSON array."
        
        try:
            response = client.chat.completions.create(
                model=deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            result = json.loads(response.choices[0].message.content)
            
            # Handle different response formats
            if isinstance(result, dict):
                if "tickets" in result:
                    batch_tickets = result["tickets"]
                elif "data" in result:
                    batch_tickets = result["data"]
                else:
                    # Assume the dict itself contains ticket data
                    batch_tickets = [result]
            elif isinstance(result, list):
                batch_tickets = result
            else:
                print(f"  ⚠️  Unexpected response format, skipping batch")
                continue
            
            tickets.extend(batch_tickets[:current_batch])
            print(f"  ✅ Generated {len(batch_tickets)} tickets")
            
        except Exception as e:
            print(f"  ❌ Error generating batch: {str(e)}")
            continue
    
    # Save tickets
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(tickets, f, indent=2)
    
    print(f"\n✅ Generated {len(tickets)} synthetic HR tickets")
    print(f"💾 Saved to: {output_path}")
    
    # Print summary
    categories = {}
    priorities = {}
    for ticket in tickets:
        cat = ticket.get("category", "Unknown")
        pri = ticket.get("priority", "Unknown")
        categories[cat] = categories.get(cat, 0) + 1
        priorities[pri] = priorities.get(pri, 0) + 1
    
    print("\n📊 Summary:")
    print(f"  Categories: {categories}")
    print(f"  Priorities: {priorities}")
    
    return tickets


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic HR tickets")
    parser.add_argument(
        "--count",
        type=int,
        default=100,
        help="Number of tickets to generate (default: 100)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/synthetic_hr_tickets.json",
        help="Output file path (default: data/synthetic_hr_tickets.json)"
    )
    
    args = parser.parse_args()
    
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_ENDPOINT"):
        print("❌ Error: OPENAI_API_KEY and OPENAI_ENDPOINT must be set in .env file")
        sys.exit(1)
    
    generate_synthetic_tickets(args.count, args.output)


if __name__ == "__main__":
    main()

