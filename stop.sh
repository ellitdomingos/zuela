#!/bin/bash

pkill -f "ollama serve"
pkill -f "main.py"
pkill -f "streamlit"

echo "Sistema parado"
