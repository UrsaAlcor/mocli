mocli
=====

Alcor command line utility

.. code-block:: bash

   pip install mocli


Dev/Personal Install
--------------------

Install Lmod
^^^^^^^^^^^^

.. code-block:: bash

   # Install Lmod to the given location
   alcor init /opt/alcor

   # Modify bash to automatically source alcor bash profiles
   alcor activate --auto

   # Reload environment
   exec bash

   # Show a list of available modules
   module spider


Install New Modules
^^^^^^^^^^^^^^^^^^^

.. literalinclude :: ../tests/integration/test_install_module.sh
   :language: bash
   :lines: 2-


Install Apt packages
^^^^^^^^^^^^^^^^^^^^

.. warning::

   This is not guaranteed to work.
   Package might hardcode library path or expect a specific system setup.


.. literalinclude :: ../tests/integration/test_install_apt.sh
   :language: bash
   :lines: 2-


Cluster Installation
--------------------

* The main installation is readonly
* Update /etc/profile so every user connecting to the cluster gets modules
* user can install their own package locally in their home

Enabling User modules
^^^^^^^^^^^^^^^^^^^^^
