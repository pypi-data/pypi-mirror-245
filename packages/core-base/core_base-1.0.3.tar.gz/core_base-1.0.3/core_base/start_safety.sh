#!/usr/bin/env bash
cd venv&&
source bin/activate&&
pip install --upgrade safety >> a.txt&&
safety check --json