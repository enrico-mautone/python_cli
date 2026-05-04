# python_cli

A Python command-line tool for managing virtual environments and basic project setup.

## Overview

This CLI tool provides simple commands to create virtual environments, scaffold new Python projects, generate `requirements.txt` files, and install dependencies.

## Requirements

- Python 3
- click
- rich

## Installation

Install dependencies:

```bash
pip install click rich
```

Run the CLI:

```bash
python main.py
```

## Commands

### Create a virtual environment

```bash
python main.py venv -n .venv
```

Optional prompt name:

```bash
python main.py venv -n .venv -p myproject
```

### Create a new project

```bash
python main.py project my_project
```

This creates:
- a project folder
- a virtual environment (`.venv`)
- an empty `requirements.txt`

### Generate requirements.txt

```bash
python main.py req --file script.py
```

Scans the file for imports and writes non-standard libraries to `requirements.txt`.

If no file is provided:

```bash
python main.py req
```

Creates an empty `requirements.txt`.

### Install dependencies

```bash
python main.py install
```

Installs packages from `requirements.txt`.

### Help

```bash
python main.py help
```

Displays available commands.

## Notes

- Virtual environments are created using Python’s built-in `venv` module.
- Requirements generation is based on simple import parsing and may require manual adjustments.
- Paths and activation instructions vary depending on the operating system.
