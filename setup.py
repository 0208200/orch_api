from setuptools import setup, find_packages
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="orch_api",
    version="0.0.1",
    author="Muktadir",
    description="Connect to Uipath orchestrator api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/foxpc-ai/orch_api",
    packages=find_packages(),
    install_requires=[
        # none
    ],
)