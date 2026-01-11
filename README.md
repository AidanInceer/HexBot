# HexBot

**HexBot** is a Catan clone implemented in Python, originally designed for terminal play and AI model training, now modernized with a web interface using [NiceGUI](https://nicegui.io/).

## Features
- Full Catan board generation and logic.
- Bot players for simulation and training.
- Web-based interface to visualize the board and play the game.
- Modern Python stack (Python 3.13, `uv` dependency management).

## Requirements
- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (Recommended for dependency management)

## Getting Started

### Installation

1.  Clone the repository.
2.  Install dependencies using `uv`:
    ```bash
    uv sync
    ```

### Running the Web App

To start the web interface:

```bash
uv run webapp.py
```

This will launch the application and typically open it in your browser automatically (or visit `http://127.0.0.1:8080`).

### Running Tests

To run the test suite:

```bash
uv run pytest
```

## Development

This project uses `ruff` for linting and formatting.
- Check code: `uv run ruff check .`
- Format code: `uv run ruff format .`

## CI/CD
The project uses GitHub Actions for CI, running tests and linting on push/PR.
