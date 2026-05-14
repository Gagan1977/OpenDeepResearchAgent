from src.report import save_report


path = save_report(
    question="What is fusion energy?",
    report="This is a test report. It worked!"
)

print(f"Saved to: {path}")
