NURBS-Python v5 Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

|DOI|_ |PYPI|_ |ANACONDA|_

.. note::

    These documentation pages are for v5 release of NURBS-Python (geomdl) library.
    Please see `NURBS-Python 4.x documentation <https://nurbs-python.readthedocs.io/en/4.x/index.html>`_ for the
    previous stable release.

Welcome to the **NURBS-Python (geomdl) v5.x** documentation! NURBS-Python is a pure Python, object-oriented B-Spline
and NURBS library. It is compatible with Python versions 2.7.x, 3.4.x and later. It supports rational and non-rational
parametric shapes; e.g. curves, surfaces and volumes.

NURBS-Python also provides a convenient and easy-to-use data structures for storing parametric shape descriptions.
These are documented under :ref:`modules`.

This documentation is organized into a couple sections:

* :ref:`introduction`
* :ref:`using`
* :ref:`modules`

.. _introduction:

.. toctree::
    :maxdepth: 2
    :caption: Introduction

    introduction
    citing
    q_a

.. _using:

.. toctree::
    :maxdepth: 2
    :caption: Using the Library

    install
    examples_repo
    cli_application
    load_save
    file_formats
    compatibility
    surface_generator
    visualization
    visualization_splitting
    visualization_export

.. _modules:

.. toctree::
    :maxdepth: 3
    :caption: Modules

    modules
    modules_visualization
    modules_experimental


NURBS-Python is developed by `Onur Rauf Bingol <https://github.com/orbingol>`_ and all the code released under the
`MIT License <https://github.com/orbingol/NURBS-Python/blob/master/LICENSE>`_.


.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.815010.svg
.. _DOI: https://doi.org/10.5281/zenodo.815010

.. |PYPI| image:: https://img.shields.io/pypi/v/geomdl.svg
.. _PYPI: https://pypi.org/project/geomdl/

.. |ANACONDA| image:: https://anaconda.org/orbingol/geomdl/badges/version.svg
.. _ANACONDA: https://anaconda.org/orbingol/geomdl
