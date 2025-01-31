from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="repository2prompt",
    version="1.0.0",
    author="tweichuan",
    author_email="wctsai20002@gmail.com",
    description="A tool to convert GitHub repositories into LLM prompts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wctsai20002/repository2prompt",
    packages=find_packages(include=['repository2prompt', 'repository2prompt.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        'pyyaml>=6.0',
        'requests>=2.26.0',
        'jinja2>=3.0.1',
    ],
    entry_points={
        'console_scripts': [
            'repository2prompt=repository2prompt.cli:main',
        ],
    },
    include_package_data=True,
    package_data={
        'repository2prompt': ['templates/*.j2', '*.yaml'],
    },
)