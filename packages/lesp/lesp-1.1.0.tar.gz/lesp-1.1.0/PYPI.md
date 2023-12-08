# LESP - Lightweight Efficient Spelling Proofreader

[![Version](https://img.shields.io/badge/Version-1.0.0-gold.svg)](https://pypi.org/project/lesp/)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Python](https://img.shields.io/badge/Python-3.6+-green.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)](https://github.com/LyubomirT/lesp)
[![Dependencies](https://img.shields.io/badge/Dependencies-none-red.svg)](https://github.com/LyubomirT/lesp)

## Welcome to LESP - Lightweight Efficient Spelling Proofreader!

LESP is a lightweight, efficient spelling proofreader for Python, designed to be easy to use and resource-friendly.

## Features

- Lightweight and efficient
- Easy to use
- Cross-platform (Linux, Windows, macOS)
- No external dependencies

## Installation

```bash
pip install lesp
```

## Usage

```python
from lesp.autocorrect import Proofreader

proofreader = Proofreader()
is_correct = proofreader.is_correct("apgle")  # False

if not is_correct:
    similar_word = proofreader.get_similar("apgle")
    print("Did you mean:", similar_word)  # Did you mean: apple
```

For detailed usage and configuration options, check the [documentation](https://lesp.gitbook.io/lesp).

## Contributing

Contributions are welcome! Check out the [GitHub repository](https://github.com/LyubomirT/lesp) and feel free to open issues or pull requests.

## License

This project is licensed under the BSD 3-Clause License. See the [LICENSE](https://github.com/LyubomirT/lesp/blob/main/LICENSE) file for details.

## Acknowledgements

Thanks to [Google 10000 English](https://github.com/first20hours/google-10000-english) and [English Word List](https://github.com/dwyl/english-words) for contributing to the wordlist.

## Contact

For discussions or support, join the [Discord Server](https://discord.gg/XkjPDcSfNz) or DM @lyubomirt.

[![Contributors](https://contrib.rocks/image?repo=lyubomirt/lesp)](https://github.com/lyubomirt/lesp/graphs/contributors)