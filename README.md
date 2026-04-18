# CandleStickPattern_Quiz

A Python-based quiz application designed to help users learn and identify various candlestick patterns used in technical analysis for trading. This script dynamically imports candlestick pattern files, presents a quiz to the user, and provides explanations and trading actions based on user responses.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Pattern Files](#pattern-files)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Interactive Quiz**: Test your knowledge by identifying various candlestick patterns through multiple-choice questions.
- **Dynamic Imports**: Automatically loads pattern files from the directory to keep the quiz up-to-date with the latest patterns.
- **Detailed Explanations**: Provides clear explanations for each pattern, helping users understand the significance and characteristics of the pattern.
- **Trading Actions**: Suggests trading actions or strategies based on user responses and the identified patterns.
- **Customizable and Extensible**: Easily add new pattern files or modify existing ones to expand or tailor the quiz to your needs.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/TwoChill/CandleStickPattern_Quiz.git
    cd CandleStickPattern_Quiz
    ```

2. **Install Required Packages**:
    Ensure you have the necessary Python packages installed. You can install them using pip:
    ```bash
    pip install colorama termcolor
    ```

3. **Run the Script**:
    Start the quiz by running:
    ```bash
    python main.py
    ```

## Usage

- Upon running the script, you will be prompted to select candlestick pattern files to include in the quiz.
- Answer multiple-choice questions to identify different candlestick patterns.
- The quiz will provide explanations and trading actions based on your answers to help you learn and improve your technical analysis skills.

## Pattern Files

- `single_patterns.py`: Contains definitions for individual candlestick patterns such as Doji, Bullish Marubozu, Bearish Marubozu, and others.
- Additional pattern files can be added in the same format as `single_patterns.py` to introduce new patterns to the quiz.
  
## Contributing

Contributions are highly encouraged! To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m "Add some feature"`).
4. Push your branch (`git push origin feature-branch`).
5. Open a pull request and provide a brief description of your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

For questions or suggestions, feel free to reach out! Happy learning and trading!
