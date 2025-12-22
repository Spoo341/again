"""
Storage Module
Handles optional file-based storage of optimization results.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class ResultStorage:
    """Manages storage of prompt optimization results to local files."""
    
    def __init__(self, storage_dir: str = "data"):
        """
        Initialize the storage handler.
        
        Args:
            storage_dir: Directory to store results (default: "data")
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        self.results_file = self.storage_dir / "results.json"
        
        # Initialize results file if it doesn't exist
        if not self.results_file.exists():
            self._save_results([])
    
    def save_optimization_result(self, result: Dict) -> None:
        """
        Save a single optimization result.
        
        Args:
            result: Dictionary containing optimization results
                {
                    'timestamp': str,
                    'task_type': str,
                    'original_prompt': str,
                    'optimized_prompt': str,
                    'original_score': float,
                    'optimized_score': float,
                    'improvement': float
                }
        """
        # Load existing results
        results = self._load_results()
        
        # Add timestamp if not present
        if 'timestamp' not in result:
            result['timestamp'] = datetime.now().isoformat()
        
        # Append new result
        results.append(result)
        
        # Save back to file
        self._save_results(results)
        
        print(f"Result saved to {self.results_file}")
    
    def get_all_results(self) -> List[Dict]:
        """
        Retrieve all stored results.
        
        Returns:
            List of all optimization results
        """
        return self._load_results()
    
    def get_results_by_task_type(self, task_type: str) -> List[Dict]:
        """
        Get results filtered by task type.
        
        Args:
            task_type: Task type to filter by
            
        Returns:
            List of matching results
        """
        all_results = self._load_results()
        return [r for r in all_results if r.get('task_type') == task_type]
    
    def get_statistics(self) -> Dict:
        """
        Calculate statistics from stored results.
        
        Returns:
            Dictionary with statistics:
                - total_optimizations: int
                - average_improvement: float
                - task_type_counts: dict
                - best_improvement: float
        """
        results = self._load_results()
        
        if not results:
            return {
                'total_optimizations': 0,
                'average_improvement': 0.0,
                'task_type_counts': {},
                'best_improvement': 0.0
            }
        
        # Calculate statistics
        improvements = [r.get('improvement', 0) for r in results if 'improvement' in r]
        task_types = [r.get('task_type', 'Unknown') for r in results]
        
        stats = {
            'total_optimizations': len(results),
            'average_improvement': sum(improvements) / len(improvements) if improvements else 0.0,
            'task_type_counts': self._count_task_types(task_types),
            'best_improvement': max(improvements) if improvements else 0.0
        }
        
        return stats
    
    def clear_results(self) -> None:
        """Clear all stored results."""
        self._save_results([])
        print("All results cleared")
    
    def _load_results(self) -> List[Dict]:
        """Load results from JSON file."""
        try:
            with open(self.results_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_results(self, results: List[Dict]) -> None:
        """Save results to JSON file."""
        with open(self.results_file, 'w') as f:
            json.dump(results, f, indent=2)
    
    def _count_task_types(self, task_types: List[str]) -> Dict[str, int]:
        """Count occurrences of each task type."""
        counts = {}
        for task_type in task_types:
            counts[task_type] = counts.get(task_type, 0) + 1
        return counts
    
    def export_to_csv(self, output_file: str = None) -> str:
        """
        Export results to CSV format.
        
        Args:
            output_file: Output CSV file path (optional)
            
        Returns:
            Path to the created CSV file
        """
        if output_file is None:
            output_file = self.storage_dir / "results_export.csv"
        
        results = self._load_results()
        
        if not results:
            print("No results to export")
            return None
        
        import csv
        
        # Define CSV headers
        headers = ['timestamp', 'task_type', 'original_prompt', 'optimized_prompt', 
                   'original_score', 'optimized_score', 'improvement']
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(results)
        
        print(f"Results exported to {output_file}")
        return str(output_file)
