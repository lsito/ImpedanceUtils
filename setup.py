from setuptools import setup, find_packages

setup(
    name="ImpedanceUtils",  # Name of your package
    version="0.1.0",  # Initial release version
    author="Leonardo Sito",  # Your name
    author_email="leonardo.sito@cern.ch",  # Your email
    description="A package for handling wake function FFT computations",  # Short description
    long_description=open("README.md").read(),  # Optional, long description from README
    long_description_content_type="text/markdown",  # If README is in Markdown format
    #url="https://github.com/yourusername/my_package",  # URL to the package repo (GitHub)
    packages=find_packages(),  # Automatically find all packages in this directory
    install_requires=[  # List any package dependencies
        "numpy", 
        "pandas",
        # Add other dependencies here if needed
    ],
    classifiers=[  # Optional: Classifiers to describe the project
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify the Python version requirement
)