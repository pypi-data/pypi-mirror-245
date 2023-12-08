# `sphinx-pybtex-etal-style`

[![PyPI package](https://badge.fury.io/py/sphinx-pybtex-etal-style.svg)](https://pypi.org/project/sphinx-pybtex-etal-style)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/sphinx-pybtex-etal-style)](https://pypi.org/project/sphinx-pybtex-etal-style)
[![BSD 3-Clause license](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Open in Visual Studio Code](https://img.shields.io/badge/vscode-open-blue?logo=visualstudiocode)](https://open.vscode.dev/ComPWA/sphinx-pybtex-etal-style)
[![CI status](https://github.com/ComPWA/sphinx-pybtex-etal-style/workflows/CI/badge.svg)](https://github.com/ComPWA/sphinx-pybtex-etal-style/actions?query=branch%3Amain+workflow%3ACI)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy.readthedocs.io)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/ComPWA/sphinx-pybtex-etal-style/main.svg)](https://results.pre-commit.ci/latest/github/ComPWA/sphinx-pybtex-etal-style/main)
[![Spelling checked](https://img.shields.io/badge/cspell-checked-brightgreen.svg)](https://github.com/streetsidesoftware/cspell/tree/master/packages/cspell)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

This Sphinx extension defines a new bibliography style for the [`sphinxcontrib-bibtex`](https://sphinxcontrib-bibtex.rtfd.io) extension. Install through [PyPI](https://pypi.org) with `pip`:

```bash
pip install sphinx-pybtex-etal-style
```

Next, in your [Sphinx configuration file](https://www.sphinx-doc.org/en/master/usage/configuration.html) (`conf.py`), add `"sphinx_pybtex_etal_style"` to your `extensions`:

```python
extensions = [
    "sphinx_pybtex_etal_style",
]
```

and set your [default bibliography style](https://sphinxcontrib-bibtex.readthedocs.io/en/stable/usage.html#bibliography-style) to `"unsrt_et_al"`:

```python
bibtex_default_style = "unsrt_et_al"
```

Alternatively, you can use the style for one bibliography only by specifying it in the [`.. bibliography::` directive](https://sphinxcontrib-bibtex.readthedocs.io/en/stable/usage.html#directive-bibliography):

```rst
.. bibliography:: /references.bib
  :style: unsrt_et_al
```

Book entries that have an ISBN get a link to the book entry on [bookfinder.com](https://bookfinder.com/search). If you want to use [isbnsearch.org](https://isbnsearch.org) instead, add the following to your `conf.py`:

```python
unsrt_etal_isbn_resolver = "isbnsearch"
```
