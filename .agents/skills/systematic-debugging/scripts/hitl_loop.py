#!/usr/bin/env python3
"""Drive a person through a reproduction, so a loop that needs a human stays structured.

The last rung of `systematic-debugging`'s red command ladder, used only when a person is present
and no unattended route reaches the defect. Copy this file to a scratch location outside the
tracked tree, write the steps one per line in a text file, and run:

    python hitl_loop.py STEPS_FILE --question "Did the error banner appear?" [--log FILE]

It shows each step, numbered, and waits for Enter; then it asks the question once, re-asking until
the answer is yes or no. With --log, it appends one JSON line per run: the time, the steps, the
question, and the answer, for the diagnosis record's `reproduction` field. Redact before you log:
a step or answer that carries a secret is written as given.

Exit status: 1 when the person saw the symptom (red), 0 when they did not (green), and 2 when the
run could not complete (no steps, an unreadable file, or nobody answering). Two means unanswered,
never green. Standard library only.
"""
import argparse
import json
import sys
from datetime import datetime, timezone

YES = {"y", "yes"}
NO = {"n", "no"}


def ask(prompt):
    """One line from the person, or None when stdin is closed (nobody is there to answer)."""
    print(prompt, end="", flush=True)
    line = sys.stdin.readline()
    if not line:
        print()
        return None
    return line.strip()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("steps_file", help="text file with one reproduction step per line")
    parser.add_argument("--question", required=True,
                        help="the yes-or-no question about the symptom, asked after the steps")
    parser.add_argument("--log", help="append one JSON line recording this run")
    args = parser.parse_args(argv)

    try:
        with open(args.steps_file, encoding="utf-8") as handle:
            steps = [line.strip() for line in handle if line.strip()]
    except (OSError, UnicodeDecodeError) as exc:
        print(f"hitl_loop: cannot read the steps file: {exc}", file=sys.stderr)
        return 2
    if not steps:
        print("hitl_loop: the steps file has no steps", file=sys.stderr)
        return 2

    for number, step in enumerate(steps, 1):
        print(f"{number}. {step}")
        if ask("   Press Enter when done. ") is None:
            print("hitl_loop: no answer, the run did not complete", file=sys.stderr)
            return 2

    while True:
        answer = ask(f"{args.question} [y/n] ")
        if answer is None:
            print("hitl_loop: no answer, the run did not complete", file=sys.stderr)
            return 2
        if answer.lower() in YES | NO:
            break
        print("Answer y or n.")

    seen = answer.lower() in YES
    if args.log:
        record = {"time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                  "steps": steps, "question": args.question, "answer": answer,
                  "symptom_seen": seen}
        with open(args.log, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(record) + "\n")
    print("red: the symptom was seen" if seen else "green: the symptom was not seen")
    return 1 if seen else 0


if __name__ == "__main__":
    sys.exit(main())
