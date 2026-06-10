"""
evaluate.py — Evaluation script for the Unofficial NYC Student Guide RAG system.

This script runs 5 pre-defined test questions through the full RAG pipeline,
compares the system's answers to expected answers, and prints a formatted report.

Each result is labeled:
  Accurate          — System answer matches the expected answer well.
  Partially Accurate — System answer is related but incomplete or slightly off.
  Inaccurate        — System answer is wrong or irrelevant.

Usage:
    python build_database.py   # if not already done
    python evaluate.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.query import ask
from src.utils import get_logger

load_dotenv_func = None
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = get_logger("evaluate")


# Test cases

##Each entry: (question, expected_answer_key_facts)

EVAL_QUESTIONS = [
    {
        "question": "How do I get a reduced-fare MetroCard and how much does it cost?",
        "expected": (
            "Apply through your school. The reduced fare is $1.45 per ride, "
            "which is half of the standard $2.90 base fare."
        ),
    },
    {
        "question": "What is OMNY and how does the weekly bonus cap work?",
        "expected": (
            "OMNY is the tap-to-pay system replacing MetroCards. "
            "After 12 rides in a week, rides 13 through the end of that 7-day "
            "period are free — this is the weekly bonus cap."
        ),
    },
    {
        "question": "What free or low-cost mental health resources are available to NYC students?",
        "expected": (
            "Campus counseling centers (free), NYC Well (free 24/7 hotline), "
            "Crisis Text Line (text HOME to 741741), Open Path Collective "
            "($30-80/session), and Therapy Aid Coalition."
        ),
    },
    {
        "question": "What are the tenant rights regarding security deposits in NYC?",
        "expected": (
            "The landlord must return the security deposit within 14 days of "
            "move-out with itemized deductions, or they may owe the full amount."
        ),
    },
    {
        "question": "How many hours per week can an F-1 international student work on campus?",
        "expected": (
            "F-1 students may work up to 20 hours per week on campus while "
            "school is in session. There is no limit during official school breaks."
        ),
    },
]


# Evaluation function
def evaluate() -> None:
    """Run all evaluation questions and print results."""

    print("\n" + "=" * 70)
    print("  UNOFFICIAL GUIDE — RAG EVALUATION REPORT")
    print("=" * 70)

    for i, case in enumerate(EVAL_QUESTIONS, start=1):
        question = case["question"]
        expected = case["expected"]

        print(f"\n{'─' * 70}")
        print(f"Question {i}: {question}")
        print(f"{'─' * 70}")
        print(f"Expected:  {expected}")

        try:
            result = ask(question)
            answer = result["answer"]
            chunks = result.get("chunks", [])
            sources = result.get("sources", [])

            print(f"\nActual:    {answer}")
            print(f"\nSources retrieved: {', '.join(sources) if sources else 'None'}")

            print("\nTop Retrieved Chunks:")
            for j, chunk in enumerate(chunks[:3], start=1):
                preview = chunk["text"][:120].replace("\n", " ")
                print(f"  Chunk {j} [{chunk['source']}] (score={chunk['score']:.4f}): {preview}...")

            # Simple accuracy label — in real evaluation this would be automated
            accuracy = _auto_accuracy_hint(answer, expected)
            print(f"\nAccuracy Label: {accuracy}")

        except ValueError as e:
            print(f"\n  Pipeline error: {e}")
            print("Make sure you have run: python build_database.py")

        except Exception as e:
            print(f"\n  Unexpected error: {e}")
            logger.error("Eval error on question %d: %s", i, e, exc_info=True)

    print("\n" + "=" * 70)
    print("  Evaluation complete.")
    print("  Review the 'Actual' answers above and update the README")
    print("  evaluation table with your manual accuracy judgments.")
    print("=" * 70 + "\n")


def _auto_accuracy_hint(answer: str, expected: str) -> str:
    """
    Provide a rough automatic accuracy hint based on keyword overlap.
    This is a heuristic to save time — students should review manually.

    Args:
        answer:   The system's generated answer.
        expected: The expected key facts string.

    Returns:
        'Accurate', 'Partially Accurate', or 'Inaccurate'
    """
    refusal = "i don't have enough information"
    if refusal in answer.lower():
        return "Inaccurate  ← system refused to answer"

    # Extract key number/word tokens from expected and check if they appear in answer
    expected_tokens = set(expected.lower().split())
    answer_tokens = set(answer.lower().split())

    # Remove common stop words for a cleaner signal
    stop_words = {"the", "a", "an", "is", "in", "of", "to", "and", "or",
                  "for", "with", "are", "per", "as", "that", "which", "at",
                  "by", "this", "be", "it", "from", "on", "have", "may"}
    key_expected = expected_tokens - stop_words
    overlap = key_expected & answer_tokens
    ratio = len(overlap) / len(key_expected) if key_expected else 0

    if ratio >= 0.5:
        return "Accurate"
    elif ratio >= 0.25:
        return "Partially Accurate"
    else:
        return "Inaccurate  ← review manually"


if __name__ == "__main__":
    evaluate()
