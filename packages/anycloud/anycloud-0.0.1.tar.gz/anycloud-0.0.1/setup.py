from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="anycloud",
    version="0.0.1",
    author="Applens.inc",
    author_email="contact@applens.io",
    description="Always choose the cheapest cloud.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/applens-inc/anycloud",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Add your project dependencies here
        "numpy",
        "requests",
        # Add other dependencies as needed
    ],
)
