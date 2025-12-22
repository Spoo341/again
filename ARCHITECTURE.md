# System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         STREAMLIT WEB INTERFACE (app.py)                     │
│                                                                              │
│  ┌─────────────────┐        ┌──────────────────┐                           │
│  │  User Input     │        │  Results Display │                           │
│  │  • Text prompt  │        │  • Optimized     │                           │
│  │  • Task type    │        │    prompt        │                           │
│  │  • Submit       │        │  • Improved      │                           │
│  └────────┬────────┘        │    response      │                           │
│           │                 │  • Explanation   │                           │
│           ▼                 │  • Scores        │                           │
│  ┌────────────────────────┐└──────────────────┘                           │
│  │  Progress Tracking     │                                                 │
│  │  • Step indicators     │                                                 │
│  │  • Status messages     │                                                 │
│  └────────────────────────┘                                                 │
└────────────────────────────┬─────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                        OPTIMIZATION PIPELINE                                 │
└──────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────┐
│  STAGE 1: INPUT            │
│  • Original prompt         │
│  • Task type selection     │
└──────────┬─────────────────┘
           │
           ▼
┌────────────────────────────────────────┐
│  STAGE 2: PROMPT OPTIMIZATION          │
│  (PromptOptimizer)                     │
│                                        │
│  Input: Original prompt + task type    │
│  ┌────────────────────────────────┐   │
│  │  Gemini API Call               │   │
│  │  • Task-specific guidelines    │   │
│  │  • Generate 4 variations       │   │
│  └────────────────────────────────┘   │
│  Output: 4 improved prompts            │
└──────────┬─────────────────────────────┘
           │
           ▼
┌────────────────────────────────────────┐
│  STAGE 3: RESPONSE GENERATION          │
│  (ResponseGenerator)                   │
│                                        │
│  For each prompt (original + 4):       │
│  ┌────────────────────────────────┐   │
│  │  Gemini API Call               │   │
│  │  • Temperature: 0.7            │   │
│  │  • Max tokens: 1024            │   │
│  │  • Identical settings for all  │   │
│  └────────────────────────────────┘   │
│  Output: 5 responses total             │
└──────────┬─────────────────────────────┘
           │
           ▼
┌────────────────────────────────────────────────────────┐
│  STAGE 4: METRIC-BASED EVALUATION                      │
│  (ResponseEvaluator) - NO LLM INVOLVEMENT              │
│                                                        │
│  For each response, calculate:                         │
│  ┌────────────────────────────────────────────────┐   │
│  │  Metric 1: Length & Completeness    (0-25 pts)│   │
│  │  • Word count in optimal range?                │   │
│  │  • Appropriate for task type?                  │   │
│  └────────────────────────────────────────────────┘   │
│  ┌────────────────────────────────────────────────┐   │
│  │  Metric 2: Keyword Relevance        (0-25 pts)│   │
│  │  • Contains task-specific keywords?            │   │
│  │  • Keyword percentage score                    │   │
│  └────────────────────────────────────────────────┘   │
│  ┌────────────────────────────────────────────────┐   │
│  │  Metric 3: Structure & Formatting   (0-25 pts)│   │
│  │  • Proper sentences & paragraphs?              │   │
│  │  • Lists/bullets present?                      │   │
│  │  • Code blocks (for code tasks)?               │   │
│  └────────────────────────────────────────────────┘   │
│  ┌────────────────────────────────────────────────┐   │
│  │  Metric 4: Prompt Alignment         (0-25 pts)│   │
│  │  • Keyword overlap with prompt?                │   │
│  │  • Addresses the actual question?              │   │
│  └────────────────────────────────────────────────┘   │
│                                                        │
│  Output: Total score (0-100) for each response        │
└──────────┬─────────────────────────────────────────────┘
           │
           ▼
┌────────────────────────────────────────┐
│  STAGE 5: SELECTION                    │
│  (ResponseEvaluator)                   │
│                                        │
│  • Compare all total scores            │
│  • Select highest-scoring response     │
│  • Generate explanation of why it won  │
│  • Identify strongest metrics          │
│                                        │
│  Output: Best prompt + response pair   │
└──────────┬─────────────────────────────┘
           │
           ▼
┌────────────────────────────────────────┐
│  STAGE 6: DISPLAY & STORAGE            │
│                                        │
│  Display to User:                      │
│  • Optimized prompt                    │
│  • Improved response                   │
│  • Score comparison                    │
│  • Explanation                         │
│                                        │
│  Save to Storage (ResultStorage):      │
│  • JSON file storage                   │
│  • Statistics tracking                 │
│  • History maintenance                 │
└────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                        SUPPORTING COMPONENTS                                 │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────┐  ┌──────────────────────────┐
│  GeminiClient            │  │  ResultStorage           │
│  • API configuration     │  │  • JSON file handling    │
│  • Text generation       │  │  • Statistics calc       │
│  • Error handling        │  │  • Export functions      │
└──────────────────────────┘  └──────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│                        DATA FLOW SUMMARY                                     │
└──────────────────────────────────────────────────────────────────────────────┘

User Prompt → Optimization (Gemini) → Response Gen (Gemini) → 
Evaluation (Metrics) → Selection (Compare) → Display (UI) → Storage (JSON)

═══════════════════════════════════════════════════════════════════════════════

KEY CHARACTERISTICS:

✓ Sequential Pipeline     - Fixed order, no parallel paths
✓ Two LLM Uses           - Optimization & response generation only
✓ Deterministic Eval     - Rule-based metrics, no LLM judgment
✓ Transparent Scoring    - Each metric clearly defined
✓ User-Friendly UI       - No technical knowledge required
✓ History Tracking       - All results stored for analysis

═══════════════════════════════════════════════════════════════════════════════
