import ast
from typing import List, TypedDict
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

from .tools import search_web

load_dotenv()


def get_llm():
    """Return the Ollama AI model."""
    return ChatOllama(
        model='llama3.2',
        temperature=0.1
    )


class ResearchState(TypedDict):
    """
    This is the memory of the agent.
    Every piece of information we need gets stored here
    and passed from one step to the next.
    """
    question: str
    search_queries: List[str]
    search_results: str
    report: str
    iteration: int


def plan_queries(state: ResearchState) -> ResearchState:
    """
    Step 1: Ask the AI to break the question into
    3 specific search queries."""
    print(f'\n Planning queries for: {state['question']}')

    llm = get_llm()

    prompt = (
        "You are a research assistant." \
        "Convert the following question into exactly 3 specific search queries." \
        "Return only a Python list like this: [\'query1\', \'query2\', \'query3\'] "\
        "No explanations. No extra text. Just the list.\n\n" \
        "Question: " + state['question']
    )

    response = llm.invoke([HumanMessage(content=prompt)])
    queries = parse_list(response.content)
    if not queries:
        queries = [state['question']]
        
    print(f'    Got {len(queries)} queries')
    for q in queries:
        print(f'    - {q}')

    return {**state, "search_queries": queries}


def run_search(state: ResearchState) -> ResearchState:
    """
    Step 2: Pass all queries to tools.py and get back
    the web results as a single block of text.
    """
    print(f'\n Searching the web...')
    
    results = search_web(state['search_queries'])
    print(f'    Search complete.')
    return {**state, "search_results": results}


def write_report(state: ResearchState) -> ResearchState:
    """
    Step 3: Give the AI the search results and ask it
    to write a proper research report.
    """
    print(f'\n Writing report...')

    llm = get_llm()

    prompt = (
        "You are an expert research writer." \
        "Write only the search results below, write a detailed research report.\n\n" \
        "Structure the report with these sections:\n" \
        "1. Summary\n"
        "2. Key Findings\n"
        "3. Detailed Analysis\n"
        "4. Conclusion\n\n"
        "Research Question: " + state["question"] + "\n\n"
        "Search Results:\n" + state["search_results"]
    )

    response = llm.invoke([HumanMessage(content=prompt)])
    print(f'    Report written ({len(response.content)} characters).')
    return {**state, "report": response.content}


def plan_followup(state: ResearchState) -> ResearchState:
    """
    Step 4: Read the first report and as the AI what 
    important topics were missed. Plan 2 more searches.
    """
    print(f'\n Planning follow-up searches...')

    llm = get_llm()

    short_report = state['report'][:1000]
    
    prompt = (
        "You are a research assistant. "
        "Read this partial research report and identify 2 topics that need more investigation. "
        "Return ONLY a Python list like: [\"follow up query one\", \"follow up query two\"] "
        "No explanation. Just the list.\n\n"
        "Original question: " + state["question"] + "\n\n"
        "Report so far:\n" + short_report
    )

    response = llm.invoke([HumanMessage(content=prompt)])
    followup = parse_list(response.content)

    if not followup:
        followup = [state['question'] + " recent developments"]

    print(f'    Got {len(followup)} follow-up queries.')
    return {**state, "search_queries": followup, "iteration": state['iteration'] + 1}


def parse_list(text: str) -> list:
    """
    Safely extracts a Python list from the AI's response text.
    The AI might say 'Here is your list: ['a', 'b'] - we find
    just the list part and parse it.
    """
    text = text.strip()
    start = text.find('[')
    end = text.rfind(']')

    if start == -1 or end == -1:
        return []
    
    try:
        result = ast.literal_eval(text[start:end+1])
        if isinstance(result, list):
            return result
    except Exception as e:
        pass

    return []


def run_research(question: str) -> ResearchState:
    """
    This main function that runs all 4 steps in order.
    This is what main.py will call.
    """
    state = ResearchState(
        question=question,
        search_queries=[],
        search_results='',
        report='',
        iteration=1
    )

    print("\n" + "=" * 60)
    print("DEEP RESEARCH AGENT")
    print("=" * 60)

    state = plan_queries(state)
    state = run_search(state)
    state = write_report(state)

    state = plan_followup(state)
    state = run_search(state)
    state = write_report(state)

    return state['report']