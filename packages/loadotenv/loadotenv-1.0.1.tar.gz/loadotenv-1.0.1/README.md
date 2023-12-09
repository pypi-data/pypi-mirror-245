[![ci](https://github.com/lemredd/loadotenv/actions/workflows/core.yml/badge.svg?branch=main)](https://github.com/lemredd/loadotenv/actions/workflows/core.yml)

# `loadotenv`
Reinventing the wheel to load .env variables

## Requirement/s
- Python version: `>= 3.9`

## Installation
```python
pip install loadotenv
```

## Usage
From a `.py` file near your `.env` file:

```py
from loadotenv import load_env

load_env()
# load_env(file_loc="/loc/to/.env")
```

## Contributing
Issues and PRs are welcome!
