# Automated Prompt Optimization Using LLM-Generated Variations and Metric-Based Evaluation

## Overview
This project automatically improves user prompts through systematic optimization and metric-based evaluation, without requiring prompt engineering expertise from the user.

## How It Works
1. User enters a prompt and selects a task type
2. System generates 3-5 improved prompt variations using Gemini
3. Generates responses for original and all optimized prompts
4. Evaluates each response using deterministic, rule-based metrics
5. Selects the best-performing prompt
6. Returns the optimized prompt and improved response to the user

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Get a free Gemini API key:
   - Visit https://makersuite.google.com/app/apikey
   - Create an API key

4. Create a `.env` file in the project root:
   ```bash
   echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
   ```
   Replace `your_actual_api_key_here` with your actual API key

## Running the Application

```bash
python3 -m streamlit run app.py
```

The app will open in your browser at http://localhost:8501

## Features
- Interactive web UI for prompt input
- Four task types: Question Answering, Summarization, Explanation, Code Generation
- Systematic prompt variation generation
- Metric-based evaluation (no subjective LLM self-rating)
- Clear explanation of optimization results
- Optional result storage for analysis

## Project Structure
```
├── app.py                      # Streamlit UI
├── src/
│   ├── gemini_client.py        # API interactions
│   ├── prompt_optimizer.py     # Variation generation
│   ├── response_generator.py   # Response generation
│   ├── evaluator.py            # Metric-based evaluation
│   └── storage.py              # File-based storage
├── data/
│   └── results.json            # Stored results
├── requirements.txt
└── .env                        # Your API key
```

## Design Principles
- Modular, readable code
- Sequential, repeatable pipeline
- Rule-based, deterministic evaluation
- No model fine-tuning required
- No subjective LLM self-evaluation
