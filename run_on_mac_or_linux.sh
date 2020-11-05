#!/bin/bash

echo "Setting up venv... ..."
python3 -m venv ./venv
source ./venv/bin/activate
echo "Installing required Python packages... ..."
pip3 install -r requirements.txt
python3 run_extraction_and_generation.py
read -p "Finished extracting. Press enter to continue... ..." placeholdervar
