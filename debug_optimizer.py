"""Debug script to see what's happening with prompt optimization"""

import os
from dotenv import load_dotenv
from src.gemini_client import GeminiClient
from src.prompt_optimizer import PromptOptimizer

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
client = GeminiClient(api_key)

# Test the raw prompt that goes to Gemini
test_prompt = "explain ML"
task_type = "Explanation"
num_variations = 4

guidelines = """- Specify the complexity level (beginner, intermediate, expert)
- Request examples if needed
- Ask for step-by-step breakdown if appropriate
- Indicate preferred depth of explanation"""

optimization_prompt = f"""You are a prompt engineering expert. Your task is to generate {num_variations} improved variations of a user's prompt.

Original Prompt: "{test_prompt}"

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

print("="*80)
print("SENDING THIS PROMPT TO GEMINI:")
print("="*80)
print(optimization_prompt)
print("\n" + "="*80)
print("GEMINI'S RAW RESPONSE:")
print("="*80)

response = client.generate_text(optimization_prompt, temperature=0.8)
print(response)

print("\n" + "="*80)
print("PARSED VARIATIONS:")
print("="*80)

optimizer = PromptOptimizer(client)
variations = optimizer._parse_variations(response)
print(f"Found {len(variations)} variations:")
for i, v in enumerate(variations, 1):
    print(f"\n{i}. {v}")

print("\n" + "="*80)
print("USING generate_variations method:")
print("="*80)
variations = optimizer.generate_variations(test_prompt, task_type, num_variations=4)
print(f"Generated {len(variations)} variations:")
for i, v in enumerate(variations, 1):
    print(f"\n{i}. {v}")
