"""
Simple test script to verify the system components work correctly.
Run this after setting up your .env file to test the pipeline.
"""

import os
from dotenv import load_dotenv

from src.gemini_client import GeminiClient
from src.prompt_optimizer import PromptOptimizer
from src.response_generator import ResponseGenerator
from src.evaluator import ResponseEvaluator
from src.storage import ResultStorage


def test_system():
    """Test all system components."""
    
    print("=" * 60)
    print("Testing Automated Prompt Optimization System")
    print("=" * 60)
    
    # Load environment
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found in .env file")
        print("Please create a .env file with your API key.")
        return False
    
    print("✅ API key loaded")
    
    try:
        # Test 1: Initialize client
        print("\n[Test 1] Initializing Gemini client...")
        client = GeminiClient(api_key)
        print("✅ Client initialized")
        
        # Test 2: Simple generation
        print("\n[Test 2] Testing basic text generation...")
        response = client.generate_text("Say 'Hello, World!' in exactly 2 words.", temperature=0.5)
        print(f"✅ Response received: {response[:50]}...")
        
        # Test 3: Prompt optimizer
        print("\n[Test 3] Testing prompt optimizer...")
        optimizer = PromptOptimizer(client)
        test_prompt = "explain AI"
        variations = optimizer.generate_variations(test_prompt, "Explanation", num_variations=2)
        print(f"✅ Generated {len(variations)} variations")
        for i, var in enumerate(variations, 1):
            print(f"   Variation {i}: {var[:60]}...")
        
        # Test 4: Response generator
        print("\n[Test 4] Testing response generator...")
        generator = ResponseGenerator(client)
        all_responses = generator.generate_all_responses(test_prompt, variations[:1])
        print(f"✅ Generated responses for {len(all_responses['variations']) + 1} prompts")
        
        # Test 5: Evaluator
        print("\n[Test 5] Testing evaluator...")
        evaluator = ResponseEvaluator()
        
        eval_results = []
        
        # Evaluate original
        original_scores = evaluator.evaluate_response(
            all_responses['original']['response'],
            all_responses['original']['prompt'],
            "Explanation"
        )
        eval_results.append({
            'prompt': all_responses['original']['prompt'],
            'response': all_responses['original']['response'],
            'scores': original_scores
        })
        
        # Evaluate variation
        for var_data in all_responses['variations']:
            scores = evaluator.evaluate_response(
                var_data['response'],
                var_data['prompt'],
                "Explanation"
            )
            eval_results.append({
                'prompt': var_data['prompt'],
                'response': var_data['response'],
                'scores': scores
            })
        
        print(f"✅ Evaluated {len(eval_results)} responses")
        print(f"   Original score: {eval_results[0]['scores']['total_score']:.1f}/100")
        print(f"   Optimized score: {eval_results[1]['scores']['total_score']:.1f}/100")
        
        # Test 6: Selection
        print("\n[Test 6] Testing best prompt selection...")
        best = evaluator.compare_and_select_best(eval_results)
        print(f"✅ Best prompt selected (score: {best['best_scores']['total_score']:.1f}/100)")
        print(f"   Explanation: {best['explanation'][:80]}...")
        
        # Test 7: Storage
        print("\n[Test 7] Testing storage...")
        storage = ResultStorage()
        storage.save_optimization_result({
            'task_type': 'Explanation',
            'original_prompt': test_prompt,
            'optimized_prompt': best['best_prompt'],
            'original_score': eval_results[0]['scores']['total_score'],
            'optimized_score': best['best_scores']['total_score'],
            'improvement': best['best_scores']['total_score'] - eval_results[0]['scores']['total_score']
        })
        print("✅ Result saved to storage")
        
        stats = storage.get_statistics()
        print(f"   Total optimizations: {stats['total_optimizations']}")
        
        print("\n" + "=" * 60)
        print("🎉 All tests passed! System is working correctly.")
        print("=" * 60)
        print("\nYou can now run the web app with:")
        print("  streamlit run app.py")
        
        return True
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_system()
    exit(0 if success else 1)
