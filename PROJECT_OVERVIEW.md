# Project Overview: Automated Prompt Optimization

## 🎯 What This Project Does

This system automatically improves user prompts through a systematic, metric-based optimization process. Users don't need any prompt engineering knowledge—they just enter a prompt, and the system returns an optimized version with a better response.

## 🏗️ Architecture Overview

### System Components

1. **Gemini Client** (`gemini_client.py`)
   - Manages all API interactions with Google Gemini
   - Handles text generation with configurable parameters
   - Ensures consistent model settings across all operations

2. **Prompt Optimizer** (`prompt_optimizer.py`)
   - Generates 4 improved variations of the user's prompt
   - Uses task-specific optimization guidelines
   - Employs Gemini to create better-structured prompts

3. **Response Generator** (`response_generator.py`)
   - Generates responses for original and all optimized prompts
   - Uses identical model settings (temp=0.7, max_tokens=1024)
   - Ensures fair comparison between prompts

4. **Evaluator** (`evaluator.py`)
   - **Deterministic, rule-based evaluation only**
   - No subjective LLM self-rating
   - Scores responses on 4 metrics (0-25 points each):
     * **Length/Completeness**: Appropriate word count for task type
     * **Keyword Relevance**: Presence of task-specific keywords
     * **Structure/Formatting**: Proper sentences, paragraphs, lists
     * **Prompt Alignment**: Keyword overlap between prompt and response

5. **Storage** (`storage.py`)
   - File-based storage of optimization results
   - Statistics tracking and history
   - Export capabilities

6. **Web UI** (`app.py`)
   - Interactive Streamlit interface
   - Real-time progress tracking
   - Results visualization

## 🔄 System Workflow

### Sequential Pipeline (FIXED ORDER):

```
┌─────────────────────────────────────────────────────────────┐
│  1. USER INPUT                                              │
│     • Text prompt                                           │
│     • Task type selection (dropdown)                        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  2. VARIATION GENERATION (Using Gemini)                     │
│     • Generate 4 improved prompt variations                 │
│     • Apply task-specific optimization guidelines           │
│     • Each variation improves clarity & specificity         │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  3. RESPONSE GENERATION (Using Gemini)                      │
│     • Generate response for original prompt                 │
│     • Generate response for each optimized variation        │
│     • All use identical model settings                      │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  4. METRIC-BASED EVALUATION (Deterministic)                 │
│     • Score each response on 4 metrics                      │
│     • Length/completeness: 0-25 pts                         │
│     • Keyword relevance: 0-25 pts                           │
│     • Structure/formatting: 0-25 pts                        │
│     • Prompt alignment: 0-25 pts                            │
│     • Total score: 0-100 pts                                │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  5. SELECTION                                               │
│     • Compare all scores                                    │
│     • Select highest-scoring prompt+response pair           │
│     • Generate explanation of why it won                    │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  6. OUTPUT TO USER (UI Display)                             │
│     • Optimized prompt                                      │
│     • Improved response                                     │
│     • Explanation of improvements                           │
│     • Score comparison (original vs optimized)              │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│  7. OPTIONAL STORAGE                                        │
│     • Save results to local JSON file                       │
│     • Track statistics and history                          │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Evaluation Methodology

### Why Metric-Based Evaluation?

The system uses **deterministic, rule-based metrics** instead of LLM self-evaluation to:

1. **Avoid Bias**: LLMs can be biased when judging their own outputs
2. **Ensure Repeatability**: Same input always produces same scores
3. **Provide Transparency**: Users can understand exactly how scores are calculated
4. **Maintain Objectivity**: No subjective "this seems better" judgments

### The 4 Evaluation Metrics

#### 1. Length & Completeness (0-25 points)
- Checks if response length is appropriate for task type
- Each task has optimal word count ranges:
  * Question Answering: 30-200 words
  * Summarization: 50-150 words
  * Explanation: 100-300 words
  * Code Generation: 50-400 words

#### 2. Keyword Relevance (0-25 points)
- Counts presence of task-specific keywords
- Question Answering: "answer", "because", "therefore", "evidence"
- Summarization: "summary", "main", "key", "important"
- Explanation: "first", "step", "example", "how", "why"
- Code Generation: "function", "class", "return", "import"

#### 3. Structure & Formatting (0-25 points)
- Proper sentences (ending with punctuation)
- Multiple paragraphs (organization)
- Lists or bullet points (clarity)
- Code blocks (for code generation)
- Proper capitalization

#### 4. Prompt Alignment (0-25 points)
- Keyword overlap between prompt and response
- Ensures response addresses the actual prompt
- Higher overlap = better alignment

## 🎨 Task Types & Optimization Strategies

### Question Answering
**Guidelines:**
- Be specific about information needed
- Specify answer format
- Include relevant context
- Request appropriate detail level

**Example:**
- Original: "What is AI?"
- Optimized: "Please provide a concise, accurate answer to: What is artificial intelligence? Include a brief definition and 2-3 real-world applications."

### Summarization
**Guidelines:**
- Specify desired summary length
- Indicate key points to focus on
- Request specific format (bullets, paragraph)
- Mention target audience

**Example:**
- Original: "Summarize this article"
- Optimized: "Please provide a 5-sentence summary of this article, focusing on the main arguments and conclusions. Use clear, concise language suitable for a general audience."

### Explanation
**Guidelines:**
- Specify complexity level (beginner/expert)
- Request examples
- Ask for step-by-step breakdown
- Indicate desired depth

**Example:**
- Original: "Explain blockchain"
- Optimized: "Please provide a beginner-friendly explanation of blockchain technology. Include: (1) a simple definition, (2) how it works in 3-4 steps, and (3) one real-world example. Use analogies where helpful."

### Code Generation
**Guidelines:**
- Specify programming language
- Include input/output requirements
- Mention constraints
- Request comments/documentation

**Example:**
- Original: "Write sorting function"
- Optimized: "Please write a Python function that implements quicksort. Requirements: (1) takes a list of integers as input, (2) returns sorted list, (3) includes docstring and comments, (4) handles edge cases like empty lists."

## 📁 Project Structure

```
/Users/vamika/Documents/again/
│
├── app.py                      # Main Streamlit application
│
├── src/                        # Core system modules
│   ├── __init__.py
│   ├── gemini_client.py        # API client
│   ├── prompt_optimizer.py     # Variation generator
│   ├── response_generator.py   # Response creator
│   ├── evaluator.py            # Metric-based scorer
│   └── storage.py              # Result storage
│
├── data/                       # Storage directory
│   └── results.json            # Optimization history
│
├── requirements.txt            # Python dependencies
├── .env.example                # API key template
├── .env                        # Your API key (create this)
├── .gitignore                  # Git ignore rules
│
├── README.md                   # Full documentation
├── QUICKSTART.md               # Quick setup guide
└── test_system.py              # System verification script
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (free tier)

