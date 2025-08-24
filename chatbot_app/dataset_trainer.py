"""
Dataset Training Integration for Chatbot
Integrates Microsoft rStar-Coder and other datasets for improved responses
"""

import os
# Removed unused import: from datasets import load_dataset
from typing import Dict, List, Optional
import json
import random

class DatasetTrainer:
    """Integrate external datasets to improve chatbot responses"""
    
    def __init__(self):
        self.datasets = {}
        self.cached_responses = {}
        
    # Removed HuggingFace dataset loading for low-memory deployment
    
    def _cache_coding_examples(self, dataset):
        """Cache coding examples for quick responses"""
        self.cached_responses['programming'] = []
        
        for example in dataset:
            if 'prompt' in example and 'response' in example:
                self.cached_responses['programming'].append({
                    'prompt': example['prompt'],
                    'response': example['response']
                })
    
    def _cache_alternative_coding_examples(self, dataset):
        """Cache alternative coding examples"""
        self.cached_responses['programming'] = []
        
        for example in dataset:
            if 'instruction' in example and 'output' in example:
                self.cached_responses['programming'].append({
                    'prompt': example['instruction'],
                    'response': example['output']
                })
    
    def get_relevant_response(self, query: str, topic: str = "general") -> Optional[str]:
        """Get relevant response from cached dataset examples"""
        
        if topic == "programming" and 'programming' in self.cached_responses:
            # Find relevant programming examples
            query_lower = query.lower()
            relevant_examples = []
            
            for example in self.cached_responses['programming']:
                prompt_lower = example['prompt'].lower()
                
                # Simple keyword matching
                if any(keyword in prompt_lower for keyword in query_lower.split()):
                    relevant_examples.append(example)
            
            if relevant_examples:
                # Return a random relevant example
                selected = random.choice(relevant_examples)
                return f"**Based on training data:**\n\n{selected['response']}"
        
        return None
    
    def save_cache(self, filepath: str = "dataset_cache.json"):
        """Save cached responses to file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.cached_responses, f, indent=2)
            print(f"✅ Cache saved to {filepath}")
        except Exception as e:
            print(f"❌ Error saving cache: {e}")
    
    def load_cache(self, filepath: str = "dataset_cache.json"):
        """Load cached responses from file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    self.cached_responses = json.load(f)
                print(f"✅ Cache loaded from {filepath}")
                return True
        except Exception as e:
            print(f"❌ Error loading cache: {e}")
        return False
    
    def get_dataset_stats(self):
        """Get statistics about loaded datasets"""
        stats = {}
        
        for name, dataset in self.datasets.items():
            stats[name] = {
                'total_examples': len(dataset),
                'sample_keys': list(dataset[0].keys()) if len(dataset) > 0 else []
            }
        
        for name, cached in self.cached_responses.items():
            stats[f'{name}_cached'] = len(cached)
        
        return stats

# Initialize the dataset trainer
dataset_trainer = DatasetTrainer()

def initialize_datasets():
    """Initialize all datasets for the chatbot"""
    print("🚀 Initializing datasets for enhanced responses...")
    
    # Try to load from cache first
    if dataset_trainer.load_cache():
        print("✅ Using cached dataset responses")
        return True
    
    # Try to load rStar-Coder dataset
    if dataset_trainer.load_rstar_coder_dataset():
        dataset_trainer.save_cache()
        return True
    
    # Fallback to alternative dataset
    if dataset_trainer.load_alternative_coding_dataset():
        dataset_trainer.save_cache()
        return True
    
    print("❌ Could not load any datasets")
    return False

def get_dataset_response(query: str, topic: str = "general") -> Optional[str]:
    """Get response from dataset if available"""
    return dataset_trainer.get_relevant_response(query, topic)

def get_stats():
    """Get dataset statistics"""
    return dataset_trainer.get_dataset_stats()
