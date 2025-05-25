import qdrant_client
import openai
import dotenv

print("All imports successful!")

# Get versions safely
try:
    print(f"qdrant_client version: {qdrant_client.__version__}")
except AttributeError:
    print("qdrant_client is installed (version attribute not available)")

try:
    print(f"openai version: {openai.__version__}")
except AttributeError:
    print("openai is installed (version attribute not available)")

try:
    print(f"dotenv version: {dotenv.__version__}")
except AttributeError:
    print("dotenv is installed (version attribute not available)")