"""
Response Generator Module
Generates responses for all prompts using identical model settings.
"""

from .gemini_client import GeminiClient


class ResponseGenerator:
    """Generates responses for original and optimized prompts."""
    
    # Fixed generation parameters to ensure consistency
    TEMPERATURE = 0.7
    MAX_TOKENS = 1024
    
    def __init__(self, client: GeminiClient):
        """
        Initialize the response generator.
        
        Args:
            client: Initialized GeminiClient instance
        """
        self.client = client
    
    def generate_all_responses(self, original_prompt: str, optimized_prompts: list[str]) -> dict:
        """
        Generate responses for the original prompt and all optimized variations.
        Uses identical model settings for fair comparison.
        
        Args:
            original_prompt: The user's original prompt
            optimized_prompts: List of optimized prompt variations
            
        Returns:
            Dictionary mapping prompt to its response:
            {
                'original': {'prompt': str, 'response': str},
                'variations': [
                    {'prompt': str, 'response': str},
                    ...
                ]
            }
        """
        results = {
            'original': {},
            'variations': []
        }
        
        # Generate response for original prompt
        print("Generating response for original prompt...")
        original_response = self.client.generate_text(
            original_prompt,
            temperature=self.TEMPERATURE,
            max_tokens=self.MAX_TOKENS
        )
        
        results['original'] = {
            'prompt': original_prompt,
            'response': original_response
        }
        
        # Generate responses for all optimized prompts
        print(f"Generating responses for {len(optimized_prompts)} optimized prompts...")
        for idx, prompt in enumerate(optimized_prompts, 1):
            print(f"  Processing variation {idx}/{len(optimized_prompts)}...")
            response = self.client.generate_text(
                prompt,
                temperature=self.TEMPERATURE,
                max_tokens=self.MAX_TOKENS
            )
            
            results['variations'].append({
                'prompt': prompt,
                'response': response
            })
        
        return results
    
    def generate_single_response(self, prompt: str) -> str:
        """
        Generate a single response with standard settings.
        
        Args:
            prompt: The input prompt
            
        Returns:
            Generated response text
        """
        return self.client.generate_text(
            prompt,
            temperature=self.TEMPERATURE,
            max_tokens=self.MAX_TOKENS
        )
