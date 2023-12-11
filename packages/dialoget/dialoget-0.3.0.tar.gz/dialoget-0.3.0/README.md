# dialoget [py.dialoget.com](https://py.dialoget.com/)


[![PyPI - Version](https://img.shields.io/pypi/v/dialoget.svg)](https://pypi.org/project/dialoget)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dialoget.svg)](https://pypi.org/project/dialoget)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install dialoget
```

## License

`dialoget` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Version

```bash
hatch version
```


### Publish
After the build completes successfully, upload the new distribution files to the Python Package Index (PyPI).
Upload your package to PyPI using `twine`
   ```shell
   twine upload dist/*
   ```

## CONTRIBUTION

[Introduction - Hatch](https://hatch.pypa.io/latest/intro/)

```bash
hatch new dialoget
hatch version minor
python -m build
```


```
dialoget
├── src
│   └── dialoget
│       ├── __about__.py
│       └── __init__.py
├── tests
│   └── __init__.py
├── LICENSE.txt
├── README.md
└── pyproject.toml
```