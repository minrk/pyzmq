#!/usr/bin/env bash
set -ex

if [[ $TRAVIS_OS_NAME == osx ]]; then
  rm -rf "$TEST_ENV"
  brew install $PYTHON
  $PYTHON -m pip install virtualenv
  $PYTHON -m virtualenv "$TEST_ENV"
else
  sudo add-apt-repository -y ppa:anton+/dnscrypt
  sudo apt-get update
fi

pip install --upgrade setuptools pip

if [[ $ZMQ != bundled ]]; then
  if [[ $TRAVIS_OS_NAME == osx ]]; then
    brew install zeromq
  else
    sudo apt-get install -y -qq libzmq3-dev libsodium-dev
  fi
fi

if [[ $TRAVIS_PYTHON_VERSION != pypy* ]]; then
  pip install -q cython --install-option="--no-cython-compile"
fi

if [[ ! -z "$ZMQ" && $ZMQ != bundled ]]; then
  wget https://github.com/zeromq/$ZMQ/archive/master.zip -O libzmq.zip
  unzip libzmq.zip
  pushd "$ZMQ-master"
  ./autogen.sh
  ./configure
  make -j
  sudo make install
  sudo ldconfig
  popd
  export ZMQ=/usr/local
fi

pip install -r test-requirements.txt
if [[ "$NOTORNADO" == "1" ]]; then
  pip uninstall -yq tornado
fi

