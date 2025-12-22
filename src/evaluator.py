"""
Evaluator Module
Implements deterministic, rule-based metrics for evaluating response quality.
NO subjective LLM self-evaluation - only fixed, measurable criteria.
"""

import re
from typing import Dict, List


class ResponseEvaluator:
    """
    Evaluates response quality using predefined, rule-based metrics.
    All scoring is deterministic and does not rely on LLM judgment.
    """
    
    def __init__(self):
        """Initialize the evaluator with task-specific keywords."""
        
        # Task-specific quality indicators
        self.task_keywords = {
            "Question Answering": [
                "answer", "because", "therefore", "specifically", "exactly",
                "result", "conclusion", "fact", "evidence", "reason"
            ],
            "Summarization": [
                "summary", "main", "key", "important", "overall", "primarily",
                "essentially", "briefly", "in short", "highlights"
            ],
            "Explanation": [
                "first", "second", "step", "because", "reason", "example",
                "means", "understand", "process", "explain", "how", "why"
            ],
            "Code Generation": [
                "function", "class", "def", "return", "import", "variable",
                "method", "parameter", "loop", "if", "else"
            ]
        }
    
    def evaluate_response(self, response: str, prompt: str, task_type: str) -> Dict[str, float]:
        """
        Evaluate a response using multiple deterministic metrics.
        
        Args:
            response: The generated response text
            prompt: The prompt that generated this response
            task_type: Type of task
            
        Returns:
            Dictionary of individual scores and total score
        """
        scores = {}
        
        # Metric 1: Length and completeness (0-25 points)
        scores['length_score'] = self._score_length(response, task_type)
        
        # Metric 2: Keyword relevance (0-25 points)
        scores['keyword_score'] = self._score_keywords(response, task_type)
        
        # Metric 3: Structure and formatting (0-25 points)
        scores['structure_score'] = self._score_structure(response, task_type)
        
        # Metric 4: Prompt alignment (0-25 points)
        scores['alignment_score'] = self._score_prompt_alignment(response, prompt)
        
        # Calculate total score (0-100)
        scores['total_score'] = sum([
            scores['length_score'],
            scores['keyword_score'],
            scores['structure_score'],
            scores['alignment_score']
        ])
        
        return scores
    
    def _score_length(self, response: str, task_type: str) -> float:
        """
        Score based on response length appropriateness.
        Different tasks have different optimal length ranges.
        
        Args:
            response: Response text
            task_type: Task type
            
        Returns:
            Score from 0-25
        """
        word_count = len(response.split())
        
        # Define optimal word count ranges for each task type
        optimal_ranges = {
            "Question Answering": (30, 200),
            "Summarization": (50, 150),
            "Explanation": (100, 300),
            "Code Generation": (50, 400)
        }
        
        min_words, max_words = optimal_ranges.get(task_type, (50, 200))
        
        if word_count < min_words * 0.5:
            # Too short
            return 5.0
        elif word_count < min_words:
            # Slightly short
            return 15.0
        elif min_words <= word_count <= max_words:
            # Optimal length
            return 25.0
        elif word_count <= max_words * 1.5:
            # Slightly long
            return 20.0
        else:
            # Too long
            return 10.0
    
    def _score_keywords(self, response: str, task_type: str) -> float:
        """
        Score based on presence of task-relevant keywords.
        
        Args:
            response: Response text
            task_type: Task type
            
        Returns:
            Score from 0-25
        """
        keywords = self.task_keywords.get(task_type, [])
        
        if not keywords:
            return 15.0  # Neutral score if no keywords defined
        
        response_lower = response.lower()
        
        # Count how many keywords appear
        keyword_count = sum(1 for kw in keywords if kw in response_lower)
        
        # Calculate percentage of keywords present
        keyword_percentage = keyword_count / len(keywords)
        
        # Convert to score (0-25)
        score = keyword_percentage * 25
        
        return min(score, 25.0)
    
    def _score_structure(self, response: str, task_type: str) -> float:
        """
        Score based on response structure and formatting quality.
        
        Args:
            response: Response text
            task_type: Task type
            
        Returns:
            Score from 0-25
        """
        score = 0.0
        
        # Check for proper sentence structure (sentences end with punctuation)
        sentences = re.split(r'[.!?]+', response)
        valid_sentences = [s for s in sentences if s.strip() and len(s.split()) > 3]
        
        if len(valid_sentences) >= 2:
            score += 8.0
        
        # Check for paragraphs or line breaks (indicates organization)
        paragraphs = response.split('\n\n')
        if len(paragraphs) > 1:
            score += 5.0
        
        # Check for lists or bullet points (good for structured info)
        if re.search(r'(\n\s*[-*•]\s+|\n\s*\d+\.\s+)', response):
            score += 5.0
        
        # Check for code blocks (important for code generation)
        if task_type == "Code Generation":
            if '```' in response or '    ' in response:  # Code blocks or indentation
                score += 7.0
        
        # Check for proper capitalization
        if response and response[0].isupper():
            score += 5.0
        
        return min(score, 25.0)
    
    def _score_prompt_alignment(self, response: str, prompt: str) -> float:
        """
        Score based on how well the response aligns with the prompt.
        Measures keyword overlap between prompt and response.
        
        Args:
            response: Response text
            prompt: Original prompt
            
        Returns:
            Score from 0-25
        """
        # Extract meaningful words from prompt (remove stop words)
        stop_words = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
            'could', 'can', 'may', 'might', 'must', 'to', 'of', 'in', 'on', 'at',
            'for', 'with', 'about', 'as', 'by', 'from', 'and', 'or', 'but', 'not'
        }
        
        prompt_words = set(
            word.lower() 
            for word in re.findall(r'\b\w+\b', prompt)
            if word.lower() not in stop_words and len(word) > 2
        )
        
        response_lower = response.lower()
        
        # Count how many prompt words appear in response
        matching_words = sum(1 for word in prompt_words if word in response_lower)
        
        if not prompt_words:
            return 15.0  # Neutral score if no meaningful words in prompt
        
        # Calculate overlap percentage
        overlap_percentage = matching_words / len(prompt_words)
        
        # Convert to score (0-25)
        score = overlap_percentage * 25
        
        return min(score, 25.0)
    
    def compare_and_select_best(self, evaluation_results: List[Dict]) -> Dict:
        """
        Compare all evaluated responses and select the best one.
        
        Args:
            evaluation_results: List of evaluation result dictionaries
                Each dict should have 'prompt', 'response', and 'scores' keys
                
        Returns:
            Dictionary with the best result and comparison data
        """
        if not evaluation_results:
            raise ValueError("No evaluation results to compare")
        
        # Find the result with the highest total score
        best_result = max(evaluation_results, key=lambda x: x['scores']['total_score'])
        
        # Create explanation of why this prompt won
        explanation = self._generate_explanation(best_result, evaluation_results)
        
        return {
            'best_prompt': best_result['prompt'],
            'best_response': best_result['response'],
            'best_scores': best_result['scores'],
            'explanation': explanation,
            'all_scores': [r['scores']['total_score'] for r in evaluation_results]
        }
    
    def _generate_explanation(self, best_result: Dict, all_results: List[Dict]) -> str:
        """
        Generate an explanation of why the selected prompt performed best.
        
        Args:
            best_result: The highest-scoring result
            all_results: All evaluation results
            
        Returns:
            Human-readable explanation string
        """
        best_scores = best_result['scores']
        
        # Identify the strongest metric
        metric_names = {
            'length_score': 'response completeness',
            'keyword_score': 'task-relevant keywords',
            'structure_score': 'structure and formatting',
            'alignment_score': 'prompt alignment'
        }
        
        strongest_metric = max(
            ['length_score', 'keyword_score', 'structure_score', 'alignment_score'],
            key=lambda m: best_scores[m]
        )
        
        explanation_parts = []
        
        explanation_parts.append(
            f"This optimized prompt achieved the highest overall score ({best_scores['total_score']:.1f}/100)."
        )
        
        explanation_parts.append(
            f"It excelled particularly in {metric_names[strongest_metric]} "
            f"({best_scores[strongest_metric]:.1f}/25)."
        )
        
        # Compare to original
        original_score = all_results[0]['scores']['total_score']
        improvement = best_scores['total_score'] - original_score
        
        if improvement > 5:
            explanation_parts.append(
                f"The optimization improved the response quality by {improvement:.1f} points "
                f"compared to the original prompt."
            )
        elif improvement > 0:
            explanation_parts.append(
                "The optimization resulted in a slightly better response."
            )
        else:
            explanation_parts.append(
                "This variation performed best among the generated options."
            )
        
        return " ".join(explanation_parts)
