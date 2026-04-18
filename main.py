import os
import random

try:
    from colorama import init
except ImportError:
    print("colorama is required. Install it with: pip install colorama")
    raise

init(autoreset=True)

RED = "\033[0;31m"
GREEN = "\033[0;32m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_RED = "\033[1;31m"
YELLOW = "\033[1;33m"
BOLD = "\033[1m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
NEGATIVE = "\033[7m"
RESET = "\033[0m"

from single_patterns import patterns as single_patterns
from double_patterns import patterns as double_patterns
from explanation import explanations
from trading_actions import trading_actions

LETTERS = ['A', 'B', 'C', 'D', 'E']


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_input_with_exit(prompt):
    try:
        user_input = input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{RED}{BOLD}Exiting the quiz. Goodbye!{RESET}")
        raise SystemExit(0)
    if user_input == 'exit':
        print(f"{RED}{BOLD}\nExiting the quiz. Goodbye!{RESET}")
        raise SystemExit(0)
    if user_input == 'return':
        return None
    return user_input


def ask_multiple_choice(header, correct, distractors, art):
    """Render one question. Returns True/False for correct/wrong, or None if user typed 'return'."""
    options = [correct] + list(distractors)
    random.shuffle(options)
    letters = LETTERS[:len(options)]

    clear_screen()
    print(f"\n{PURPLE}{BOLD}{UNDERLINE}{header}{RESET}\n")
    print(f"{GREEN}{BOLD}\n" + "\n".join(art) + f"\n{RESET}")
    print(f"{CYAN}/Options:\n{RESET}")
    for letter, opt in zip(letters, options):
        print(f"{letter}. {opt}")

    answer = get_input_with_exit(
        f"\n{YELLOW}Your answer: {RESET}"
    )
    if answer is None:
        return None
    return answer.upper() == letters[options.index(correct)]


def wait_for_continue(short=None):
    if short is None:
        get_input_with_exit(
            f"{YELLOW}Press Enter to continue: (type 'return' to go back, 'exit' to quit) {RESET}"
        )
    else:
        get_input_with_exit(
            f"{YELLOW}\nPress Enter to continue... {RESET}"
        )


def pattern_name_quiz(candlestick_patterns, explanations, trading_actions):
    names = list(candlestick_patterns.keys())
    if len(names) < 5:
        raise RuntimeError(f"need at least 5 patterns, got {len(names)}")

    correct_pattern = random.choice(names)
    art = candlestick_patterns[correct_pattern]

    distractors = random.sample([n for n in names if n != correct_pattern], 4)
    result = ask_multiple_choice(
        f"{BOLD}What candlestick pattern is this?{RESET}", correct_pattern, distractors, art
    )
    if result is None:
        return
    if not result:
        print(
            f"{RED}{ITALIC}{BOLD}\nWrong!\n{RESET}"
            f"{RED}{UNDERLINE}The correct answer is:{RESET}"
            f"{LIGHT_RED}{NEGATIVE}{BOLD}{correct_pattern}{RESET}\n"
        )
        wait_for_continue()
        return
    print(
        f"{GREEN}{ITALIC}{BOLD}\nCorrect!{RESET}{GREEN}\n"
        f"The pattern is {NEGATIVE}{correct_pattern}{RESET}"
    )
    wait_for_continue(1)

    correct_exp = explanations[correct_pattern][0]
    exp_distractors = random.sample(
        [explanations[k][0] for k in explanations if k != correct_pattern], 2
    )
    result = ask_multiple_choice(
        f"What is the correct explanation for the {GREEN}{NEGATIVE}{UNDERLINE}{correct_pattern}{RESET}{PURPLE}{BOLD}{UNDERLINE} pattern?",
        correct_exp, exp_distractors, art,
    )
    if result is None:
        return
    if not result:
        print(
            f"{RED}{ITALIC}{BOLD}\nWrong!\n\nThe correct explanation is:\n\n{RESET}"
            f"{GREEN}{UNDERLINE}{BOLD}{NEGATIVE}\t{correct_exp}{RESET}\n"
        )
        wait_for_continue()
        return
    print(f"{GREEN}{BOLD}\nCorrect! The explanation is: {correct_exp}\n{RESET}")
    wait_for_continue(1)

    correct_action = trading_actions[correct_pattern]
    action_distractors = random.sample(
        [v for k, v in trading_actions.items() if k != correct_pattern], 2
    )
    result = ask_multiple_choice(
        f"What is the correct trading action for the {GREEN}{NEGATIVE}{UNDERLINE}{correct_pattern}{RESET}{PURPLE}{BOLD}{UNDERLINE} pattern?",
        correct_action, action_distractors, art,
    )
    if result is None:
        return
    if result:
        print(f"{GREEN}{BOLD}\nCorrect! The trading action is: {correct_action}\n{RESET}")
    else:
        print(
            f"{RED}{ITALIC}{BOLD}\nWrong!\n\nThe correct trading action is: {RESET}"
            f"{GREEN}{UNDERLINE}{BOLD}{correct_action}{RESET}\n"
        )
    wait_for_continue()


def main():
    candlestick_patterns = {**single_patterns, **double_patterns}
    while True:
        clear_screen()
        pattern_name_quiz(candlestick_patterns, explanations, trading_actions)


if __name__ == "__main__":
    main()
