import glob
import re
import shutil
import subprocess
import os

from setuptools import setup, Extension
import setuptools.command.build_py

UTM_VERSION = '0.9.0'
PACKAGE_NAME = 'tmGrammar'
PACKAGE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), PACKAGE_NAME))

UTM_ROOT = os.environ.get('UTM_ROOT')
if not UTM_ROOT:
    raise RuntimeError("UTM_ROOT not defined")

def load_version(f):
    """Load version from `version.h` file."""
    content = f.read()
    versions = []
    for name in ('MAJOR', 'MINOR', 'PATCH'):
        version = re.findall(r'#define\s+{}_VERSION_{}\s+(\d+)'.format(PACKAGE_NAME, name), content)[0]
        versions.append(version)
    return '.'.join(versions)

with open(os.path.join(UTM_ROOT, PACKAGE_NAME, 'include', 'utm', PACKAGE_NAME, 'version.h')) as f:
    assert UTM_VERSION == load_version(f)

class BuildPyCommand(setuptools.command.build_py.build_py):
    """Custom build command."""

    def create_modules(self):
        cwd = os.getcwd()
        # inside package
        os.chdir(PACKAGE_DIR)
        # run SWIG to (re)create bindings module
        subprocess.check_call(['swig', '-c++', '-python', '-outcurrentdir', '-I{}'.format(os.path.join(UTM_ROOT, PACKAGE_NAME, 'include', 'utm')), '{}.i'.format(PACKAGE_NAME)])
        # (re)create version module
        with open('version.py', 'w') as f:
            f.write("__version__ = '{}'".format(UTM_VERSION))
            f.write(os.linesep)
        os.chdir(cwd)

    def run(self):
        self.create_modules()
        # run actual build command
        setuptools.command.build_py.build_py.run(self)

tmGrammar_ext = Extension(
    name='_tmGrammar',
    define_macros=[('SWIG', '1'),],
    sources=[
        os.path.join(PACKAGE_DIR, 'tmGrammar_wrap.cxx')
    ],
    include_dirs=[
        os.path.join(UTM_ROOT, 'tmUtil', 'include', 'utm'),
        os.path.join(UTM_ROOT, PACKAGE_NAME, 'include', 'utm')
    ],
    library_dirs=[
        PACKAGE_DIR,
        os.path.join(UTM_ROOT, 'tmUtil'),
        os.path.join(UTM_ROOT, PACKAGE_NAME)
    ],
    libraries=['tmutil', 'tmgrammar'],
    extra_compile_args=['-std=c++11']
)

setup(
    name='tm-grammar',
    version=UTM_VERSION,
    author="Bernhard Arnold",
    author_email="bernhard.arnold@cern.ch",
    description="""Python bindings for tmGrammar""",
    ext_modules=[tmGrammar_ext],
    cmdclass={
        'build_py': BuildPyCommand,
    },
    packages=[PACKAGE_NAME],
    package_data={
        PACKAGE_NAME: [
            '*.i',
        ]
    },
    license="GPLv3"
)
