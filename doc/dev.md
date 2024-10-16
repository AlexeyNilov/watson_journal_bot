# Development guide

## Test

```
source .venv/bin/activate
pip install -r requirements_dev.txt
pre-commit install
python -m coverage run -m pytest test/test_*.py -W ignore::DeprecationWarning
python -m coverage html -i --omit=conf/settings.py
mypy .
```
