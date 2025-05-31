from setuptools import setup, find_packages

setup(
    name="qdrant_evaluation",
    version="0.1.0",
    packages=["qdrant_evaluation", "qdrant_data_ingestion", "qdrant_simple_rag"],
    package_dir={"": "src"},
    install_requires=[
        "qdrant-client>=1.1.0",
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "pandas>=1.3.0",
        "faiss-cpu>=1.7.4",
        "sentence-transformers>=2.2.2",
        "requests>=2.28.0",
    ],
    author="Daniel Wirth",
    author_email="dnlwrthstr@gmail.com",
    description="Evaluation and benchmarking of Qdrant vector database configurations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dnlwrthstr/qdrant-evaluation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
