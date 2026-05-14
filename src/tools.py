from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()


def search_web(queries: list, max_results: int=4) -> str:
    """
    Takes a list of search query strings.
    Searches the web for each one.
    Returns all results combined as a single block of text.
    """
    tool = TavilySearchResults(
        max_results=max_results,
        include_answer=True,
        include_raw_content=False,
    )

    seen_urls = set()
    all_results = []
    for query in queries:
        print(f'    Searching : {query}')
        try:
            results = tool.invoke(query)
            for r in results:
                url = r.get('url', '')
                if url not in seen_urls:
                    seen_urls.add(url)
                    all_results.append(r)
        except Exception as e:
            print(f'    Search failed: {e}')

    return _format(all_results)


def _format(results: list) -> str:
    """
    Convert raw search result list into readable text.
    """
    if not results:
        return "No results found."
    
    parts = []
    for i, r in enumerate(results, 1):
        url = r.get('url', 'Unknown source')
        content = r.get('content', '').strip()
        parts.append(f'[Source {i}] {url}\n{content}')

    return "\n\n---\n\n".join(parts)
