# Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Your Free Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your key

### 3. Configure API Key
```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your key
# GEMINI_API_KEY=your_actual_api_key_here
```

### 4. Run the Application
```bash
streamlit run app.py
```

The app will open automatically at http://localhost:8501

## Usage Example

### Input:
- **Prompt:** "explain ML"
- **Task Type:** "Explanation"

### Click "Optimize My Prompt"

### Output:
- **Optimized Prompt:** "Please provide a clear, beginner-friendly explanation of machine learning, including what it is, how it works, and real-world examples."
- **Improved Response:** [Detailed, well-structured explanation]
- **Explanation:** Why the optimized prompt scored higher

## System Architecture

```
User Input → Variation Generation → Response Generation → Evaluation → Best Selection → Display
```

### Pipeline Stages:

1. **Variation Generation** (Gemini)
   - Creates 4 improved prompts
   - Task-specific optimization

2. **Response Generation** (Gemini)
   - Generates responses for all prompts
   - Identical settings for fairness

3. **Metric-Based Evaluation** (Deterministic)
   - Length/completeness (0-25 pts)
   - Keyword relevance (0-25 pts)
   - Structure/formatting (0-25 pts)
   - Prompt alignment (0-25 pts)

4. **Selection**
   - Highest total score wins
   - Clear explanation provided

## Key Features

✅ **No Expertise Required** - Just enter your prompt
✅ **Systematic Process** - Repeatable, reliable results
✅ **Objective Scoring** - Rule-based metrics, no subjective LLM rating
✅ **Clear Explanations** - Understand why optimizations work
✅ **History Tracking** - Review past optimizations

## Troubleshooting

### API Key Error
- Make sure `.env` file exists in the project root
- Check that `GEMINI_API_KEY` is set correctly
- Verify your API key is active

### Module Not Found
```bash
pip install -r requirements.txt
```

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

## Project Structure

```
.
├── app.py                    # Streamlit web UI
├── src/
│   ├── gemini_client.py      # API client
│   ├── prompt_optimizer.py   # Variation generator
│   ├── response_generator.py # Response creator
│   ├── evaluator.py          # Metric scorer
│   └── storage.py            # Result storage
├── data/
│   └── results.json          # Stored results
├── requirements.txt
├── .env                      # Your API key (create this)
└── README.md
```

## Example Prompts to Try

### Question Answering
- "What is photosynthesis"
- "Who invented the internet"

### Summarization
- "Summarize the benefits of exercise"
- "Key points about climate change"

### Explanation
- "Explain quantum computing"
- "How does WiFi work"

### Code Generation
- "Function to calculate fibonacci"
- "Python script to read CSV"

## Design Principles

- **Modular**: Each component has a single responsibility
- **Deterministic**: Same input = same output
- **Transparent**: Clear explanations of all decisions
- **No Self-Evaluation**: LLM doesn't judge itself
- **Systematic**: Fixed, repeatable pipeline

Enjoy optimizing your prompts! 🚀
