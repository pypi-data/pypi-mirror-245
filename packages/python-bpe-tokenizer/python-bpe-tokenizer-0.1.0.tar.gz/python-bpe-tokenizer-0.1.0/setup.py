from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="python-bpe-tokenizer",
    version="0.1.0",
    author="jafarmahin",
    author_email="jafarmahin107@iit.du.ac.bd",
    description="Python based BPE Tokenizer",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=[
        'transformers',
    ],
    entry_points={
        'console_scripts': [
            'bpe-tokenizer = bpe_tokenizer.bpe_tokenizer:main',
        ],
    },

    python_requires=">=3.6"
)
