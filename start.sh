#!/bin/bash

source .venv/bin/activate
watchmedo auto-restart --pattern "*.py" --recursive --signal SIGTERM python server.py
