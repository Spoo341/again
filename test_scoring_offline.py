"""Test scoring logic without calling API"""

from src.evaluator import ResponseEvaluator

evaluator = ResponseEvaluator()

# Simulate simple original prompt and response
simple_prompt = "what is AI"
simple_response = "AI is artificial intelligence. It's technology that allows computers to think."

# Simulate detailed optimized prompt and response  
detailed_prompt = "Please provide a comprehensive answer to: What is artificial intelligence? Include: (1) a clear definition, (2) key characteristics, (3) real-world applications with specific examples, and (4) current limitations. Structure your response with clear sections."
detailed_response = """Artificial Intelligence (AI) is a field of computer science focused on creating intelligent machines capable of performing tasks that typically require human intelligence.

**Definition and Core Concept:**
Specifically, AI refers to computer systems designed to perceive their environment, process information, learn from experience, and make decisions to achieve specific goals. Therefore, AI systems can adapt and improve their performance over time through machine learning algorithms.

**Key Characteristics:**
The primary characteristics of AI include pattern recognition, natural language processing, problem-solving capabilities, and autonomous decision-making. Research has shown that modern AI systems excel at processing large datasets to identify trends and make predictions.

**Real-World Applications:**
1. Healthcare: AI algorithms analyze medical images to detect diseases with high accuracy
2. Finance: Automated trading systems use AI to make investment decisions based on market data
3. Transportation: Self-driving cars employ AI for navigation and safety

**Current Limitations:**
Despite significant progress, AI systems face limitations in common sense reasoning, emotional intelligence, and explaining their decision-making process. Studies indicate that AI still requires substantial human oversight in critical applications.

In conclusion, AI represents a transformative technology with evidence of growing capabilities, though ethical considerations and technical constraints remain important factors."""

print("="*80)
print("ORIGINAL (SIMPLE) PROMPT SCORING")
print("="*80)
print(f"Prompt: '{simple_prompt}'")
print(f"Prompt length: {len(simple_prompt.split())} words")
print(f"Response length: {len(simple_response.split())} words")

original_scores = evaluator.evaluate_response(
    simple_response,
    simple_prompt,
    "Question Answering"
)

print(f"\nScores:")
print(f"  Length: {original_scores['length_score']:.1f}/25")
print(f"  Keywords: {original_scores['keyword_score']:.1f}/25")
print(f"  Structure: {original_scores['structure_score']:.1f}/25")
print(f"  Alignment: {original_scores['alignment_score']:.1f}/25")
print(f"  TOTAL: {original_scores['total_score']:.1f}/100")

print("\n" + "="*80)
print("OPTIMIZED (DETAILED) PROMPT SCORING")
print("="*80)
print(f"Prompt: '{detailed_prompt[:80]}...'")
print(f"Prompt length: {len(detailed_prompt.split())} words")
print(f"Response length: {len(detailed_response.split())} words")

optimized_scores = evaluator.evaluate_response(
    detailed_response,
    detailed_prompt,
    "Question Answering"
)

print(f"\nScores:")
print(f"  Length: {optimized_scores['length_score']:.1f}/25")
print(f"  Keywords: {optimized_scores['keyword_score']:.1f}/25")
print(f"  Structure: {optimized_scores['structure_score']:.1f}/25")
print(f"  Alignment: {optimized_scores['alignment_score']:.1f}/25")
print(f"  TOTAL: {optimized_scores['total_score']:.1f}/100")

improvement = optimized_scores['total_score'] - original_scores['total_score']
improvement_pct = (improvement / original_scores['total_score'] * 100) if original_scores['total_score'] > 0 else 0

print("\n" + "="*80)
print("IMPROVEMENT ANALYSIS")
print("="*80)
print(f"Absolute improvement: +{improvement:.1f} points")
print(f"Percentage improvement: {improvement_pct:.1f}%")

if improvement_pct >= 90:
    print("\n✓ EXCELLENT: 90%+ improvement (target achieved!)")
elif improvement_pct >= 50:
    print("\n✓ GOOD: 50%+ improvement")
elif improvement_pct >= 20:
    print("\n⚠️  MODERATE: 20-50% improvement (could be better)")
else:
    print("\n❌ LOW: <20% improvement (needs adjustment)")

print("\n" + "="*80)
print("SCORE BREAKDOWN BY METRIC:")
print("="*80)
print(f"Length:    Simple: {original_scores['length_score']:.1f}  →  Detailed: {optimized_scores['length_score']:.1f}  (Δ{optimized_scores['length_score']-original_scores['length_score']:+.1f})")
print(f"Keywords:  Simple: {original_scores['keyword_score']:.1f}  →  Detailed: {optimized_scores['keyword_score']:.1f}  (Δ{optimized_scores['keyword_score']-original_scores['keyword_score']:+.1f})")
print(f"Structure: Simple: {original_scores['structure_score']:.1f}  →  Detailed: {optimized_scores['structure_score']:.1f}  (Δ{optimized_scores['structure_score']-original_scores['structure_score']:+.1f})")
print(f"Alignment: Simple: {original_scores['alignment_score']:.1f}  →  Detailed: {optimized_scores['alignment_score']:.1f}  (Δ{optimized_scores['alignment_score']-original_scores['alignment_score']:+.1f})")
