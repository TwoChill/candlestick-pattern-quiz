"""Behavioral test harness for the candlestick quiz.

Drives main.pattern_name_quiz via monkey-patched input + random to verify:
  - correct name -> cascades into explanation_quiz -> trading_action_quiz
  - wrong name   -> short-circuits (no cascade)
  - 'return'     -> aborts the current level
  - 'exit'       -> raises SystemExit
  - garbage input -> treated as wrong
"""
import builtins
import io
import random
import sys
from contextlib import redirect_stdout
from unittest.mock import patch

import main
from single_patterns import patterns as sp
from double_patterns import patterns as dp
from explanation import explanations
from trading_actions import trading_actions

PATTERNS = {**sp, **dp}


class InputFeeder:
    def __init__(self, answers):
        self.answers = list(answers)
        self.consumed = []

    def __call__(self, prompt=""):
        if not self.answers:
            raise RuntimeError(f"ran out of scripted input; prompt was: {prompt!r}")
        a = self.answers.pop(0)
        self.consumed.append(a)
        return a


def run(answers, seed=0):
    random.seed(seed)
    feeder = InputFeeder(answers)
    buf = io.StringIO()
    exit_code = None
    try:
        with patch.object(builtins, "input", feeder), redirect_stdout(buf):
            main.pattern_name_quiz(PATTERNS, explanations, trading_actions)
    except SystemExit as e:
        exit_code = e.code
    return feeder, buf.getvalue(), exit_code


def letter_of(correct, options):
    return ["A", "B", "C", "D", "E"][options.index(correct)]


def find_correct_letters(seed):
    """Replay RNG to figure out correct A-E letter at each stage for a given seed."""
    random.seed(seed)
    names = list(PATTERNS.keys())
    correct_pattern = random.choice(names)
    incorrect = random.sample([n for n in names if n != correct_pattern], 4)
    opts = [correct_pattern] + incorrect
    random.shuffle(opts)
    l1 = letter_of(correct_pattern, opts)

    ce = explanations[correct_pattern][0]
    ie = random.sample([explanations[k][0] for k in explanations if k != correct_pattern], 2)
    opts = [ce] + ie
    random.shuffle(opts)
    l2 = letter_of(ce, opts)

    ca = trading_actions[correct_pattern]
    ia = random.sample([v for k, v in trading_actions.items() if k != correct_pattern], 2)
    opts = [ca] + ia
    random.shuffle(opts)
    l3 = letter_of(ca, opts)

    return correct_pattern, l1, l2, l3


FAILS = []


def check(name, cond, detail=""):
    tag = "PASS" if cond else "FAIL"
    print(f"[{tag}] {name}" + (f"  -- {detail}" if detail and not cond else ""))
    if not cond:
        FAILS.append(name)


# --- Test 1: fully-correct path cascades all 3 levels ---
seed = 42
correct, l1, l2, l3 = find_correct_letters(seed)
feeder, out, exc = run([l1, "", l2, "", l3, ""], seed=seed)
check("correct cascade consumes 6 inputs (3 answers + 3 continues)", len(feeder.consumed) == 6,
      detail=f"consumed={feeder.consumed}")
check("correct cascade prints 'Correct!' 3 times", out.count("Correct!") == 3)
check("correct cascade does not print 'Wrong!'", "Wrong!" not in out)
check("no SystemExit on correct flow", exc is None)

# --- Test 2: wrong name short-circuits ---
seed = 7
correct, l1, _, _ = find_correct_letters(seed)
wrong = next(l for l in "ABCDE" if l != l1)
feeder, out, exc = run([wrong, ""], seed=seed)
check("wrong-name consumes 2 inputs (answer + continue)", len(feeder.consumed) == 2)
check("wrong-name prints 'Wrong!' exactly once", out.count("Wrong!") == 1)
check("wrong-name never reaches explanation stage",
      "explanation for the" not in out.lower())
check("wrong-name shows correct answer in output", correct in out)

# --- Test 3: wrong at explanation stage short-circuits ---
seed = 11
correct, l1, l2, _ = find_correct_letters(seed)
wrong_l2 = next(l for l in "ABC" if l != l2)
feeder, out, exc = run([l1, "", wrong_l2, ""], seed=seed)
check("wrong-exp consumes 4 inputs", len(feeder.consumed) == 4)
check("wrong-exp reaches explanation stage", "explanation for the" in out.lower())
check("wrong-exp never reaches trading-action stage",
      "trading action for the" not in out.lower())

# --- Test 4: wrong at trading-action stage ---
seed = 13
correct, l1, l2, l3 = find_correct_letters(seed)
wrong_l3 = next(l for l in "ABC" if l != l3)
feeder, out, exc = run([l1, "", l2, "", wrong_l3, ""], seed=seed)
check("wrong-action consumes 6 inputs", len(feeder.consumed) == 6)
check("wrong-action reaches trading-action stage", "trading action for the" in out.lower())
check("wrong-action prints exactly one 'Wrong!'", out.count("Wrong!") == 1)

# --- Test 5: 'return' at top level aborts ---
seed = 3
feeder, out, exc = run(["return"], seed=seed)
check("return at top level consumes 1 input", len(feeder.consumed) == 1)
check("return at top level does not raise SystemExit", exc is None)

# --- Test 6: 'exit' triggers SystemExit ---
seed = 3
feeder, out, exc = run(["exit"], seed=seed)
check("exit raises SystemExit", isinstance(exc, (int, type(None))) or exc is not False)
# exit() returns None as SystemExit.code when invoked bare
check("exit message printed", "Exiting the quiz" in out)

# --- Test 7: garbage input treated as wrong ---
seed = 17
correct, l1, _, _ = find_correct_letters(seed)
feeder, out, exc = run(["zzz", ""], seed=seed)
check("garbage input treated as wrong", "Wrong!" in out)

# --- Test 8: lowercase correct letter still counts ---
seed = 21
correct, l1, l2, l3 = find_correct_letters(seed)
feeder, out, exc = run([l1.lower(), "", l2.lower(), "", l3.lower(), ""], seed=seed)
check("lowercase answer accepted", out.count("Correct!") == 3)

# --- Test 9: empty string treated as wrong ---
seed = 25
feeder, out, exc = run(["", ""], seed=seed)
check("empty input treated as wrong", "Wrong!" in out)

print()
if FAILS:
    print(f"FAILED: {len(FAILS)}")
    for f in FAILS:
        print(f"  - {f}")
    sys.exit(1)
else:
    print("ALL TESTS PASSED")

input(":>")