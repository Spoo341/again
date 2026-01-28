"""Test with different prompts to verify fix"""

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

test_cases = [
    ("explain ML", "Explanation"),
    ("what is blockchain", "Question Answering"),
    ("write sorting code", "Code Generation"),
]

for test_prompt, task_type in test_cases:
    print("=" * 80)
    print(f"Testing: '{test_prompt}' ({task_type})")
    print("=" * 80)
    
    # Generate variations
    variations = optimizer.generate_variations(test_prompt, task_type, num_variations=4)
    
    # Generate responses
    all_responses = generator.generate_all_responses(test_prompt, variations)
    
    # Evaluate
    evaluation_results = []
    
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
    
    for var_data in all_responses['variations']:
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
    
    # Select best
    best_result = evaluator.compare_and_select_best(evaluation_results)
    
    original_score = evaluation_results[0]['scores']['total_score']
    best_score = best_result['best_scores']['total_score']
    is_original = best_result['best_prompt'] == test_prompt
    
    print(f"\nOriginal score: {original_score:.1f}/100")
    print(f"Best score: {best_score:.1f}/100")
    print(f"Improvement: +{best_score - original_score:.1f}")
    print(f"Original won? {is_original}")
    
    if is_original:
        print("❌ FAIL: Original prompt won")
    else:
        print("✅ PASS: Optimized prompt won")
    
    print()

print("\n" + "=" * 80)
print("Testing complete!")
print("=" * 80)
