#!/usr/bin/env python3
"""Daily habit checklist. Run once per day to log your habits."""

import json
import os
from datetime import date

HABITS_FILE = os.path.join(os.path.dirname(__file__), "habits.json")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def load_habits():
    with open(HABITS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["habits"]


def load_log(today: str) -> dict:
    os.makedirs(DATA_DIR, exist_ok=True)
    log_file = os.path.join(DATA_DIR, f"{today}.json")
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_log(today: str, log: dict):
    log_file = os.path.join(DATA_DIR, f"{today}.json")
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)


def print_summary(habits: list, log: dict):
    done = sum(1 for h in habits if log.get(h["id"], {}).get("done"))
    print(f"\n  Progress: {done}/{len(habits)} habits completed today\n")
    for h in habits:
        entry = log.get(h["id"], {})
        checked = "[x]" if entry.get("done") else "[ ]"
        goal_info = f"  (goal: {h['goal']} {h['unit']})" if h.get("goal") else ""
        note = f"  -> logged {entry['actual']} {h['unit']}" if entry.get("actual") else ""
        print(f"  {checked} {h['name']}{goal_info}{note}")
    print()


def run_checklist():
    today = date.today().isoformat()
    habits = load_habits()
    log = load_log(today)

    print(f"\n=== Habit Checklist — {today} ===")
    print_summary(habits, log)

    unchecked = [h for h in habits if not log.get(h["id"], {}).get("done")]

    if not unchecked:
        print("  All habits done for today. Great work!\n")
        return

    print("  Mark habits as done (press Enter to skip):\n")
    for h in unchecked:
        prompt = f"  Did you '{h['name']}'? (y/n): "
        answer = input(prompt).strip().lower()
        if answer == "y":
            actual = None
            if h.get("goal"):
                raw = input(f"    How many {h['unit']} did you do? (Enter to use goal {h['goal']}): ").strip()
                actual = int(raw) if raw.isdigit() else h["goal"]
            log[h["id"]] = {"done": True, "actual": actual}
            print(f"    Logged!\n")
        elif answer == "n":
            log[h["id"]] = {"done": False}
            print(f"    Noted.\n")
        else:
            print(f"    Skipped.\n")

    save_log(today, log)
    print("=== Updated summary ===")
    print_summary(habits, log)


if __name__ == "__main__":
    run_checklist()
