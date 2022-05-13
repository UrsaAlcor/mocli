mocli
=====

Alcor command line utility

.. code-block:: bash

   pip install mocli


Dev/Personal Install
--------------------

Install Lmod
^^^^^^^^^^^^

.. code-block::

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

.. code-block::

   alcor install lz4

   module load lz4


Install Apt packages
^^^^^^^^^^^^^^^^^^^^

.. warning::

   This is not guaranteed to work.
   Package might hardcode library path or expect a specific system setup.


.. code-block::

   aclor aptinstall libsdl2-dev

   module load sdl2


Cluster Installation
--------------------

