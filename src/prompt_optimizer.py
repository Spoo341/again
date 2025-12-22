"""
Prompt Optimizer Module
Generates improved variations of user prompts using Gemini.
"""

from .gemini_client import GeminiClient


class PromptOptimizer:
    """Generates optimized prompt variations based on task type."""
    
    def __init__(self, client: GeminiClient):
        """
        Initialize the prompt optimizer.
        
        Args:
            client: Initialized GeminiClient instance
        """
        self.client = client
        
        # Task-specific optimization guidelines
        self.task_guidelines = {
            "Question Answering": (
                "- Be specific about what information is needed\n"
                "- Specify the desired format of the answer\n"
                "- Include relevant context\n"
                "- Request concise or detailed answers as appropriate"
            ),
            "Summarization": (
                "- Specify the desired length of the summary\n"
                "- Indicate key points to focus on\n"
                "- Request specific format (bullet points, paragraph, etc.)\n"
                "- Mention the target audience if relevant"
            ),
            "Explanation": (
                "- Specify the complexity level (beginner, intermediate, expert)\n"
                "- Request examples if needed\n"
                "- Ask for step-by-step breakdown if appropriate\n"
                "- Indicate preferred depth of explanation"
            ),
            "Code Generation": (
                "- Specify the programming language\n"
                "- Include input/output requirements\n"
                "- Mention any constraints or requirements\n"
                "- Request comments or documentation if needed"
            )
        }
    
    def generate_variations(self, original_prompt: str, task_type: str, num_variations: int = 4) -> list[str]:
        """
        Generate improved prompt variations.
        
        Args:
            original_prompt: The user's original prompt
            task_type: Type of task (Question Answering, Summarization, etc.)
            num_variations: Number of variations to generate (default 4)
            
        Returns:
            List of improved prompt variations
        """
        guidelines = self.task_guidelines.get(task_type, "")
        
        optimization_prompt = f"""You are a prompt engineering expert. Your task is to generate {num_variations} improved variations of a user's prompt.

Original Prompt: "{original_prompt}"

Task Type: {task_type}

Optimization Guidelines for {task_type}:
{guidelines}

Requirements:
1. Generate exactly {num_variations} distinct improved variations
2. Each variation should be clear, specific, and well-structured
3. Maintain the original intent but enhance clarity and specificity
4. Add appropriate constraints and formatting instructions
5. Each variation should be different from the others

Output Format:
Provide each variation on a separate line, numbered as:
VARIATION 1: [improved prompt]
VARIATION 2: [improved prompt]
VARIATION 3: [improved prompt]
VARIATION 4: [improved prompt]

Do not include any other text or explanations."""

        try:
            response = self.client.generate_text(optimization_prompt, temperature=0.8)
            
            # Parse the variations from the response
            variations = self._parse_variations(response)
            
            # Ensure we have the expected number of variations
            if len(variations) < num_variations:
                print(f"Warning: Expected {num_variations} variations, got {len(variations)}")
            
            return variations[:num_variations]
        
        except Exception as e:
            print(f"Error generating variations: {e}")
            # Fallback: return the original prompt with basic improvements
            return [self._create_fallback_variation(original_prompt, task_type)]
    
    def _parse_variations(self, response: str) -> list[str]:
        """
        Parse prompt variations from the LLM response.
        
        Args:
            response: Raw text response from Gemini
            
        Returns:
            List of extracted prompt variations
        """
        variations = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            # Look for patterns like "VARIATION 1:", "1.", "1:", etc.
            if line and any(marker in line.upper() for marker in ['VARIATION', '1:', '2:', '3:', '4:', '5:']):
                # Extract the prompt text after the marker
                for separator in [':', '.']:
                    if separator in line:
                        parts = line.split(separator, 1)
                        if len(parts) > 1:
                            variation_text = parts[1].strip()
                            # Remove quotes if present
                            variation_text = variation_text.strip('"\'')
                            if variation_text:
                                variations.append(variation_text)
                                break
        
        return variations
    
    def _create_fallback_variation(self, original_prompt: str, task_type: str) -> str:
        """
        Create a basic improved variation as fallback.
        
        Args:
            original_prompt: Original user prompt
            task_type: Task type
            
        Returns:
            A basic improved prompt
        """
        if task_type == "Question Answering":
            return f"Please provide a detailed and accurate answer to the following question: {original_prompt}"
        elif task_type == "Summarization":
            return f"Please provide a concise summary of: {original_prompt}"
        elif task_type == "Explanation":
            return f"Please provide a clear explanation of: {original_prompt}"
        elif task_type == "Code Generation":
            return f"Please generate well-commented code for: {original_prompt}"
        else:
            return f"Please help with the following: {original_prompt}"
