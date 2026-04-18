"""Stress test — try to break the quiz."""
import builtins
import io
import random
from contextlib import redirect_stdout
from unittest.mock import patch

import main
from single_patterns import patterns as sp
from double_patterns import patterns as dp
from explanation import explanations
from trading_actions import trading_actions

PATTERNS = {**sp, **dp}


def feeder(answers):
    it = iter(answers)

    def _(prompt=""):
        try:
            return next(it)
        except StopIteration:
            raise EOFError("no more input")

    return _


def drive(answers, seed=0):
    random.seed(seed)
    buf = io.StringIO()
    err = None
    code = None
    try:
        with patch.object(builtins, "input", feeder(answers)), redirect_stdout(buf):
            main.pattern_name_quiz(PATTERNS, explanations, trading_actions)
    except SystemExit as e:
        code = e.code
    except BaseException as e:
        err = e
    return buf.getvalue(), err, code


print("=== BREAK ATTEMPTS ===\n")

# 1. EOF (Ctrl-D / stdin closed) — currently raises uncaught EOFError
out, err, code = drive([])
print(f"1. EOF on first input: error={type(err).__name__ if err else None}")

# 2. Whitespace-only
out, err, code = drive(["   ", ""])
print(f"2. Whitespace answer:  error={type(err).__name__ if err else None}, wrong-branch={'Wrong!' in out}")

# 3. Multi-char answer like 'AB'
out, err, code = drive(["AB", ""])
print(f"3. Multi-char 'AB':    error={type(err).__name__ if err else None}, wrong-branch={'Wrong!' in out}")

# 4. Extremely long input
out, err, code = drive(["A" * 10_000, ""])
print(f"4. 10k-char input:     error={type(err).__name__ if err else None}")

# 5. Non-ascii input
out, err, code = drive(["\u00e9\u00e9", ""])
print(f"5. Non-ASCII input:    error={type(err).__name__ if err else None}")

# 6. Input with embedded newlines — input() already strips at newline, but .strip() handles trailing spaces
out, err, code = drive(["  A  ", ""])
# Find what letter is correct for seed=0
random.seed(0)
names = list(PATTERNS.keys())
cp = random.choice(names)
inc = random.sample([n for n in names if n != cp], 4)
opts = [cp] + inc
random.shuffle(opts)
correct_letter = ["A", "B", "C", "D", "E"][opts.index(cp)]
print(f"6. Padded '  A  ':     correct_letter={correct_letter}, got-correct={out.count('Correct!')>0}")

# 7. Reduce pattern pool to <5 — should break random.sample(..., 4)
import copy
small = {k: PATTERNS[k] for k in list(PATTERNS)[:3]}
try:
    random.seed(0)
    buf = io.StringIO()
    with patch.object(builtins, "input", feeder([])), redirect_stdout(buf):
        main.pattern_name_quiz(small, explanations, trading_actions)
    print("7. Pool<5 patterns:    no error?!")
except (ValueError, RuntimeError) as e:
    print(f"7. Pool<5 patterns:    {type(e).__name__} (expected): {e}")
except Exception as e:
    print(f"7. Pool<5 patterns:    {type(e).__name__}: {e}")

# 8. KeyboardInterrupt during input
def raising_input(prompt=""):
    raise KeyboardInterrupt

try:
    random.seed(0)
    buf = io.StringIO()
    with patch.object(builtins, "input", raising_input), redirect_stdout(buf):
        main.pattern_name_quiz(PATTERNS, explanations, trading_actions)
    print("8. Ctrl-C:             no error?!")
except SystemExit as e:
    print(f"8. Ctrl-C:             graceful SystemExit({e.code})")
except KeyboardInterrupt:
    print("8. Ctrl-C:             KeyboardInterrupt bubbles up (traceback shown to user)")
except Exception as e:
    print(f"8. Ctrl-C:             {type(e).__name__}: {e}")

# 9. EOFError during input (Ctrl-D)
def eof_input(prompt=""):
    raise EOFError

try:
    random.seed(0)
    buf = io.StringIO()
    with patch.object(builtins, "input", eof_input), redirect_stdout(buf):
        main.pattern_name_quiz(PATTERNS, explanations, trading_actions)
    print("9. Ctrl-D (EOF):       no error?!")
except SystemExit as e:
    print(f"9. Ctrl-D (EOF):       graceful SystemExit({e.code})")
except EOFError:
    print("9. Ctrl-D (EOF):       EOFError bubbles up (traceback shown to user)")
except Exception as e:
    print(f"9. Ctrl-D (EOF):       {type(e).__name__}: {e}")
