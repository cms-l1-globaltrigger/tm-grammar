#!/bin/bash
# usage: build_all.sh [--with-boost] [--with-xerces-c]

set -eo pipefail

: ${UTM_VERSION:=0.12.0}
: ${UTM_BASE:="$(pwd)/dist/utm"}
: ${UTM_FLAGS:=""}

: ${BOOST_VERSION:=1.84.0}
: ${BOOST_BASE:="$(pwd)/dist/boost"}

: ${XERCES_C_VERSION:=3.2.5}
: ${XERCES_C_BASE:="$(pwd)/dist/xerces-c"}

: ${BUILD_UTM:=1}
: ${BUILD_DIR:="$(pwd)/build"}
: ${MAKE_ARGS:=""}

for arg in "$@"
do
  if [ "$arg" = "--with-boost" ]; then
    BUILD_BOOST=1
  elif [ "$arg" = "--with-xerces-c" ]; then
    BUILD_XERCES_C=1
  elif [ "$arg" = "--help" ]; then
    echo "usage: $0 [--with-boost] [--with-xerces-c] [--help]"
    exit 0
  else
    echo "invalid argument: $arg"
    exit 1
done

mkdir -p $BUILD_DIR

if [ ! -z "${BUILD_BOOST}" ];
then
  cd $BUILD_DIR
  curl -LO "https://github.com/boostorg/boost/releases/download/boost-${BOOST_VERSION}/boost-${BOOST_VERSION}.tar.xz"
  tar xf "boost-${BOOST_VERSION}.tar.xz"
  cd "boost-${BOOST_VERSION}"
  ./bootstrap.sh
  ./b2 ${MAKE_ARGS} --with-system --with-filesystem link=shared runtime-link=shared threading=multi variant=release install --prefix=${BOOST_BASE}
  UTM_FLAGS+=" BOOST_BASE=${BOOST_BASE}"
fi

if [ ! -z "${BUILD_XERCES_C}" ];
then
  cd $BUILD_DIR
  curl -OL https://dlcdn.apache.org/xerces/c/3/sources/xerces-c-${XERCES_C_VERSION}.tar.gz
  tar xzf xerces-c-${XERCES_C_VERSION}.tar.gz
  cd xerces-c-${XERCES_C_VERSION}
  ./configure --prefix=${XERCES_C_BASE}
  make ${MAKE_ARGS}
  make install
  UTM_FLAGS+=" XERCES_C_BASE=${XERCES_C_BASE}"
fi

if [ ! -z "${BUILD_UTM}" ];
then
  cd $BUILD_DIR
  curl -OL https://gitlab.cern.ch/cms-l1t-utm/utm/-/archive/utm_${UTM_VERSION}/utm-utm_${UTM_VERSION}.tar.gz
  tar xzf utm-utm_${UTM_VERSION}.tar.gz
  cd utm-utm_${UTM_VERSION}
  ./configure
  make all ${MAKE_ARGS} CPPFLAGS='-DNDEBUG -DSWIG' ${UTM_FLAGS}
  make install PREFIX=${UTM_BASE}
fi
