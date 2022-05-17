Lmod
====

* Statically linked against (i.e squashed dependencies)
    * lfs
    * lpeg
    * luaposix

* Built using alpine linux 
    * statically linked against musl (no dependency on any system libraries)

* Cross compiled
    * x86_64
    * ppc64le
    * riscv64
    * aarch64


Dynamic loading of dependencies
-------------------------------

.. code-block::

    1. DT_RPATH unless DT_RUNPATH
    2. LD_LIBRARY_PATH
    3. DT_RUNPATH 
    4. /etc/ld.so.cache, unless -z nodeflib
    5. /lib, /usr/lib unless -z nodeflib
