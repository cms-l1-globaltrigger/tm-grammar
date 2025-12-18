import argparse
import os
import subprocess
from urllib.request import urlretrieve

DEFAULT_UTM_VERSION = "0.14.0"
DEFAULT_BOOST_VERSION = "1.90.0"
DEFAULT_XERCES_C_VERSION = "3.3.0"
DEFAULT_BUILD_DIR = os.path.join(os.getcwd(), "build")
DEFAULT_INSTALL_PREFIX = os.path.join(os.getcwd(), "dist")


def run(*args):
    subprocess.run(args, check=True)


class Builder:
    def __init__(self, version, build_dir, install_prefix):
        self.version = version
        self.build_dir = os.path.realpath(build_dir)
        self.install_prefix = os.path.realpath(install_prefix)
        self.cpu_count = os.cpu_count()

    def fetch(self):
        ...

    def build(self):
        ...


class BoostBuilder(Builder):
    def fetch(self):
        os.chdir(self.build_dir)
        url = f"https://github.com/boostorg/boost/releases/download/boost-{self.version}/boost-{self.version}.tar.xz"
        urlretrieve(url, f"boost-{self.version}.tar.xz")
        run("tar", "xf", f"boost-{self.version}.tar.xz", "-C", self.build_dir)

    def build(self):
        os.chdir(self.build_dir)
        os.chdir(f"boost-{self.version}")
        b2_options = [
            f"-j{self.cpu_count}",
            "--with-system",
            "--with-filesystem",
            "link=shared",
            "runtime-link=shared",
            "threading=multi",
            "variant=release",
        ]
        run("./bootstrap.sh")
        run("./b2", *b2_options, "install", f"--prefix={self.install_prefix}")


class XercesCBuilder(Builder):
    def fetch(self):
        os.chdir(self.build_dir)
        url = f"https://github.com/apache/xerces-c/archive/v{self.version}.tar.gz"
        urlretrieve(url, f"xerces-c-{self.version}.tar.gz")
        run("tar", "xf", f"xerces-c-{self.version}.tar.gz", "-C", self.build_dir)
        os.chdir(f"xerces-c-{self.version}")

    def build(self):
        os.chdir(self.build_dir)
        os.chdir(f"xerces-c-{self.version}")
        os.makedirs("build")
        os.chdir("build")
        cmake_options = [
            "-DCMAKE_BUILD_TYPE=Release",
            f"-DCMAKE_INSTALL_PREFIX={self.install_prefix}",
            "-DBUILD_SHARED_LIBS=ON",
            "-DCMAKE_INSTALL_LIBDIR=lib",
        ]
        make_options = [
            f"-j{self.cpu_count}",
        ]
        run("cmake", *cmake_options, "..")
        run("make", *make_options)
        run("make", "install")


class UtmBuilder(Builder):
    boost_prefix = None
    xerces_c_prefix = None

    def fetch(self):
        os.chdir(self.build_dir)
        url = f"https://gitlab.cern.ch/cms-l1t-utm/utm/-/archive/utm_{self.version}/utm-utm_{self.version}.tar.gz"
        urlretrieve(url, f"utm-utm_{self.version}.tar.gz")
        run("tar", "xzf", f"utm-utm_{self.version}.tar.gz", "-C", self.build_dir)
        os.chdir(f"utm-utm_{self.version}")

    def build(self):
        os.chdir(self.build_dir)
        os.chdir(f"utm-utm_{self.version}")
        run("./configure")
        make_options = [
            f"-j{self.cpu_count}",
            "CPPFLAGS='-DNDEBUG -DSWIG'",
        ]
        if self.boost_prefix:
            make_options.append(f"BOOST_BASE={self.boost_prefix}")
        if self.xerces_c_prefix:
            make_options.append(f"XERCES_C_BASE={self.xerces_c_prefix}")
        run("make", "all", *make_options)
        run("make", "install", f"PREFIX={self.install_prefix}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--utm-version", default=DEFAULT_UTM_VERSION)
    parser.add_argument("--with-boost", action="store_true")
    parser.add_argument("--boost-version", default=DEFAULT_BOOST_VERSION)
    parser.add_argument("--with-xerces-c", action="store_true")
    parser.add_argument("--xerces-c-version", default=DEFAULT_XERCES_C_VERSION)
    parser.add_argument("--build", default=DEFAULT_BUILD_DIR)
    parser.add_argument("--install-prefix", default=DEFAULT_INSTALL_PREFIX)
    return parser.parse_args()


def main():
    args = parse_args()

    # Setup

    if not os.path.exists(args.build):
        os.makedirs(args.build)

    if not os.path.exists(args.install_prefix):
        os.makedirs(args.install_prefix)

    boost_builder = BoostBuilder(
        version=args.boost_version,
        build_dir=args.build,
        install_prefix=args.install_prefix,
    )
    xerxes_c_builder = XercesCBuilder(
        version=args.xerces_c_version,
        build_dir=args.build,
        install_prefix=args.install_prefix,
    )
    utm_builder = UtmBuilder(
        version=args.utm_version,
        build_dir=args.build,
        install_prefix=args.install_prefix,
    )

    # Fetch

    if args.with_boost:
        boost_builder.fetch()
        utm_builder.boost_prefix=args.install_prefix

    if args.with_xerces_c:
        xerxes_c_builder.fetch()
        utm_builder.xerces_c_prefix=args.install_prefix

    utm_builder.fetch()

    # Build

    if args.with_boost:
        boost_builder.build()

    if args.with_xerces_c:
        xerxes_c_builder.build()

    utm_builder.build()


if __name__ == "__main__":
    main()
