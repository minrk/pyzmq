#!/usr/bin/env bash
# script to install libzmq/libsodium for use in wheels
set -ex
LIBSODIUM_VERSION=$(python buildutils/bundle.py libsodium)
LIBZMQ_VERSION=$(python buildutils/bundle.py)

if [[ "$(uname)" == "Darwin" ]]; then
    ARCHS="x86_64"
    case "${CIBW_ARCHS_MACOS:-auto}" in
        "universal2")
            ARCHS="x86_64 arm64"
            ;;
        "arm64")
            ARCHS="arm64"
            ;;
        "x86_64")
            ARCHS="x86_64"
            ;;
        "auto")
            ;;
        *)
            echo "Unexpected arch: ${CIBW_ARCHS_MACOS}"
            exit 1
            ;;
    esac
    echo "building libzmq for mac ${ARCHS}"
    for arch in ${ARCHS}; do
        export CFLAGS="-arch ${arch} ${CFLAGS:-}"
        export CXXFLAGS="-arch ${arch} ${CXXFLAGS:-}"
        export LDFLAGS="-arch ${arch} ${LDFLAGS:-}"
    done
fi

PREFIX="${PREFIX:-/usr/local}"

curl -L -O "https://download.libsodium.org/libsodium/releases/libsodium-${LIBSODIUM_VERSION}.tar.gz"

curl -L -O "https://github.com/zeromq/libzmq/releases/download/v${LIBZMQ_VERSION}/zeromq-${LIBZMQ_VERSION}.tar.gz"

tar -xzf libsodium-${LIBSODIUM_VERSION}.tar.gz
cd libsodium-*/
./configure --prefix="$PREFIX"
make -j4
make install

cd ..

which ldconfig && ldconfig || true

tar -xzf zeromq-${LIBZMQ_VERSION}.tar.gz
cd zeromq-${LIBZMQ_VERSION}
# avoid error on warning
export CXXFLAGS="-Wno-error ${CXXFLAGS:-}"

./configure --prefix="$PREFIX" --disable-perf --without-docs --enable-curve --with-libsodium --disable-libsodium_randombytes_close
make -j4
make install

which ldconfig && ldconfig || true
