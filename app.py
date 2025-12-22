"""
Streamlit Web Application for Automated Prompt Optimization
Interactive UI for improving user prompts using LLM-generated variations and metric-based evaluation.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime

from src.gemini_client import GeminiClient
from src.prompt_optimizer import PromptOptimizer
from src.response_generator import ResponseGenerator
from src.evaluator import ResponseEvaluator
from src.storage import ResultStorage


# Load environment variables
load_dotenv()


def initialize_system():
    """Initialize all system components."""
    try:
        # Initialize Gemini client
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("⚠️ GEMINI_API_KEY not found. Please set it in your .env file.")
            st.info("Get your free API key from: https://makersuite.google.com/app/apikey")
            st.stop()
        
        client = GeminiClient(api_key)
        optimizer = PromptOptimizer(client)
        generator = ResponseGenerator(client)
        evaluator = ResponseEvaluator()
        storage = ResultStorage()
        
        return optimizer, generator, evaluator, storage
    
    except Exception as e:
        st.error(f"Error initializing system: {e}")
        st.stop()


def run_optimization_pipeline(user_prompt, task_type, optimizer, generator, evaluator, storage):
    """
    Execute the complete optimization pipeline.
    
    Args:
        user_prompt: Original user prompt
        task_type: Selected task type
        optimizer: PromptOptimizer instance
        generator: ResponseGenerator instance
        evaluator: ResponseEvaluator instance
        storage: ResultStorage instance
        
    Returns:
        Dictionary with optimization results
    """
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Generate prompt variations
        status_text.text("🔄 Step 1/4: Generating optimized prompt variations...")
        progress_bar.progress(10)
        
        variations = optimizer.generate_variations(user_prompt, task_type, num_variations=4)
        
        if not variations:
            st.error("Failed to generate prompt variations. Please try again.")
            return None
        
        st.success(f"✅ Generated {len(variations)} optimized prompts")
        progress_bar.progress(25)
        
        # Step 2: Generate responses
        status_text.text("🔄 Step 2/4: Generating responses for all prompts...")
        
        all_responses = generator.generate_all_responses(user_prompt, variations)
        
        st.success(f"✅ Generated {len(variations) + 1} responses")
        progress_bar.progress(50)
        
        # Step 3: Evaluate all responses
        status_text.text("🔄 Step 3/4: Evaluating responses using metric-based scoring...")
        
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
        
        # Evaluate all variations
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
        
        st.success("✅ Evaluation complete")
        progress_bar.progress(75)
        
        # Step 4: Select best prompt
        status_text.text("🔄 Step 4/4: Selecting optimal prompt...")
        
        best_result = evaluator.compare_and_select_best(evaluation_results)
        
        progress_bar.progress(100)
        status_text.text("✅ Optimization complete!")
        
        # Save result to storage
        storage.save_optimization_result({
            'timestamp': datetime.now().isoformat(),
            'task_type': task_type,
            'original_prompt': user_prompt,
            'optimized_prompt': best_result['best_prompt'],
            'original_score': evaluation_results[0]['scores']['total_score'],
            'optimized_score': best_result['best_scores']['total_score'],
            'improvement': best_result['best_scores']['total_score'] - evaluation_results[0]['scores']['total_score']
        })
        
        return {
            'best_result': best_result,
            'evaluation_results': evaluation_results,
            'variations': variations
        }
    
    except Exception as e:
        st.error(f"Error during optimization: {e}")
        return None


def display_results(results):
    """Display optimization results in the UI."""
    
    best = results['best_result']
    
    # Main result section
    st.markdown("---")
    st.markdown("## 🎯 Optimization Results")
    
    # Score improvement
    original_score = results['evaluation_results'][0]['scores']['total_score']
    optimized_score = best['best_scores']['total_score']
    improvement = optimized_score - original_score
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Original Score", f"{original_score:.1f}/100")
    with col2:
        st.metric("Optimized Score", f"{optimized_score:.1f}/100", f"+{improvement:.1f}")
    with col3:
        improvement_pct = (improvement / original_score * 100) if original_score > 0 else 0
        st.metric("Improvement", f"{improvement_pct:.1f}%")
    
    # Optimized prompt
    st.markdown("### ✨ Optimized Prompt")
    st.info(best['best_prompt'])
    
    # Final response
    st.markdown("### 📝 Improved Response")
    st.success(best['best_response'])
    
    # Explanation
    st.markdown("### 💡 Why This Prompt Performed Better")
    st.write(best['explanation'])
    
    # Detailed scoring breakdown (collapsible)
    with st.expander("📊 View Detailed Score Breakdown"):
        scores = best['best_scores']
        
        st.markdown("**Individual Metric Scores:**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Length & Completeness", f"{scores['length_score']:.1f}/25")
            st.metric("Keyword Relevance", f"{scores['keyword_score']:.1f}/25")
        with col2:
            st.metric("Structure & Formatting", f"{scores['structure_score']:.1f}/25")
            st.metric("Prompt Alignment", f"{scores['alignment_score']:.1f}/25")
    
    # Show all variations (collapsible)
    with st.expander("🔍 View All Generated Variations"):
        for idx, var in enumerate(results['variations'], 1):
            st.markdown(f"**Variation {idx}:**")
            st.text(var)
            st.markdown("---")


def main():
    """Main application entry point."""
    
    # Page configuration
    st.set_page_config(
        page_title="Automated Prompt Optimization",
        page_icon="🚀",
        layout="wide"
    )
    
    # Title and description
    st.title("🚀 Automated Prompt Optimization")
    st.markdown("""
    ### Using LLM-Generated Variations and Metric-Based Evaluation
    
    This system automatically improves your prompts through systematic optimization and 
    deterministic evaluation—no prompt engineering expertise required!
    """)
    
    st.markdown("---")
    
    # Initialize system components
    optimizer, generator, evaluator, storage = initialize_system()
    
    # Sidebar for statistics
    with st.sidebar:
        st.markdown("## 📊 System Statistics")
        
        stats = storage.get_statistics()
        st.metric("Total Optimizations", stats['total_optimizations'])
        st.metric("Average Improvement", f"{stats['average_improvement']:.1f} pts")
        
        if stats['task_type_counts']:
            st.markdown("**Task Type Distribution:**")
            for task, count in stats['task_type_counts'].items():
                st.write(f"• {task}: {count}")
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        This system uses:
        - **Google Gemini** (free tier)
        - **Rule-based metrics** (no subjective LLM rating)
        - **Systematic optimization** pipeline
        """)
        
        if st.button("Clear History"):
            storage.clear_results()
            st.success("History cleared!")
            st.rerun()
    
    # Main input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_prompt = st.text_area(
            "Enter your prompt:",
            placeholder="Example: Explain machine learning",
            height=150,
            help="Enter any prompt you'd like to optimize"
        )
    
    with col2:
        task_type = st.selectbox(
            "Select task type:",
            options=[
                "Question Answering",
                "Summarization",
                "Explanation",
                "Code Generation"
            ],
            help="Choose the type of task for task-specific optimization"
        )
        
        st.markdown("")
        st.markdown("")
        optimize_button = st.button("🚀 Optimize My Prompt", type="primary", use_container_width=True)
    
    # Run optimization when button is clicked
    if optimize_button:
        if not user_prompt or len(user_prompt.strip()) < 5:
            st.warning("⚠️ Please enter a prompt with at least 5 characters.")
        else:
            # Run the pipeline
            results = run_optimization_pipeline(
                user_prompt.strip(),
                task_type,
                optimizer,
                generator,
                evaluator,
                storage
            )
            
            # Display results
            if results:
                display_results(results)
    
    # Instructions section
    with st.expander("📖 How to Use This System"):
        st.markdown("""
        ### Step-by-Step Guide:
        
        1. **Enter Your Prompt**: Type your original prompt in the text area
        2. **Select Task Type**: Choose the type of task from the dropdown:
           - **Question Answering**: For factual questions
           - **Summarization**: For condensing information
           - **Explanation**: For understanding concepts
           - **Code Generation**: For programming tasks
        3. **Click Optimize**: Press the "Optimize My Prompt" button
        4. **View Results**: See your optimized prompt and improved response
        
        ### How It Works:
        
        The system follows a systematic 4-step pipeline:
        
        1. **Variation Generation**: Creates 4 improved versions of your prompt
        2. **Response Generation**: Generates responses for all prompts with identical settings
        3. **Metric-Based Evaluation**: Scores each response using deterministic metrics:
           - Length & completeness
           - Task-relevant keywords
           - Structure & formatting
           - Prompt alignment
        4. **Selection**: Chooses the highest-scoring prompt and response
        
        ### Key Features:
        
        - ✅ No prompt engineering expertise needed
        - ✅ Systematic, repeatable process
        - ✅ Objective, metric-based evaluation
        - ✅ Clear explanations of improvements
        - ✅ Result history and statistics
        """)


if __name__ == "__main__":
    main()
