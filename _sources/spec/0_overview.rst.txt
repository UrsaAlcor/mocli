Overview
========

.. code-block:: bash

   alcor init /opt/alcor

.. code-block:: bash

   /opt/alcor/
   ├── 8.5.23
   ├── lmod                            # Points to the current version of lmod
   ├── config                          # Default config of lmod
   ├── modules
   |   ├── <arch>/<package>/<version>/
   |   ├── aarch64/lua/v5.4.3.lua
   |   ├── ppc64le/lua/v5.4.3.lua
   |   ├── riscv64/lua/v5.4.3.lua
   |   └── x86_64/lua/v5.4.3.lua
   └── dist/<arch>/<package>/<version>
       ├── aarch64/lua/bin/lua
       ├── ppc64le/lua/bin/lua
       ├── riscv64/lua/bin/lua
       └── x86_64/lua/bin/lua


