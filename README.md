# tm-grammar

Python bindings for tmGrammar.

## Install instructions

It is recommended to install the utm Python bindings in a virtual environment
which makes it also possible to use multiple versions in parallel.

### Python 3.11

```bash
pip install https://github.com/cms-l1-globaltrigger/tm-grammar/releases/download/0.11.2/tm_grammar-0.11.2-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```

### Python 3.10

```bash
pip install https://github.com/cms-l1-globaltrigger/tm-grammar/releases/download/0.11.2/tm_grammar-0.11.2-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```

### Python 3.9

```bash
pip install https://github.com/cms-l1-globaltrigger/tm-grammar/releases/download/0.11.2/tm_grammar-0.11.2-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```

### Python 3.8

```bash
pip install https://github.com/cms-l1-globaltrigger/tm-grammar/releases/download/0.11.2/tm_grammar-0.11.2-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```

### Python 3.7

```bash
pip install https://github.com/cms-l1-globaltrigger/tm-grammar/releases/download/0.11.2/tm_grammar-0.11.2-cp37-cp37m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```

### Python 3.6

```bash
pip install https://github.com/cms-l1-globaltrigger/tm-grammar/releases/download/0.11.2/tm_grammar-0.11.2-cp36-cp36m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```

## Build instructions

**Note:** building the Python bindings from scratch is only recommended for
development. To create portable Python bindings use the
[tm-manylinux](https://github.com/cms-l1-globaltrigger/tm-manylinux)
Docker image.

Make sure to install all required build dependecies.

On ubuntu based distributions install
```bash
sudo apt-get install git build-essential libboost-dev libboost-system-dev libboost-filesystem-dev libxerces-c-dev python3-dev python3-venv swig
```

Check out and build all utm libraries.

**Important:** compile using the `-DSWIG` flag, see below.

```bash
git clone https://gitlab.cern.ch/cms-l1t-utm/utm.git
cd utm
git checkout utm_0.11.2
./configure # create makefiles
make all CPPFLAGS='-DNDEBUG -DSWIG'  # compile with -DSWIG
. ./env.sh  # source paths
cd ..
```

Next build the Python bindings and install the resulting wheel. It is
recommended to execute this step in a virtual environment.

```bash
git clone https://github.com/cms-l1-globaltrigger/tm-grammar.git
cd tm-grammar
git checkout 0.11.2
python3 -m venv env
. env/bin/activate
pip install --upgrade pip
pip install .
```
