[![Build Status](https://travis-ci.com/filwaitman/pytracetable.svg?branch=master)](https://travis-ci.com/filwaitman/pytracetable)

# pytracetable

Script debugging tool that aims to make a line-by-line debugging easier. Take a look:

```python
from pytracetable import tracetable

@tracetable()
def some_weird_calculation(a, b):
        c = 10 + a
        b *= 2
        c += b
        del b
        return a + c
```

Then, calling `some_weird_calculation(5, 10)` will give the output:

```
--------------------------------------------------
At some_weird_calculation, line 3
    [ADDED]    a: 5 (int)
    [ADDED]    b: 10 (int)

--------------------------------------------------
At some_weird_calculation, line 4
    [ADDED]    c: 15 (int)

--------------------------------------------------
At some_weird_calculation, line 5
    [CHANGED]  b: 10 (int) --> 20 (int)

--------------------------------------------------
At some_weird_calculation, line 6
    [CHANGED]  c: 15 (int) --> 35 (int)

--------------------------------------------------
At some_weird_calculation, line 7
    [REMOVED]  b
    [RETURNED] 40 (int)
```


## Development:

### Run linter:
```bash
pip install -r requirements_dev.txt
isort -rc .
tox -e lint
```

### Run tests via `tox`:
```bash
pip install -r requirements_dev.txt
tox
```

### Release a new major/minor/patch version:
```bash
pip install -r requirements_dev.txt
bump2version <PART>  # <PART> can be either 'patch' or 'minor' or 'major'
```

### Upload to PyPI:
```bash
pip install -r requirements_dev.txt
python setup.py sdist bdist_wheel
python -m twine upload dist/*
```

## Contributing:

Please [open issues](https://github.com/filwaitman/pytracetable/issues) if you see one, or [create a pull request](https://github.com/filwaitman/pytracetable/pulls) when possible.
In case of a pull request, please consider the following:
- Respect the line length (132 characters)
- Write automated tests
- Run `tox` locally so you can see if everything is green (including linter and other python versions)
