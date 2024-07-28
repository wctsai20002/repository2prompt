from setuptools import setup, find_packages

setup(
    name="repository2prompt",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "jinja2",
    ],
    entry_points={
        "console_scripts": [
            "repository2prompt=repository2prompt.repository2prompt:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to convert GitHub repositories into LLM prompts",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/repository2prompt",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)