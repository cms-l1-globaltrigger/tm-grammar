# tmGrammar

Python bindings for tmGrammar.

## Install instructions

It is recommended to install the utm python bindings in a virtual environment
which makes it possible to run multiple versions of utm in parallel.

### Python 3.7

```bash
pip install https://github.com/cms-l1-globaltrigger/tm-grammar/releases/download/0.7.3/tm_grammar-0.7.3-cp37-cp37m-manylinux1_x86_64.whl
```

### Python 3.6

```bash
pip install https://github.com/cms-l1-globaltrigger/tm-grammar/releases/download/0.7.3/tm_grammar-0.7.3-cp36-cp36m-manylinux1_x86_64.whl
```

### Python 3.5

```bash
pip install https://github.com/cms-l1-globaltrigger/tm-grammar/releases/download/0.7.3/tm_grammar-0.7.3-cp35-cp35m-manylinux1_x86_64.whl
```

# Build instructions

First check out and build utm libraries.

```bash
git clone https://gitlab.cern.ch/cms-l1t-utm/utm.git
cd utm
git checkout utm_0.7.3
make
. setup.sh  # source paths
cd ..
```

Build python bindings and pack into a wheel. It is recommended to do this in a
virtual environment.

```bash
git clone https://github.com/cms-l1-globaltrigger/tm-grammar.git
cd tm-grammar
python -m venv env
. env/bin/activate
pip --upgrade pip wheel
python setup.py bdist_wheel
```

Use `manylinux1` and `audithwheel` to build universal binaries.

