"""Test to see actual scoring behavior"""

import os
from dotenv import load_dotenv
from src.gemini_client import GeminiClient
from src.prompt_optimizer import PromptOptimizer
from src.response_generator import ResponseGenerator
from src.evaluator import ResponseEvaluator

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
client = GeminiClient(api_key)
optimizer = PromptOptimizer(client)
generator = ResponseGenerator(client)
evaluator = ResponseEvaluator()

# Test with a very simple prompt
test_prompt = "what is AI"
task_type = "Question Answering"

print("="*80)
print(f"Testing: '{test_prompt}'")
print("="*80)

# Generate variations
print("\nGenerating variations...")
variations = optimizer.generate_variations(test_prompt, task_type, num_variations=4)
print(f"Got {len(variations)} variations")

# Generate responses
print("\nGenerating responses...")
all_responses = generator.generate_all_responses(test_prompt, variations)

print(f"\nOriginal response ({len(all_responses['original']['response'])} chars):")
print(all_responses['original']['response'][:300])

# Evaluate original
original_scores = evaluator.evaluate_response(
    all_responses['original']['response'],
    all_responses['original']['prompt'],
    task_type
)

print("\n" + "="*80)
print("ORIGINAL PROMPT SCORING:")
print("="*80)
print(f"Prompt: '{test_prompt}'")
print(f"Response length: {len(all_responses['original']['response'])} chars")
print(f"\nScores:")
print(f"  Length: {original_scores['length_score']:.1f}/25")
print(f"  Keywords: {original_scores['keyword_score']:.1f}/25")
print(f"  Structure: {original_scores['structure_score']:.1f}/25")
print(f"  Alignment: {original_scores['alignment_score']:.1f}/25")
print(f"  TOTAL: {original_scores['total_score']:.1f}/100")

# Evaluate best variation
best_var_idx = 0
best_var_score = 0

for idx, var_data in enumerate(all_responses['variations']):
    scores = evaluator.evaluate_response(
        var_data['response'],
        var_data['prompt'],
        task_type
    )
    if scores['total_score'] > best_var_score:
        best_var_score = scores['total_score']
        best_var_idx = idx

best_var = all_responses['variations'][best_var_idx]
best_scores = evaluator.evaluate_response(
    best_var['response'],
    best_var['prompt'],
    task_type
)

print("\n" + "="*80)
print("BEST OPTIMIZED PROMPT SCORING:")
print("="*80)
print(f"Prompt: '{best_var['prompt'][:100]}...'")
print(f"Response length: {len(best_var['response'])} chars")
print(f"\nScores:")
print(f"  Length: {best_scores['length_score']:.1f}/25")
print(f"  Keywords: {best_scores['keyword_score']:.1f}/25")
print(f"  Structure: {best_scores['structure_score']:.1f}/25")
print(f"  Alignment: {best_scores['alignment_score']:.1f}/25")
print(f"  TOTAL: {best_scores['total_score']:.1f}/100")

improvement = best_scores['total_score'] - original_scores['total_score']
improvement_pct = (improvement / original_scores['total_score'] * 100) if original_scores['total_score'] > 0 else 0

print("\n" + "="*80)
print("IMPROVEMENT:")
print("="*80)
print(f"Absolute: +{improvement:.1f} points")
print(f"Percentage: {improvement_pct:.1f}%")

if improvement_pct < 20:
    print("\n⚠️  WARNING: Improvement too low! Should be 50%+")
elif improvement_pct < 50:
    print("\n⚠️  Improvement is moderate but could be better")
else:
    print("\n✓ Good improvement!")
