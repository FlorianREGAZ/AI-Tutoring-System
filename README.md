# AI Tutoring System

A sophisticated multi-agent AI tutoring system that uses the Socratic method, adaptive scaffolding, and RAG to provide personalized learning experiences.

## 🏗️ Architecture

The system is built using **LangGraph** with three specialized agents collaborating:

```
┌─────────────────┐
│   Tutor Agent   │ ← Executes teaching plans
│                 │   using Socratic method
└─────────────────┘
      ▲
      │ Teaching Instructions
      │
      │
      ├─────────────────┐
      │                 │
┌─────────────────┐ ┌─────────────────┐
│   Stage Judge   │ │  PDF Assistant  │
│      Agent      │ │      Agent      │
└─────────────────┘ └─────────────────┘
```

## 📁 Project Structure

```
AI-Tutoring-System/
├── agents/                    # Multi-agent system components
│   ├── pdf_assistant.py       # RAG-powered PDF content extraction agent
│   ├── stage_judge.py         # Learning stage assessment and progression agent
│   └── tutor.py               # Socratic method tutoring agent
├── core/                      # Core system components
│   ├── prompts.py             # System prompts and instructions for each learning stage
│   └── schemas.py             # Pydantic models and state management schemas
├── utils/                     # Utility modules
│   ├── debug.py               # Debugging and state inspection utilities
│   ├── image_parser.py        # Image processing and caption generation
│   └── pdf_parser.py          # PDF parsing with text and image extraction
├── config.py                  # Configuration management and environment setup
├── run_ai_tutor.py            # Main application entry point
```

## ✨ Key Features

### **Multi-Agent Architecture**
- **Tutor Agent**: Implements Socratic method teaching with adaptive scaffolding
- **Stage Judge Agent**: Monitors learning progress and determines optimal stage transitions
- **PDF Assistant Agent**: Provides contextual information from uploaded learning materials

### **Learning Stages**
- **Topic Clarification**: Identifies learning objectives and subject matter
- **User Assessment**: Evaluates student's grade level, goals, and prior knowledge
- **Knowledge Evaluation**: Establishes baseline understanding and entry points
- **Concept Presentation**: Introduces new concepts with analogies and examples
- **Guided Practice**: Interactive exercises with hints and step-by-step guidance
- **Independent Practice**: Self-directed application of learned concepts
- **Wrap-up**: Knowledge consolidation and session summary

### **RAG System**
- **PDF Processing**: Automatic text and image extraction from learning materials
- **Vector Search**: Semantic similarity search for contextual information retrieval
- **Multi-modal Support**: Handles both text and image content from PDFs

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Installation

1. **Clone and setup environment:**
   ```bash
   cd AI-Tutor-Playground
   source venv/bin/activate  # or create new: python -m venv venv
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   Create `.env.local` file with your API keys:
   ```bash
   # API Keys (one is enough depending on model selection)
   GOOGLE_API_KEY=your_google_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here

   # Model Selection
   DEFAULT_MODEL=openai:gpt-5
   STAGE_JUDGE_MODEL=openai:gpt-5
   PDF_ASSISTANT_MODEL=openai:gpt-5
   TUTOR_MODEL=openai:gpt-5-chat-latest
   ```

4. **Run the system:**
   ```bash
   python run_ai_tutor.py
   ```
