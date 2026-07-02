from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
AUTHOR_NAME = "AMY AISSATOU"
SRC_REPO = "src"
LIST_OF_REQUIREMENTS = ["streamlit"]

setup(
    name="SCR_REPO",
    version="0.0.1",
    author=AUTHOR_NAME,
    author_email="amicheikhthiam@gmail.com",
    description="Un package Python simple pour créer une application web simple.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[SRC_REPO],
    python_requires=">=3.10",
    install_requires=LIST_OF_REQUIREMENTS,
)