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
        try:
            result_to_save = {
                'timestamp': datetime.now().isoformat(),
                'task_type': task_type,
                'original_prompt': user_prompt,
                'optimized_prompt': best_result['best_prompt'],
                'original_score': evaluation_results[0]['scores']['total_score'],
                'optimized_score': best_result['best_scores']['total_score'],
                'improvement': best_result['best_scores']['total_score'] - evaluation_results[0]['scores']['total_score']
            }
            print(f"📝 Attempting to save: {result_to_save}")
            print(f"📂 Storage object: {storage}")
            print(f"📂 Storage file path: {storage.results_file}")
            
            storage.save_optimization_result(result_to_save)
            
            print("✅ Successfully saved to storage")
            st.info(f"💾 Saved to {storage.results_file}")
        except Exception as save_error:
            print(f"❌ Error saving to storage: {save_error}")
            import traceback
            print(traceback.format_exc())
            st.error(f"Could not save history: {save_error}")
        
        return {
            'best_result': best_result,
            'evaluation_results': evaluation_results,
            'variations': variations
        }
    
    except Exception as e:
        st.error(f"Error during optimization: {e}")
        import traceback
        st.code(traceback.format_exc())
        print(f"FULL ERROR: {traceback.format_exc()}")
        return None


def display_results(results):
    """Display optimization results in the UI."""
    
    best = results['best_result']
    
    # Main result section
    st.markdown("")
    st.markdown("### Results")
    
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
    
    st.markdown("")
    
    # Optimized prompt
    st.markdown("**Optimized Prompt:**")
    st.markdown(f"""
    <div style='background: #f0f4ff; padding: 1rem; border-radius: 10px; border-left: 4px solid #c5d5f7;'>
        {best['best_prompt']}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Final response
    st.markdown("**Response:**")
    st.markdown(f"""
    <div style='background: #f5fff5; padding: 1rem; border-radius: 10px; border-left: 4px solid #c5e8c5;'>
        {best['best_response']}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Explanation
    st.caption(best['explanation'])
    
    # Detailed scoring breakdown (collapsible)
    with st.expander("View Score Details"):
        scores = best['best_scores']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Length & Completeness", f"{scores['length_score']:.1f}/25")
            st.metric("Keyword Relevance", f"{scores['keyword_score']:.1f}/25")
        with col2:
            st.metric("Structure & Formatting", f"{scores['structure_score']:.1f}/25")
            st.metric("Prompt Alignment", f"{scores['alignment_score']:.1f}/25")


def main():
    """Main application entry point."""
    
    # Page configuration
    st.set_page_config(
        page_title="PromptBoost - Make Your Prompts Better",
        
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for soft pastel aesthetic and force light mode
    st.markdown("""
    <style>
        /* Force light mode */
        [data-testid="stAppViewContainer"] {
            background-color: #ffffff;
            color: #333333;
        }
        
        /* Hide only deploy button */
        button[kind="header"] {
            display: none;
        }
        
        .main-header {
            text-align: center;
            padding: 2rem 0 1rem 0;
            margin-bottom: 1.5rem;
        }
        .main-header h1 {
            color: #8b9dc3;
            font-size: 2.5rem;
            margin-bottom: 0.3rem;
            font-weight: 600;
        }
        .main-header p {
            color: #6b6b6b;
            font-size: 1.1rem;
            margin: 0;
        }
        .stTextArea textarea {
            border-radius: 12px;
            border: 2px solid #e8e8f0;
            font-size: 15px;
            background-color: #fafbfd;
            color: #333333;
        }
        .stTextArea textarea:focus {
            border-color: #c7d2e8;
            box-shadow: 0 0 0 0.2rem rgba(199,210,232,0.2);
        }
        .stButton > button {
            border-radius: 12px;
            font-weight: 500;
            font-size: 16px;
            padding: 0.6rem 1.5rem;
            background-color: #d4e4f7;
            color: #5a6f8f;
        }
        .stButton > button:hover {
            background-color: #c0d7f2;
            border-color: #b8d0ed;
        }
        [data-testid="stSidebar"] {
            background-color: #fafbfd;
        }
        
        /* Ensure all text is visible */
        p, span, div, label, h1, h2, h3, h4, h5, h6 {
            color: #333333 !important;
        }
        
        /* Sidebar text */
        [data-testid="stSidebar"] * {
            color: #333333 !important;
        }
        
        /* Metric labels and values */
        [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
            color: #333333 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Simple header
    st.markdown("""
    <div class="main-header">
        <h1>✨ PromptBoost</h1>
        <p>Turn your ideas into better prompts</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: #f5f3ff; padding: 1.2rem; border-radius: 12px; margin-bottom: 2rem; border-left: 4px solid #d4c5f9;'>
        <p style='margin: 0; font-size: 1rem; color: #6b6b6b;'>
            Drop your prompt below and I'll help make it clearer and more effective.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize system components
    optimizer, generator, evaluator, storage = initialize_system()
    
    # Sidebar - functional elements only
    with st.sidebar:
        st.markdown("### Your Stats")
        
        stats = storage.get_statistics()
        
        if stats['total_optimizations'] > 0:
            st.metric("Prompts Improved", stats['total_optimizations'])
            st.metric("Average Boost", f"+{stats['average_improvement']:.1f} pts")
            
            if stats['task_type_counts']:
                st.markdown("")
                st.markdown("**By Task Type:**")
                for task, count in stats['task_type_counts'].items():
                    st.caption(f"• {task}: {count}")
        else:
            st.caption("No optimizations yet")
        
        st.markdown("")
        st.markdown("")
        if st.button("Clear History", use_container_width=True):
            storage.clear_results()
            st.success("History cleared")
            st.rerun()
    
    # Main input section
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### 💭 What's on your mind?")
        user_prompt = st.text_area(
            "Enter your prompt",
            placeholder="e.g., 'explain quantum computing' or 'write a function to sort numbers'",
            height=160,
            help="Type anything you want help with – don't worry about making it perfect!",
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("#### Task Type")
        
        task_type = st.selectbox(
            "Select task type",
            options=[
                "Question Answering",
                "Summarization", 
                "Explanation",
                "Code Generation"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("")
        st.markdown("")
        optimize_button = st.button(
            "✨ Optimize Prompt", 
            type="primary", 
            use_container_width=True
        )
    
    # Run optimization when button is clicked
    if optimize_button:
        if not user_prompt or len(user_prompt.strip()) < 5:
            st.warning("Please enter a prompt (at least 5 characters)")
        else:
            with st.spinner("Running optimization..."):
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
                    st.success("✅ Saved to history!")
                else:
                    st.error("Optimization failed. Check the console for errors.")
    
    # Simple help section
    with st.expander("How it works"):
        st.markdown("""
        1. Enter your prompt and select the task type
        2. Click optimize
        3. The system generates improved variations
        4. Responses are evaluated using objective metrics
        5. You get the best optimized prompt and response
        """)


if __name__ == "__main__":
    main()
