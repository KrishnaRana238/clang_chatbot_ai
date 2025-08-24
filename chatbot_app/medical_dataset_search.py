import json
import os
from typing import Optional

def get_medical_response_from_dataset(query: str, dataset_path: str = None) -> Optional[str]:
    """
    Search the medical training dataset for a matching question and return the answer.
    Uses simple keyword matching for demonstration.
    """
    if dataset_path is None:
        dataset_path = os.path.join(os.path.dirname(__file__), 'medical_training_data_template.json')
    if not os.path.exists(dataset_path):
        return None
    try:
        with open(dataset_path, 'r') as f:
            data = json.load(f)
        query_lower = query.lower()
        # Find best match (simple contains or exact match)
        for entry in data:
            if 'question' in entry and entry['question']:
                if query_lower in entry['question'].lower() or entry['question'].lower() in query_lower:
                    return entry['answer']
        return None
    except Exception as e:
        print(f"Error reading medical dataset: {e}")
        return None
