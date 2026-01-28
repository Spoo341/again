"""Complete workflow debug - simulates what happens in the UI"""

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

test_prompt = "what is python"
task_type = "Question Answering"

print("="*80)
print(f"Testing full workflow with prompt: '{test_prompt}'")
print(f"Task type: {task_type}")
print("="*80)

# Step 1: Generate variations
print("\nSTEP 1: Generating variations...")
variations = optimizer.generate_variations(test_prompt, task_type, num_variations=4)
print(f"Generated {len(variations)} variations:")
for i, v in enumerate(variations, 1):
    print(f"\n{i}. {v[:100]}...")

# Step 2: Generate responses
print("\n" + "="*80)
print("STEP 2: Generating responses...")
print("="*80)
all_responses = generator.generate_all_responses(test_prompt, variations)

print(f"\nOriginal response ({len(all_responses['original']['response'])} chars):")
print(all_responses['original']['response'][:200] + "...")

print(f"\nVariation responses:")
for i, var_data in enumerate(all_responses['variations'], 1):
    print(f"\n{i}. Response length: {len(var_data['response'])} chars")
    print(f"   Preview: {var_data['response'][:150]}...")

# Step 3: Evaluate all responses
print("\n" + "="*80)
print("STEP 3: Evaluating all responses...")
print("="*80)

evaluation_results = []

# Evaluate original
original_scores = evaluator.evaluate_response(
    all_responses['original']['response'],
    all_responses['original']['prompt'],
    task_type
)

evaluation_results.append({
    'prompt': all_responses['original']['prompt'],
    'response': all_responses['original']['response'],
    'scores': original_scores,
    'is_original': True
})

print(f"\nOriginal scores:")
print(f"  Length: {original_scores['length_score']:.1f}/25")
print(f"  Keywords: {original_scores['keyword_score']:.1f}/25")
print(f"  Structure: {original_scores['structure_score']:.1f}/25")
print(f"  Alignment: {original_scores['alignment_score']:.1f}/25")
print(f"  TOTAL: {original_scores['total_score']:.1f}/100")

# Evaluate variations
for idx, var_data in enumerate(all_responses['variations'], 1):
    scores = evaluator.evaluate_response(
        var_data['response'],
        var_data['prompt'],
        task_type
    )
    
    evaluation_results.append({
        'prompt': var_data['prompt'],
        'response': var_data['response'],
        'scores': scores,
        'is_original': False
    })
    
    print(f"\nVariation {idx} scores:")
    print(f"  Length: {scores['length_score']:.1f}/25")
    print(f"  Keywords: {scores['keyword_score']:.1f}/25")
    print(f"  Structure: {scores['structure_score']:.1f}/25")
    print(f"  Alignment: {scores['alignment_score']:.1f}/25")
    print(f"  TOTAL: {scores['total_score']:.1f}/100")

# Step 4: Select best
print("\n" + "="*80)
print("STEP 4: Selecting best...")
print("="*80)

best_result = evaluator.compare_and_select_best(evaluation_results)

print(f"\nBest prompt selected:")
print(f"Score: {best_result['best_scores']['total_score']:.1f}/100")
print(f"Is it the original? {best_result['best_prompt'] == test_prompt}")
print(f"\nBest prompt:")
print(best_result['best_prompt'])
print(f"\nExplanation:")
print(best_result['explanation'])

# Check if original won
if best_result['best_prompt'] == test_prompt:
    print("\n" + "!"*80)
    print("WARNING: Original prompt won! This is the issue the user is experiencing.")
    print("!"*80)
else:
    print("\n" + "="*80)
    print("✓ SUCCESS: An optimized variation won!")
    print("="*80)
