"""
evaluate.py
Runs 5 targeted test questions through the full RAG pipeline and prints
a structured evaluation report.

Use the output to fill in the Evaluation Report table in README.md.
"""

from dotenv import load_dotenv
load_dotenv()

from src.utils import check_env
from src.query import ask

check_env()

TEST_QUESTIONS = [
    {
        "question": "What is the cheapest way to eat in NYC as a student?",
        "expected": "Dollar slices, halal carts (~$7-9), Trader Joe's frozen meals, bodega egg-and-cheese sandwiches ($3-5)",
    },
    {
        "question": "How does the OMNY weekly bonus cap work on the subway?",
        "expected": "After 12 rides in a week the 13th+ rides are free; replaces the old 7-day unlimited MetroCard",
    },
    {
        "question": "What neighborhoods are affordable for students sharing an apartment?",
        "expected": "Astoria ($1,000-1,400/room), Ridgewood/Bushwick ($1,100-1,500), Washington Heights ($1,200-1,600), Crown Heights, Sunnyside/Woodside",
    },
    {
        "question": "As an F-1 international student, can I work off campus?",
        "expected": "Generally no, unless authorized via CPT (for internships integral to curriculum) or OPT (after graduation)",
    },
    {
        "question": "What are common scams in NYC that target students?",
        "expected": "CD hustle, petition scam, three-card monte, fake monks, Times Square costumed characters demanding money",
    },
]


def evaluate():
    print("\n" + "="*70)
    print("  NYC STUDENT GUIDE — EVALUATION REPORT")
    print("="*70)

    for i, test in enumerate(TEST_QUESTIONS, 1):
        print(f"\n{'─'*70}")
        print(f"Q{i}: {test['question']}")
        print(f"Expected: {test['expected']}")

        result = ask(test["question"], top_k=5)

        print(f"\nSystem answer:\n{result['answer']}")
        print(f"\nSources retrieved: {', '.join(result['sources'])}")
        print(f"Chunk distances:   {[c['distance'] for c in result['chunks']]}")

        # Simple self-check: did any retrieved chunk come from a plausible source?
        print("\n[Manual check needed]")
        print("  Retrieval quality: Relevant / Partially relevant / Off-target")
        print("  Response accuracy: Accurate / Partially accurate / Inaccurate")

    print("\n" + "="*70)
    print("Evaluation complete. Fill in README.md table with results above.")
    print("="*70 + "\n")


if __name__ == "__main__":
    evaluate()