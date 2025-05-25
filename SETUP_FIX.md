# Fix for setup.py Issue

## The Issue

The root-level `setup.py` wasn't correctly finding and installing both packages in the project:
1. `qdrant_evaluation`
2. `qdrant_data_ingestion`

The issue was that `find_packages(where="src")` wasn't correctly identifying both packages.

## The Solution

The solution was to explicitly list both packages in the `packages` parameter of the `setup()` function:

```python
setup(
    name="qdrant_evaluation",
    version="0.1.0",
    packages=["qdrant_evaluation", "qdrant_data_ingestion"],
    package_dir={"": "src"},
    # ... rest of the setup parameters ...
)
```

This ensures that both packages are properly installed when using the root `setup.py`.

## Testing the Solution

To test the solution, you can run the provided test script:

```bash
# Make the script executable
chmod +x test_installation.sh

# Run the script
./test_installation.sh
```

This script will:
1. Uninstall any existing installation of the package
2. Install the package using the modified root `setup.py`
3. Run a test script to verify that both packages can be imported correctly

## Cleanup

Once you've confirmed that the root `setup.py` is working correctly, you should remove the `setup.py` file from the `src` directory, as it's not standard practice to have a `setup.py` file in the `src` directory.

```bash
# Remove the src/setup.py file
rm src/setup.py
```

## Standard Python Package Structure

The standard Python package structure is:

```
project_root/
├── setup.py
├── README.md
├── requirements.txt
└── src/
    └── package_name/
        ├── __init__.py
        └── module.py
```

With this structure, the `setup.py` file should be at the project root level, and the actual package code should be in the `src` directory.