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

.. literalinclude :: tests/integration/test_install_module.sh
   :language: bash


Install Apt packages
^^^^^^^^^^^^^^^^^^^^

.. warning::

   This is not guaranteed to work.
   Package might hardcode library path or expect a specific system setup.


.. code-block::

   alcor aptinstall libsdl2-dev

   module load libsdl2-dev

   tee sdl2_main.c << END
   #include "SDL2/SDL.h"

   int main(int argc, const char* argv[]){
      return 0;
   }
   END

   gcc sdl2_main.c -o sdl2_main -lSDL2


Cluster Installation
--------------------

* The main installation is readonly
* Update /etc/profile so every user connecting to the cluster gets modules
* user can install their own package locally in their home

Enabling User modules
~~~~~~~~~~~~~~~~~~~~~
