# Multi-Agent Personalized Learning Platform

A production-grade, locally-running multi-agent system that transforms uploaded text or PDFs into adaptive, personalized learning content (quizzes, flashcards, interactive modules) that evolves based on user feedback.

## 🏗️ Architecture

The platform consists of four specialized agents:

1. **NLP Agent** - Extracts and processes text from PDFs using spaCy and HuggingFace BART
2. **LLM Agent** - Generates learning content using OpenAI GPT-4o-mini
3. **RL Agent** - Personalizes experience using Thompson Sampling reinforcement learning
4. **Manager Agent** - Orchestrates all agents and manages workflow

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- macOS M1 (optimized for Apple Silicon)
- OpenAI API key

### Installation

1. **Clone and navigate to the project:**
   ```bash
   cd QuizGenerator
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

6. **Run the application:**
   ```bash
   streamlit run src/ui/app.py
   ```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage

### First Time Setup

1. **Complete the Survey**: When you first launch the app, you'll be asked about your preferred learning style:
   - 📝 Quizzes (Test your knowledge)
   - 🃏 Flashcards (Quick memorization)
   - 🎯 Interactive (Step-by-step learning)
   - ❓ I don't know (Show me all options)

2. **Upload Material**: Upload a PDF or text file in the sidebar

3. **Study Content**: Interact with the generated content and provide feedback (👍/👎)

4. **Personalization**: The RL agent learns from your feedback and improves recommendations over time

### Features

- **Adaptive Content Generation**: Content is dynamically scaled based on document length
- **Mixed Bundle Mode**: When preference is unknown, all three content types are shown in tabs
- **Feedback Loop**: Like/Dislike buttons train the RL agent
- **Preference Reset**: Change your learning style anytime via the sidebar
- **Session Tracking**: Your preferences and feedback are persisted locally

## 🧩 Agent Details

### NLP Agent (`src/agents/nlp_agent.py`)
- Uses `pypdf` for PDF extraction
- `spaCy` with `en_core_web_sm` for text processing
- HuggingFace `facebook/bart-base` for summarization
- Intelligent text chunking with sentence boundary detection

### LLM Agent (`src/agents/llm_agent.py`)
- OpenAI GPT-4o-mini API integration
- Generates structured JSON output for:
  - Quizzes (5 MCQs with explanations)
  - Flashcards (10 front/back pairs)
  - Interactive lessons (3-step plans)
  - Mixed bundles (all three types)

### RL Agent (`src/agents/rl_agent.py`)
- Custom Thompson Sampling implementation
- Maintains success/failure probabilities for each mode
- Recommends optimal learning mode based on historical feedback
- State persisted in `.ma_state.json`

### Manager Agent (`src/agents/manager_agent.py`)
- Coordinates all agents via orchestrator
- Handles survey logic and preference management
- Routes tasks and maintains session context
- Uses OpenAI for intelligent reasoning (with rule-based fallback)

## 📁 Project Structure

```
QuizGenerator/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── orchestrator.py        # Manager Agent logic
│   │   ├── messages.py            # Inter-agent communication
│   │   ├── memory.py              # RL state persistence
│   │   └── logger.py              # Centralized logging
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── nlp_agent.py           # Text extraction
│   │   ├── llm_agent.py           # Content generation
│   │   ├── rl_agent.py            # Personalization
│   │   └── manager_agent.py       # Orchestration
│   ├── tools/
│   │   ├── __init__.py
│   │   └── pdf_extractor.py       # PDF processing
│   └── ui/
│       ├── __init__.py
│       ├── app.py                 # Streamlit UI
│       └── theme.css              # UI styling
├── .env.example
├── requirements.txt
└── README.md
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
```

### State Management

RL agent state is persisted in `.ma_state.json` in the project root. This file contains:
- Mode probabilities (alpha/beta parameters)
- Feedback history
- Survey completion status
- Session metadata

To reset preferences, use the "🔄 Reset Preferences" button in the sidebar.

## 🎨 UI Features

- **Sidebar**: File upload, survey, preference display, reset button
- **Main Area**: 
  - Survey page (first-time users)
  - Content display with mode-specific layouts
  - Mixed bundle tabs (when preference unknown)
  - Feedback buttons for RL learning

## 🔒 Privacy & Performance

- **Local Processing**: All text processing and RL logic run locally
- **API Calls**: Only OpenAI API is called (for content generation and reasoning)
- **M1 Optimized**: Efficient on macOS M1 MacBook Air
- **Modular Design**: Easy to extend with new agents or features

## 🛠️ Development

### Adding New Agents

1. Create agent class in `src/agents/`
2. Implement required methods
3. Add message types in `src/core/messages.py`
4. Integrate with orchestrator in `src/core/orchestrator.py`

### Extending Content Types

1. Add new `ContentType` enum value in `src/core/messages.py`
2. Implement generation method in `LLMAgent`
3. Add renderer in `src/ui/app.py`

### Async Orchestration

The orchestrator includes `handle_command_async()` for future parallel agent calls using `asyncio.gather`.

## 📝 Logging

Logs are stored in `logs/` directory and can be viewed in the Streamlit sidebar. The logger supports:
- Console output
- File logging (daily rotation)
- Streamlit mirroring

## 🐛 Troubleshooting

### spaCy Model Not Found
```bash
python -m spacy download en_core_web_sm
```

### OpenAI API Errors
- Verify your API key in `.env`
- Check API quota and billing
- Ensure model name is correct (`gpt-4o-mini`)

### PDF Extraction Issues
- Ensure PDF is not password-protected
- Try converting to text file as fallback
- Check file size (very large files may need chunking)

## 📄 License

This project is provided as-is for educational and development purposes.

## 🤝 Contributing

This is a modular system designed for easy extension. Key extension points:
- New agent types in `src/agents/`
- New content types in `LLMAgent`
- UI components in `src/ui/app.py`
- Message types in `src/core/messages.py`

---

Built with ❤️ using Python, Streamlit, OpenAI, spaCy, and NumPy. No LangChain, crewAI, or n8n dependencies.

