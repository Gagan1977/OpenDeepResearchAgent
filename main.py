from src.agent import run_research
from src.report import save_report


def main():
    print("\n================================")
    print("   DEEP RESEARCH AGENT")
    print("================================")
    print("Type your research question.")
    print("Type 'quit' to exit.\n")

    while True:
        question = input("Research Question: ")
        if not question:
            print('Please enter a research question.')
            continue

        if question.lower() in ('quit', 'exit', 'q'):
            print('Goodbye!')
            break

        try:
            report = run_research(question)

            path = save_report(question, report)
            print(f"\n Report saved to: {path}\n")

        except Exception as e:
            print(f"\n Something went wrong: {e}\n")


if __name__ == "__main__":
    main()