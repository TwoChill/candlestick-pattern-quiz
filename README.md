# Candlestick Pattern Quiz

An interactive terminal quiz that teaches you to recognize candlestick patterns used in technical analysis. For each pattern you are shown its ASCII chart, then tested on the name, explanation, and correct trading action — in three progressive rounds.

---

## What you will learn

- Identify 20 candlestick patterns by their visual shape
- Understand what each pattern signals about market sentiment
- Know the appropriate trading action for each pattern

---

## Patterns covered

**Single candle**
Doji, Long-legged Doji, Gravestone Doji, Dragonfly Doji,
Bullish Marubozu, Bearish Marubozu, Bullish Opening Marubozu, Bearish Opening Marubozu,
Bullish Closing Marubozu, Bearish Closing Marubozu,
Hammer, Inverted Hammer, Shooting Star, Hanging Man,
Long Day Bullish, Long Day Bearish, Short Day Bullish, Short Day Bearish

**Double candle**
Bullish Engulfing, Bearish Engulfing

---

## Requirements

- Python 3.8 or higher
- [colorama](https://pypi.org/project/colorama/)

---

## Installation

```bash
git clone https://github.com/TwoChill/candlestick-pattern-quiz.git
cd candlestick-pattern-quiz
pip install colorama
python main.py
```

---

## How the quiz works

Each round picks a random pattern and asks you three questions in sequence:

| Round | Question | Options |
|-------|----------|---------|
| 1 | What candlestick pattern is this? | 5 choices (A–E) |
| 2 | What is the correct explanation? | 3 choices (A–C) |
| 3 | What is the correct trading action? | 3 choices (A–C) |

A wrong answer at any round shows you the correct answer and ends that round — you will not be penalized twice.
A correct answer advances you to the next round immediately.

**Controls**

| Input | Action |
|-------|--------|
| `A` – `E` | Select answer |
| `return` | Go back / skip current round |
| `exit` | Quit the quiz |
| `Ctrl-C` or `Ctrl-D` | Quit gracefully |

---

## Project structure

```
candlestick-pattern-quiz/
├── main.py               # Quiz engine and entry point
├── single_patterns.py    # ASCII art for 18 single-candle patterns
├── double_patterns.py    # ASCII art for 2 double-candle patterns
├── explanation.py        # Three explanations per pattern
├── trading_actions.py    # One trading recommendation per pattern
├── LICENSE
└── README.md
```

---

## Extending the quiz

To add a new pattern:

1. Add its ASCII art to `single_patterns.py` or `double_patterns.py` using the same list-of-strings format.
2. Add a list of three explanations to `explanation.py` under the same key.
3. Add a trading action string to `trading_actions.py` under the same key.

The key must be identical in all three files. The quiz picks it up automatically on the next run.

---

## License

MIT — see [LICENSE](LICENSE).
