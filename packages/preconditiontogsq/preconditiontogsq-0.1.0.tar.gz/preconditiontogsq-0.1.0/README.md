# preconditiontogsq

A Python library for converting Stardew Valley event preconditions to Game State Queries.

## Features

- Converting vanilla preconditions to GSQs.

## Installation

```bash
pip install preconditiontogsq
```

## Usage and Examples

```python
from preconditiontogsq import convert

print(convert('t 600 1400')) # TIME 600 1400

```

Further examples can be found in the [tests](https://github.com/AnotherPillow/preconditiontogsq/tree/main/tests) directory.

## Development/Testing

- Install dependencies with `pip install -r requirements.txt`
- Tests can be added to tests/name_of_test.py and run with `py -m tests.name_of_test`
- It can be built with `py -m build`
