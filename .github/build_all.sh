#!/bin/bash

set -e

: ${UTM_VERSION:=0.12.0}
: ${UTM_BASE:="$(pwd)/dist/utm"}

: ${BOOST_VERSION:=1.84.0}
: ${BOOST_BASE:="$(pwd)/dist/boost"}

: ${XERCES_C_VERSION:=3.2.5}
: ${XERCES_C_BASE:="$(pwd)/dist/xerces-c"}

: ${BUILD_DIR:="$(pwd)/build"}

mkdir -p $BUILD_DIR
cd $BUILD_DIR

curl -LO "https://github.com/boostorg/boost/releases/download/boost-${BOOST_VERSION}/boost-${BOOST_VERSION}.tar.xz"
tar xf "boost-${BOOST_VERSION}.tar.xz"
cd "boost-${BOOST_VERSION}"
./bootstrap.sh
./b2 -j4 --with-system --with-filesystem link=shared runtime-link=shared threading=multi variant=release install --prefix=${BOOST_BASE}

cd $BUILD_DIR

curl -OL https://dlcdn.apache.org/xerces/c/3/sources/xerces-c-${XERCES_C_VERSION}.tar.gz
tar xzf xerces-c-${XERCES_C_VERSION}.tar.gz
cd xerces-c-${XERCES_C_VERSION}
./configure --prefix=${XERCES_C_BASE}
make -j4
make install

cd $BUILD_DIR

curl -OL https://gitlab.cern.ch/cms-l1t-utm/utm/-/archive/utm_${UTM_VERSION}/utm-utm_${UTM_VERSION}.tar.gz
tar xzf utm-utm_${UTM_VERSION}.tar.gz
cd utm-utm_${UTM_VERSION}
./configure
make all -j4 CPPFLAGS='-DNDEBUG -DSWIG' BOOST_BASE=${BOOST_BASE} XERCES_C_BASE=${XERCES_C_BASE}
make install PREFIX=${UTM_BASE}
