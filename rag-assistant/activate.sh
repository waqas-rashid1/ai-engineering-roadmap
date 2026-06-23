#!/usr/bin/env bash
# Activate the project virtual environment.
# Venv lives in ~/.venvs/rag-assistant (home dir) because this drive is slow
# for the thousands of small files a venv creates.
source "$HOME/.venvs/rag-assistant/bin/activate"
echo "Activated: $(which python) ($(python --version))"