### Installation Steps

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get API key:**
   - Visit https://makersuite.google.com/app/apikey
   - Create a free API key

3. **Configure:**
   ```bash
   cp .env.example .env
   # Edit .env and add: GEMINI_API_KEY=your_key_here
   ```

4. **Test system:**
   ```bash
   python test_system.py
   ```

5. **Run app:**
   ```bash
   streamlit run app.py
   ```

## 💡 Usage Example

### Input
```
Prompt: "explain ML"
Task Type: Explanation
```

### Process
1. System generates 4 variations:
   - "Please provide a clear explanation of machine learning..."
   - "Explain machine learning concepts including..."
   - "Give a detailed overview of ML with examples..."
   - "Describe what machine learning is and how it works..."

2. Generates 5 responses (original + 4 variations)

3. Evaluates each response:
   - Original: 58.5/100
   - Variation 1: 76.3/100 ← BEST
   - Variation 2: 72.1/100
   - Variation 3: 69.8/100
   - Variation 4: 71.5/100

### Output
```
Optimized Prompt: "Please provide a clear explanation of machine learning..."

Improved Response: [Well-structured, detailed explanation]

Why Better: "This optimized prompt achieved the highest overall score (76.3/100). 
It excelled particularly in structure and formatting (23.5/25). The optimization 
improved the response quality by 17.8 points compared to the original prompt."
```

## 🔍 Key Design Principles

1. **No Fine-Tuning**: Uses pre-trained Gemini as-is
2. **No Self-Evaluation**: LLM doesn't judge its own outputs
3. **Deterministic**: Same input produces same scores
4. **Modular**: Each component has single responsibility
5. **Transparent**: Clear explanations for all decisions
6. **Systematic**: Fixed, repeatable pipeline
7. **User-Friendly**: No prompt engineering expertise needed

## 📈 Future Enhancements (Optional)

- [ ] Add more task types
- [ ] Support custom evaluation metrics
- [ ] Implement A/B testing comparison
- [ ] Add multi-language support
- [ ] Export detailed reports
- [ ] Batch processing mode
- [ ] API endpoint for integration

## 🐛 Troubleshooting

### Common Issues

**"GEMINI_API_KEY not found"**
- Ensure .env file exists in project root
- Check API key is correctly set
- Don't include quotes around the key

**"Module not found"**
- Run: `pip install -r requirements.txt`

**"Port already in use"**
- Change port: `streamlit run app.py --server.port 8502`

**"Rate limit exceeded"**
- Wait a moment and retry
- Free tier has usage limits

## 📝 License & Usage

This is a demonstration project for educational purposes. Feel free to use, modify, and extend it for your own projects.

---

**Built with:** Python, Streamlit, Google Gemini API

**Last Updated:** December 2025
