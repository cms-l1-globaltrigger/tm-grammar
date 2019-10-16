# tm-grammar

Python bindings for tmGrammar.

## Install instructions

It is recommended to install the utm Python bindings in a virtual environment
which makes it also possible to run multiple versions of utm in parallel.

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

## Build instructions

**Note:** building the Python bindings from scratch is only recommended for 
development.

First check out and build all utm libraries. 

**Important:** compile using the `-DSWIG` flag, see below.

```bash
git clone https://gitlab.cern.ch/cms-l1t-utm/utm.git
cd utm
git checkout utm_0.7.3
make all CPPFLAGS='-DNDEBUG -DSWIG'  # compile with -DSWIG
. setup.sh  # source paths
cd ..
```

Next build the Python bindings and pack them into a wheel.

**Note:** it is recommended to execute this in a virtual environment.

```bash
git clone https://github.com/cms-l1-globaltrigger/tm-grammar.git
cd tm-grammar
git checkout 0.7.3
python3 -m venv env
. env/bin/activate
pip install --upgrade pip wheel
python setup.py bdist_wheel
```

To create universal Python bindings use a `manylinux1` docker image and `audithwheel` to integrate dependent libraries.
