.. highlight:: shell

============
Installation
============


Stable release
--------------

First of all, you want to make sure you have **python** and **pipx** installed on your device. It would also be preferable to have **pyenv** installed, in case the system interpreter is upgraded, as an example.

python
^^^^^^

Here are a few Python installation guides (it's quick):

* `Install Python on Windows <https://docs.python-guide.org/starting/install3/win/#install3-windows>`_
* `Install Python on MacOS <https://docs.python-guide.org/starting/install3/osx/#install3-osx>`_
* `Install Python on Linux <https://docs.python-guide.org/starting/install3/linux/#install3-linux>`_

pipx & (optional) pyenv
^^^^^^^^^^^^^^^^^^^^^^^

pipx
""""

On macOS:

.. code-block:: bash

    brew install pipx
    pipx ensurepath

Otherwise, install via pip (requires pip 19.0 or later):

.. code-block:: bash

    python3 -m pip install --user pipx
    python3 -m pipx ensurepath

pyenv
"""""

The pyenv install is optional, mostly because the installation may be a hassle for non-devs. Non-devs should simply make sure to use a Python version larger than or equal to :code:`3.11.0`.

On MacOS:

.. code-block:: bash

    brew update
    brew install pyenv

You should also `setup your shell environment.`_

On Linux:

.. code-block:: bash

    curl https://pyenv.run | bash

*Pyenv does not support Windows unless on WSL, which is Linux!*

.. _`setup your shell environment.`: https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv

cryptoolzf
^^^^^^^^

The best way to install cryptoolzf after this, for regular users, is as follows:

.. code-block:: bash

    pipx install --suffix <cryptoolzf version> cryptoolzf


We want to essentially be absolutely sure that our local installation is always able to decrypt some data, so instead of updating cryptoolzf we should simply always have a fresh install with a new suffix. As such, we never upgrade once downloaded versions.

This does not mean that the library won't be backwards compatible, but this is simply the safest option for regular users.

If using pyenv, you might also want to install a fixed version and then, in bash, as an example:

.. code-block:: bash 

    pyenv shell <python version installed>
    pipx install --suffix <python version installed> cryptoolzf
    pyenv shell $(pyenv global) # or just exit and open a new shell

Instead when using cryptoolzf as a library the regular:

.. code-block:: bash

    pip install cryptoolzf

Is used as usual.

From sources
------------

The sources for cryptoolzf can be downloaded from the `Github repo`_.

You can clone the public repository:

.. code-block:: bash

    git clone git://github.com/mtugan/cryptoolzf

.. _Github repo: https://github.com/mtugan/cryptoolzf
