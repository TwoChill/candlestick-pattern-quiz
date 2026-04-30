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
DIM = "\033[2m"

from single_patterns import patterns as single_patterns
from double_patterns import patterns as double_patterns
from explanation import explanations
from trading_actions import trading_actions

LETTERS = ['A', 'B', 'C', 'D', 'E']


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def stage_indicator(current_stage):
    stages = ["1· Name", "2· Explain", "3· Trade"]
    parts = []
    for i, label in enumerate(stages, start=1):
        if i == current_stage:
            parts.append(f"{GREEN}{BOLD}[ {label} ]{RESET}")
        else:
            parts.append(f"{DIM}[ {label} ]{RESET}")
    print("  " + f"  {DIM}›{RESET}  ".join(parts) + "\n")


def get_input_with_exit(prompt, allow_return=True):
    try:
        user_input = input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{RED}{BOLD}Exiting the quiz. Goodbye!{RESET}")
        raise SystemExit(0)
    if user_input == 'exit':
        print(f"{RED}{BOLD}\nExiting the quiz. Goodbye!{RESET}")
        raise SystemExit(0)
    if allow_return and user_input == 'return':
        return None
    return user_input


def ask_multiple_choice(header, options, correct, art, allow_return=True, stage=None):
    """Render one question. options is pre-shuffled. Returns True/False/None (return)."""
    letters = LETTERS[:len(options)]

    clear_screen()
    if stage is not None:
        stage_indicator(stage)
    print(f"\n{PURPLE}{BOLD}{UNDERLINE}{header}{RESET}\n")
    print(f"{GREEN}{BOLD}\n" + "\n".join(art) + f"\n{RESET}")
    print(f"{CYAN}Options:\n{RESET}")
    for letter, opt in zip(letters, options):
        print(f"{letter}. {opt}")

    answer = get_input_with_exit(f"\n{YELLOW}Your answer: {RESET}", allow_return=allow_return)
    if answer is None:
        return None
    return answer.upper() == letters[options.index(correct)]


def wait_for_continue(short=None):
    if short is None:
        get_input_with_exit(
            f"\n{YELLOW}Press Enter to continue: (type 'return' to go back, 'exit' to quit) {RESET}"
        )
    else:
        get_input_with_exit(
            f"\n{YELLOW}Press Enter to continue... {RESET}"
        )


def pattern_name_quiz(candlestick_patterns, explanations, trading_actions):
    names = list(candlestick_patterns.keys())
    if len(names) < 5:
        raise RuntimeError(f"need at least 5 patterns, got {len(names)}")

    correct_pattern = random.choice(names)
    art = candlestick_patterns[correct_pattern]

    # Pre-compute all options once so 'return' replays the identical question.
    name_options = [correct_pattern] + random.sample([n for n in names if n != correct_pattern], 4)
    random.shuffle(name_options)

    correct_exp = explanations[correct_pattern][0]
    exp_options = [correct_exp] + random.sample(
        [explanations[k][0] for k in explanations if k != correct_pattern], 2
    )
    random.shuffle(exp_options)

    correct_action = trading_actions[correct_pattern]
    action_options = [correct_action] + random.sample(
        [v for k, v in trading_actions.items() if k != correct_pattern], 2
    )
    random.shuffle(action_options)

    stage = 1
    while True:
        if stage == 1:
            result = ask_multiple_choice(
                f"{BOLD}What candlestick pattern is this?{RESET}",
                name_options, correct_pattern, art, allow_return=True, stage=1,
            )
            if result is None:
                continue
            if not result:
                print(
                    f"{RED}{ITALIC}{BOLD}\nWrong!\n\n{RESET}"
                    f"{RED}{UNDERLINE}The correct answer is:{RESET} "
                    f"{LIGHT_RED}{NEGATIVE}{BOLD}{correct_pattern}{RESET}\n"
                )
                wait_for_continue()
                return
            print(
                f"{GREEN}{ITALIC}{BOLD}\nCorrect!{RESET}{GREEN}\n\n"
                f"The pattern is: {NEGATIVE}{correct_pattern}{RESET}"
            )
            wait_for_continue(1)
            stage = 2

        elif stage == 2:
            result = ask_multiple_choice(
                f"What is the correct explanation for the {GREEN}{NEGATIVE}{UNDERLINE}{correct_pattern}{RESET}{PURPLE}{BOLD}{UNDERLINE} pattern?",
                exp_options, correct_exp, art, allow_return=True, stage=2,
            )
            if result is None:
                stage = 1
                continue
            if not result:
                print(
                    f"{RED}{ITALIC}{BOLD}\nWrong!\n\nThe correct explanation is:\n\n{RESET}"
                    f"{GREEN}{UNDERLINE}{BOLD}{NEGATIVE}{correct_exp}{RESET}\n"
                )
                wait_for_continue()
                return
            print(
                f"{GREEN}{ITALIC}{BOLD}\nCorrect!{RESET}{GREEN}\n\n"
                f"The explanation is:\n\n{NEGATIVE}{correct_exp}{RESET}"
            )
            wait_for_continue(1)
            stage = 3

        elif stage == 3:
            result = ask_multiple_choice(
                f"What is the correct trading action for the {GREEN}{NEGATIVE}{UNDERLINE}{correct_pattern}{RESET}{PURPLE}{BOLD}{UNDERLINE} pattern?",
                action_options, correct_action, art, allow_return=True, stage=3,
            )
            if result is None:
                stage = 2
                continue
            if result:
                print(
                    f"{GREEN}{ITALIC}{BOLD}\nCorrect!{RESET}{GREEN}\n\n"
                    f"The trading action is:\n\n{NEGATIVE}{correct_action}{RESET}"
                )
                wait_for_continue(1)
            else:
                print(
                    f"{RED}{ITALIC}{BOLD}\nWrong!\n\nThe correct trading action is: {RESET}"
                    f"{GREEN}{UNDERLINE}{BOLD}{correct_action}{RESET}\n"
                )
                wait_for_continue()
            return


def main():
    candlestick_patterns = {**single_patterns, **double_patterns}
    while True:
        clear_screen()
        pattern_name_quiz(candlestick_patterns, explanations, trading_actions)


if __name__ == "__main__":
    main()
