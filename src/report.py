import os
import re
from datetime import datetime


def save_report(question: str, report: str) -> str:
    """
    Saves the research report to a .md file in the outputs folder.
    
    question: the original research question (used for the filename)
    report: the full report text from the agent
    
    Returns the file path so we can print it to the user.
    """

    os.makedirs('outputs', exist_ok=True)

    safe_name = re.sub(r"[^\w\s]", "", question.lower())
    safe_name = re.sub(r"\s+", "_", safe_name)[:50]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{safe_name}.md"
    filepath = os.path.join('outputs', filename)

    date_str = datetime.now().strftime("%B %d, %Y at %H:%M")
    content = (
        f"#Research Report\n\n"
        f"**Question:** {question}\n\n"
        f"**Generated: {date_str}**\n\n"
        f"---\n\n"
        f"{report}\n"
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath