RESEARCH_PLAN_PROMPT = """You are an expert research planner.
Given a research question, break it down into 3-5 specific search queries that
together would give comprehensive coverage of the topic.

Research Question: {question}

Return ONLY a Python list of search query strings. Example: ['query one', 'query two', 'query three']

Search Queries:
"""

SYNTHESIS_PROMPT = """You are an expert research analyst and writer.
You have been given a research question and a collection of search results.
Your job is to synthesize the information into a clear, well-structured research report.

Research Question: {question}

Search Results: {search_results}

Write a comprehensive research report with the following secttions:
1. Executive Summary (2-3 sentences)
2. Key Findings (3-5 bullet points)
3. Detailed Analysis (3-5 paragraphs)
4. Conclusion
5. Sources Used

Be factual, balanced, and cite the sources you referenced."""

FOLLOWUP_PROMPT = """Based on the following research findings, identify 2-3 important aspects
that need deeper investigation. Result only a Python list of follow-up queries.

Original Question: {question}
Current Findings Summary: {Summary}

Follow-up Search Queries:"""