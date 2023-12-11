# import os
from pathlib import Path

from setuptools import find_packages, setup

PACKAGE_NAME = "pypi_templates"

AUTHOR = "lgf4591"
AUTHOR_EMAIL = f"{AUTHOR}@outlook.com"


ROOT_DIR = Path(__file__).parent.resolve()
# PROJECT_NAME = os.path.basename(ROOT_DIR)
# BUG: error in pypi_templates_0.0.5 setup command: Problems to parse EntryPoint(name='pypi_templates_0.0.5'
# PACKAGE_NAME = PROJECT_NAME.replace("-","_")
URL = f"https://github.com/{AUTHOR}/{PACKAGE_NAME}"

LONG_DESCRIPTION = (ROOT_DIR / "README.md").read_text(encoding="utf-8")

setup(
    name=PACKAGE_NAME,
    # version=VERSION,
    # version="0.1.0",
    setup_requires=["setuptools_scm"],
    # use_scm_version=True,
    use_scm_version={
        "version_scheme": "post-release",
        "local_scheme": "dirty-tag",
    },
    # use_scm_version={"write_to": f"src/{PACKAGE_NAME}/__version__.py"},
    description="A python package template to upload to pypi",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="pypi, template, development",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={
        f"{PACKAGE_NAME}": ["*.dat"],
    },
    include_package_data=True,
    python_requires=">=3.8, <4",
    # python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*',
    install_requires=[],
    extras_require={
        "dev": ["setuptools", "setuptools-scm", "wheel", "twine", "check-manifest"],  # python -m pip install -e .[dev]
        "test": ["pytest", "pytest-cov", "coverage"],  # python -m pip install -e .[test]
        "lint": ["mypy"],  # python -m pip install -e .[lint]
        "fmt": ["ruff"],  # python -m pip install -e .[fmt]
        "docs": ["mkdocs"],  # python -m pip install -e .[docs]
        "all": [
            "setuptools",
            "setuptools-scm",
            "wheel",
            "twine",
            "check-manifest",
            "pytest",
            "pytest-cov",
            "coverage",
            "ruff",
            "mypy",
            "mkdocs",
        ],
    },
    entry_points={
        "console_scripts": [
            f"{PACKAGE_NAME}={PACKAGE_NAME}:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/{AUTHOR}/{PROJECT_NAME}/issues",
        "Source": "https://github.com/{AUTHOR}/{PROJECT_NAME}/",
    },
)
