# -------------------------------------------------------
# Learning Object 3: The Trolley Problem Moral Simulator
# By: Hashim Shahzad Khan
# -------------------------------------------------------
# What this teaches:
# - Why trolley problems show morality is more than totals
# - Act utilitarianism vs. deontological constraints (Kant/Thomson)
# - Intention, agency, "doing vs allowing", doctrine of double effect
#
# My original misunderstanding:
#   I thought "save the most lives" = the right answer.
#   Readings/discussion showed people care about more than totals:
#   rights, agency, and not using people merely as means.
# -------------------------------------------------------

import time

PRINT_DELAY = 0.02

def slow_print(text, delay=None):
    if delay is None:
        delay = PRINT_DELAY
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def choose_text_speed():
    global PRINT_DELAY
    print("\nChoose how quickly the text should appear:")
    options = {
        "1": ("cinematic", 0.04),
        "2": ("standard", 0.02),
        "3": ("instant", 0.00),
    }
    for key, (label, _) in options.items():
        print(f"{key}. {label.title()} pacing")
    while True:
        selection = input("Enter 1, 2, or 3: ").strip()
        if selection in options:
            label, value = options[selection]
            PRINT_DELAY = value
            print(f"\nText speed set to {label} mode.\n")
            break
        print("Please enter 1, 2, or 3.")

def evaluate_choice(choice, saved, killed, scenario_type):
    print("\n=== Philosophical Evaluation ===\n")
    slow_print("• ACT UTILITARIANISM:")
    if saved > killed:
        slow_print(f"  This maximizes total lives saved ({saved} vs {killed}).")
        slow_print("  Classical utilitarianism would call this morally right because the sum is higher.")
    elif saved == killed:
        slow_print("  Totals are equal here, so utilitarianism is indifferent on numbers alone.")
        slow_print("  This highlights why intention/agency can tip our judgment beyond totals.")
    else:
        slow_print("  Fewer lives are saved; utilitarianism would likely reject this action.")
    print()
    slow_print("• DEONTOLOGY (Kant / Thomson):")
    if scenario_type == "footbridge":
        slow_print("  Pushing uses a person as a means, which deontological ethics forbids—even to save more.")
    elif scenario_type == "switch":
        slow_print("  Switching is often seen as redirecting harm (not using a person as a tool), so it is sometimes permitted.")
    elif scenario_type == "self-driving":
        slow_print("  Questions include whether the passenger is used as a means and whether harm is directly caused by swerving.")
    elif scenario_type == "equal-1v1":
        slow_print("  With equal totals, intention and agency loom large: causing harm vs. allowing harm.")
    print()
    slow_print("• MORAL INTUITION / DOCTRINE OF DOUBLE EFFECT:")
    slow_print("  We judge differently when harm is intended (as a means) versus merely foreseen (side-effect).")
    print("\n================================\n")

def scenario_prompt(scn):
    slow_print(f"\n--- Scenario: {scn['name']} ---\n")
    slow_print(scn["description"])
    slow_print("\nWhat do you choose?")
    slow_print("1. Intervene (pull lever / push / swerve)")
    slow_print("2. Do nothing (let events occur)")
    while True:
        decision = input("Enter 1 or 2: ").strip()
        if decision in ("1", "2"):
            break
        print("Please enter 1 or 2.")
    if decision == "1":
        saved = scn["saved_if_pull"]
        killed = scn["killed_if_pull"]
        slow_print(f"\nYou chose to intervene. Saved {saved}, killed {killed}.")
    else:
        saved = scn["saved_if_stay"]
        killed = scn["killed_if_stay"]
        slow_print(f"\nYou chose not to intervene. Saved {saved}, killed {killed}.")
    return decision, saved, killed

def ask_discomfort():
    while True:
        r = input("On a scale of 1–5, how uncomfortable did that feel? ").strip()
        if r == "":
            return None
        if r.isdigit() and 1 <= int(r) <= 5:
            return int(r)
        print("Please enter a number 1–5 (or press ENTER to skip).")

choose_text_speed()

slow_print("\nWELCOME TO THE TROLLEY PROBLEM MORAL SIMULATOR\n")
slow_print("I used to think trolley problems were simple:")
slow_print("   'save the most lives = right answer.'")
slow_print("But in class, I learned that morality")
slow_print("is NOT just about numbers. Intention, agency, and rights matter.")
slow_print("This program will show why.\n")

time.sleep(0.6)

scenarios = [
    {
        "name": "Classic Switch",
        "description": "A trolley is heading toward 5 workers. Pulling a lever diverts it to a track with 1 worker.",
        "saved_if_pull": 5,
        "killed_if_pull": 1,
        "saved_if_stay": 0,
        "killed_if_stay": 5,
        "type": "switch",
    },
    {
        "name": "Footbridge Push",
        "description": "A trolley heads toward 5 people. You can push a person off a footbridge to stop it, killing them but saving the others.",
        "saved_if_pull": 5,
        "killed_if_pull": 1,
        "saved_if_stay": 0,
        "killed_if_stay": 5,
        "type": "footbridge",
    },
    {
        "name": "Self-Driving Car Crash",
        "description": "Your autonomous car must choose: stay straight and hit 2 pedestrians, or swerve and kill you instead.",
        "saved_if_pull": 2,
        "killed_if_pull": 1,
        "saved_if_stay": 0,
        "killed_if_stay": 2,
        "type": "self-driving",
    },
    {
        "name": "Equal Numbers: Passenger vs. Pedestrian (1 vs 1)",
        "description": "You can swerve to sacrifice the passenger to save 1 pedestrian, or do nothing and 1 pedestrian dies.",
        "saved_if_pull": 1,
        "killed_if_pull": 1,
        "saved_if_stay": 0,
        "killed_if_stay": 1,
        "type": "equal-1v1",
    },
]

stats = {"saved": 0, "killed": 0}
discomfort_log = []

try:
    for scn in scenarios:
        decision, saved, killed = scenario_prompt(scn)
        stats["saved"] += saved
        stats["killed"] += killed
        evaluate_choice(decision, saved, killed, scn["type"])
        rating = ask_discomfort()
        if rating is not None:
            discomfort_log.append((scn["name"], rating))
        input("Press ENTER to continue...\n")

    slow_print("\nSESSION SUMMARY:")
    slow_print(f"Total saved: {stats['saved']} | Total killed: {stats['killed']}")
    if discomfort_log:
        worst = max(discomfort_log, key=lambda t: t[1])
        slow_print(f"Most uncomfortable scenario (you rated {worst[1]}/5): {worst[0]}")
    else:
        slow_print("No discomfort ratings provided.")

    slow_print("\nFINAL LESSON:")
    slow_print("Even when two scenarios have identical numbers,")
    slow_print("we judge them differently because morality is more than totals.")
    slow_print("This is the core insight of trolley philosophy—and why I originally misunderstood it.")
    slow_print("\nThank you for exploring moral reasoning!\n")

except KeyboardInterrupt:
    slow_print("\n\nSession ended. Thanks for exploring moral reasoning!\n")
