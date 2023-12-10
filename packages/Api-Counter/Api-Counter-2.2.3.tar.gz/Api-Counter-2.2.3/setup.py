from pathlib import Path

from setuptools import setup, find_packages

req_tests = ["pytest"]
req_lint = ["flake8", "flake8-docstrings"]
req_etc = ["black", "isort"]
req_dev = req_tests + req_lint + req_etc

with open('requirements.txt', 'r') as f:
    install_requires = [
        s for s in [
            line.split('#', 1)[0].strip(' \t\n') for line in f
        ] if s != ''
    ]

# read the contents of README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup_options = {
    "name": "Api-Counter",
    "version": "2.2.3",
    "url": "https://github.com/windies21/api-counter",
    "author": "winDy",
    "author_email": "winDy@windystudio.com",
    "license": "MIT",
    "description": "Simple API Counter from log files or folder.",
    "packages": find_packages(),
    "python_requires": ">=3.11.0",
    "install_requires": install_requires,
    "extras_require": {
        "tests": req_tests,
        "lint": req_lint,
        "dev": req_dev
    },
    "package_dir": {"": "."},
    "entry_points": {
        "console_scripts": [
            "counter=url_counter.main:main",
        ],
    },
    "long_description": long_description,
    "long_description_content_type": 'text/markdown',
}

setup(**setup_options)
