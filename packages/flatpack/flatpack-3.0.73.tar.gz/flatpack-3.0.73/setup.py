from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="flatpack",
    version="3.0.73",
    packages=find_packages(),
    install_requires=[
        "cryptography==41.0.7",
        "gradio==4.8.0",
        "httpx==0.25.2",
        "lida==0.0.10",
        "llmx==0.0.18a0",
        "requests==2.31.0",
        "toml==0.10.2",
        "torch==2.1.0"
    ],
    author="Romlin Group AB",
    author_email="hello@romlin.com",
    description="Ready-to-assemble AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "flatpack=flatpack.main:main"
        ],
    }
)
