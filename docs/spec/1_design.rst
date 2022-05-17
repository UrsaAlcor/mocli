Design
======

Goals
-----

* Builds software tailored for the compute cluster

* [Secondary goal] Reduce friction in a hyper-heterogeneous environment 
   * (CPU) Intel vs AMD  (intel mkl vs BLIS)
   * (CPU Arch) x64 vs Power9 vs ARM
   * (GPU) NVIDIA vs AMD


.. note::

    To help multi-arch support we cannot reference the compiler directly (gcc, clang) 
    because systems could have different defaults, 
    
    IIRC: clang has automatic x86 SIMD instruction conversion to power9 equivalent


Challenges
----------

#. Manage many dependencies for huge software (Pytorch & Tensorflow)

#. Replace dependencies with custom builds tailored for a compute cluster
   #. Modify builds configuration (not always simple, often painful)

#. Manage dependencies that might be incompatible and or have different versions

#. Manage different build system for each dependencies

#. Offer a simple way for users to use the custom binaries


Solutions
---------

* CVMFS for storing built binaries

* Lmod 
   * Manages built packages and enabling users to loading on their system

