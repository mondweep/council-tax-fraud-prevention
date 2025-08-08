from setuptools import setup, find_packages

with open("docs/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="council-tax-fraud-prevention",
    version="1.0.0",
    author="Council Development Team",
    author_email="dev-team@council.gov.uk",
    description="AI-powered council tax fraud detection and prevention system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/council/council-tax-fraud-prevention",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Government",
        "Topic :: Office/Business :: Financial :: Accounting",
        "License :: OSI Approved :: Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.35.0",
        "pandas>=2.2.0",
        "plotly>=5.21.0",
        "numpy>=1.26.0",
        "python-dateutil>=2.9.0",
        "pydantic>=2.7.0",
        "typing-extensions>=4.12.0"
    ],
    extras_require={
        "dev": [
            "pytest>=8.2.0",
            "pytest-cov>=5.0.0",
            "black>=24.4.0",
            "flake8>=7.0.0",
            "isort>=5.13.0",
            "mypy>=1.10.0",
        ],
        "ml": [
            "scikit-learn>=1.5.0",
            "tensorflow>=2.16.0",
            "torch>=2.3.0",
        ],
        "full": [
            "requests>=2.32.0",
            "cryptography>=42.0.0",
            "jsonschema>=4.22.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fraud-detector=src.cli_demo:main",
            "fraud-dashboard=src.dashboard:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    project_urls={
        "Bug Reports": "https://github.com/council/council-tax-fraud-prevention/issues",
        "Source": "https://github.com/council/council-tax-fraud-prevention",
        "Documentation": "https://council-fraud-prevention.readthedocs.io/",
    },
)