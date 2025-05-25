#!/bin/bash

# Script to test the installation of the package using the root setup.py

echo "Testing installation of the package using the root setup.py..."

# Uninstall any existing installation of the package
echo "Uninstalling any existing installation of the package..."
pip uninstall -y qdrant_evaluation

# Install the package using the root setup.py
echo "Installing the package using the root setup.py..."
pip install -e ..

# Run the test script to verify that both packages can be imported correctly
echo "Running the test script to verify that both packages can be imported correctly..."
python ./test_package_imports.py

echo "Test completed."