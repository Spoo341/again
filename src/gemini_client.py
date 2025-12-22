"""
Gemini API Client Module
Handles all interactions with Google's Gemini API.
"""

import os
import google.generativeai as genai
from typing import Optional


class GeminiClient:
    """Client for interacting with Google's Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: Gemini API key. If None, will try to read from environment.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Please set it in your .env file or pass it directly."
            )
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Use gemini-pro model (free tier)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_text(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1024) -> str:
        """
        Generate text using Gemini API.
        
        Args:
            prompt: The input prompt
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated text response
        """
        try:
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
        
        except Exception as e:
            print(f"Error generating text: {e}")
            raise
    
    def generate_text_batch(self, prompts: list[str], temperature: float = 0.7, max_tokens: int = 1024) -> list[str]:
        """
        Generate text for multiple prompts with identical settings.
        
        Args:
            prompts: List of input prompts
            temperature: Sampling temperature
            max_tokens: Maximum tokens per response
            
        Returns:
            List of generated responses
        """
        responses = []
        for prompt in prompts:
            response = self.generate_text(prompt, temperature, max_tokens)
            responses.append(response)
        
        return responses
