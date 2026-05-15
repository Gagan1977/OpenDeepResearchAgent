# Open Deep Research Agent

An AI-powered research agent that searched the web and generates
detailed research reports automatically.

## How it works
1. You type a research quesiton
2. The agent plans search queries
3. Searches the web using Tavily
4. Writes a full report using Ollama (local AI)
5. Saves the report as a Markdown file

## Setup

**1. Clone the repo**
```
git clone https://github.com/Gagan1977/open-deep-research-agent.git
cd open-deep-research-agent
```

**2. Create virtual environment**
```
python -m venv venv
venv/Scripts/Activate
```

**3. Install dependencies**
```
pip install -r requirements.txt
```

**4. Install Ollama**

    Download from https://ollama/com and then run:
    ollama pull llama3.2

**5. Add your API key**

    Create a .env file
    TAVILY_API_KEY=your_key_here

**6. Run**
```
python main.py
```

## Tech Stack
- LangChain
- LangGraph
- Tavily Search API
- Ollama (local AI)