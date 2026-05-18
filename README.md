# Job Search Agent 🤖

An AI agent that analyzes your skill gaps for any job title and generates a personalized 30-day learning plan — runs completely free using Ollama (no API key needed).

## How it works

```
Job Title
  → Look up required skills
  → Compare with your current skills
  → Find the gaps
  → Generate a personalized 30-day learning plan with free resources
```

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Ollama (llama3.2) — runs locally, free |
| Orchestration | LangChain |
| API | Python CLI |

## Getting Started

### 1. Install Ollama

Download from [ollama.com](https://ollama.com) then pull the model:

```bash
ollama pull llama3.2
```

### 2. Clone and install

```bash
git clone https://github.com/prudhvirapeti/job-search-agent.git
cd job-search-agent
python -m venv venv
source venv/bin/activate
pip install langchain-ollama langchain-core langgraph
```

### 3. Run the agent

```bash
python agent.py "AI Engineer"
python agent.py "Data Engineer"
python agent.py "Data Analyst"
```

## Example Output

```
Job Search Agent — 'AI Engineer'
============================================================

[Step 1] Looking up required skills...
Found 10 required skills.

[Step 2] Comparing with your current skills...
Found 4 skill gaps: Docker, LangGraph, MLOps basics, Vector databases

[Step 3] Finding best learning resources...

[Step 4] Generating your personalized learning plan...

You're already halfway there! With your existing skills in Python,
LangChain, RAG pipelines and FastAPI, you've got a solid foundation...

Skill gaps summary:
  • Docker: freeCodeCamp Docker course (free, 4hrs) on YouTube
  • LangGraph: LangGraph docs quickstart → https://langchain-ai.github.io/langgraph/
  • MLOps basics: Made With ML → https://madewithml.com
```

## Roadmap

- [x] Skill gap analysis
- [x] Personalized learning plan via LLM
- [ ] Connect to real job postings API
- [ ] Add resume parsing to auto-detect current skills
- [ ] Streamlit UI
- [ ] Support more job titles
