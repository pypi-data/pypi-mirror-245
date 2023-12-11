# pypi_templates(setup.py)
python package template for publish to pypi

## Windows
```powershell

python -m venv .venv
& .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip build wheel twine setuptools setuptools-scm
python -m pip list

$package_name="pypi_templates"
echo "" > setup.py
python -m pip freeze > requirements.txt
mkdir src/$package_name
echo "" > src/$package_name/__init__.py
echo "" > src/$package_name/__version__.py
echo "" > src/$package_name/__main__.py
echo "" > src/$package_name/main.py
mkdir tests
echo "" > tests/__init__.py
echo "" > tests/test_main.py


python -m pip install -e .[dev]
python -m pip install -e .[test]
python -m pip install -e .[lint]
python -m pip install -e .[fmt]
python -m pip install -e .[docs]
python -m pip install -e .[all]

```

## Unix
```bash

python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --upgrade pip build wheel twine setuptools setuptools-scm
python3 -m pip list

package_name="pypi_templates"
echo "" > setup.py
python3 -m pip freeze > requirements.txt
mkdir -p src/$package_name
echo "" > src/$package_name/__init__.py
echo "" > src/$package_name/__version__.py
echo "" > src/$package_name/__main__.py
echo "" > src/$package_name/main.py
mkdir -p tests
echo "" > tests/__init__.py
echo "" > tests/test_main.py



python3 -m pip install -e .[dev]
python3 -m pip install -e .[test]
python3 -m pip install -e .[lint]
python3 -m pip install -e .[fmt]
python3 -m pip install -e .[docs]
python -m pip install -e .[all]

```
