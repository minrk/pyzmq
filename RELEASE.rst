How to release PyZMQ
====================

Currently, we are using the following steps to release PyZMQ:

* Check the version number in ``version.pyx``.
* Remove old ``MANIFEST`` and ``egg-info`` files and ``dist`` and ``build`` directories.
* Check ``MANIFEST.in``.
* Register the release with pypi::

    python setup.py register

* Build source distributions and upload::

    python setup.py sdist --formats=zip,gztar upload

* Branch the release (do *not* push the branch)::

    git checkout -b 2.1.9 master

* commit the changed ``version.pyx`` to the branch::

    git add zmq/core/version.pyx && git commit -m "bump version to 2.1.9"

* Tag the release::

    git tag -a -m "Tagging release 2.1.9" v2.1.9
    git push origin --tags

* Make sure ``AUTHORS`` has an updated list of contributors.
* Update ØMQ Wiki page with new download URLs: http://www.zeromq.org/bindings:python
* Announce on list.
