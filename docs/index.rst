.. pyuvdata documentation master file, created by
   make_index.py on 2020-02-28

pyuvdata
========

.. image:: https://circleci.com/gh/RadioAstronomySoftwareGroup/pyuvdata.svg?style=svg
    :target: https://circleci.com/gh/RadioAstronomySoftwareGroup/pyuvdata

.. image:: https://github.com/RadioAstronomySoftwareGroup/pyuvdata/workflows/Run%20Tests/badge.svg?branch=master
    :target: https://github.com/RadioAstronomySoftwareGroup/pyuvdata/actions

.. image:: https://dev.azure.com/radioastronomysoftwaregroup/pyuvdata/_apis/build/status/RadioAstronomySoftwareGroup.pyuvdata?branchName=master
    :target: https://dev.azure.com/radioastronomysoftwaregroup/pyuvdata/_build/latest?definitionId=1&branchName=master

.. image:: https://codecov.io/gh/RadioAstronomySoftwareGroup/pyuvdata/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/RadioAstronomySoftwareGroup/pyuvdata

.. image:: http://joss.theoj.org/papers/10.21105/joss.00140/status.svg
  :target: https://doi.org/10.21105/joss.00140

pyuvdata defines a pythonic interface to interferometric data sets.
Currently pyuvdata supports reading and writing of miriad, uvfits, and
uvh5 files and reading of CASA measurement sets and FHD (`Fast
Holographic Deconvolution <https://github.com/EoRImaging/FHD>`__)
visibility save files.

Motivation
==========

The main goals are:

1. To provide a high quality, well documented path to convert between
   data formats
2. Support the direct use of datasets from python with minimal software
3. Provide precise data definition via both human readable code and high
   quality online documentation

Package Details
===============

pyuvdata has four major user classes:

-  UVData: supports interferometric data (visibilities) and associated
   metadata
-  UVCal: supports interferometric calibration solutions (antenna-based)
   and associated metadata (Note that this is a fairly new object,
   consider it to be a beta version)
-  UVBeam: supports primary beams (E-field or power) and associated
   metadata (Note that this is a fairly new object, consider it to be a
   beta version)
-  UVFlag: A class to handle the manipulation and combination of flags
   for data sets. Also can convert raw data quality metrics into flags
   using thresholding. (This object is very new and experimental.
   Consider it to be a beta version)

UVData File standard notes
--------------------------

-  miriad has been thoroughly tested with aipy-style miriad files and
   minimally tested with ATCA files
-  uvfits conforms to AIPS memo 117 (as of May 2015). It is tested
   against FHD, CASA, and AIPS. However AIPS is limited to <80 antennas
   and CASA uvfits import does not seem to support >255 antennas.
-  uvh5 is an HDF5-based file format defined by the HERA collaboration,
   details in the `uvh5 memo <https://github.com/RadioAstronomySoftwareGroup/pyuvdata/tree/master/docs/references/uvh5_memo.pdf>`__. Note
   that this is a somewhat new format, so it may evolve a bit but we
   will strive to make future versions backwards compatible with the
   current format. It is probably not compatible with other
   interferometric HDF5 files defined by other groups.
-  FHD (read-only support, tested against MWA and PAPER data)
-  CASA measurement sets (read-only support)

UVCal file formats
------------------

-  calfits: a new format defined in pyuvdata, details in the
   `calfits_memo <https://github.com/RadioAstronomySoftwareGroup/pyuvdata/tree/master/docs/references/calfits_memo.pdf>`__. Note that this
   format was recently defined and may change in coming versions, based
   on user needs. Consider it to be a beta version, but we will strive
   to make future versions backwards compatible with the current format.
-  FHD calibration files (read-only support)

UVBeam file formats
-------------------

-  regularly gridded fits for both E-field and power beams
-  non-standard HEALPix fits for both E-field and power beams (in an
   ImageHDU rather than a binary table to support frequency,
   polarization and E-field vector axes)
-  read support for CST beam text files, with a defined yaml file format
   for metadata, details here: `cst settings
   file <https://github.com/RadioAstronomySoftwareGroup/pyuvdata/tree/master/docs/cst_settings_yaml.rst>`__

Under Development
-----------------

-  UVCal: object and calfits file format (beta version)
-  UVBeam: object and beamfits file format (beta version)
-  UVFlag: object and HDF5 file format. (beta version)

Known Issues and Planned Improvements
-------------------------------------

-  UVData: phasing (and the accuracy on the uvw coordinates) is only
   known to be good to 2cm on a 3km baseline (this is limited by the
   accuracy of the test file, see the `phasing
   memo <https://github.com/RadioAstronomySoftwareGroup/pyuvdata/tree/master/docs/references/phasing.pdf>`__ for more details).
-  UVData: Multiple spectral windows or multiple sources are not
   currently supported
-  UVData: add support for writing CASA measurement sets
-  UVBeam: support phased-array antenna beams (e.g. MWA beams).
-  UVFlag: Adding requires a high level knowledge of individual objects.
   (see `issue
   #653 <https://github.com/RadioAstronomySoftwareGroup/pyuvdata/issues/653>`__)

For details see the `issue
log <https://github.com/RadioAstronomySoftwareGroup/pyuvdata/issues>`__.

Community Guidelines
--------------------

Contributions to this package to add new file formats or address any of
the issues in the `issue
log <https://github.com/RadioAstronomySoftwareGroup/pyuvdata/issues>`__
are very welcome, as are bug reports and feature requests. Please see
our `guide on contributing <https://github.com/RadioAstronomySoftwareGroup/pyuvdata/tree/master/.github/CONTRIBUTING.md>`__

Telescopes
==========

pyuvdata has been used with data from the following telescopes. If you
use it on data from a telescope we don’t have listed here please let us
know how it went via an issue! We would like to make pyuvdata generally
useful to the community for as many telescopes as possible.

-  MWA
-  HERA
-  PAPER
-  LWA
-  ALMA
-  VLA
-  ATCA

Versioning
==========

We use a ``generation.major.minor`` version number format. We use the
``generation`` number for very significant improvements or major
rewrites, the ``major`` number to indicate substantial package changes
(intended to be released every 3-4 months) and the ``minor`` number to
release smaller incremental updates (intended to be released
approximately monthly and which usually do not include breaking API
changes). We do our best to provide a significant period (usually 2
major generations) of deprecation warnings for all breaking changes to
the API. We track all changes in our
`changelog <https://github.com/RadioAstronomySoftwareGroup/pyuvdata/blob/master/CHANGELOG.md>`__.

Documentation
=============

A tutorial with example usage and developer API documentation is hosted
on `ReadTheDocs <https://pyuvdata.readthedocs.io>`__.

History
=======

pyuvdata was originally developed in the low frequency 21cm community to
support the development of and interchange of data between calibration
and foreground subtraction pipelines. Particular focus has been paid to
supporting drift and phased array modes.

Citation
========

Please cite pyuvdata by citing our JOSS paper:

Hazelton et al, (2017), pyuvdata: an interface for astronomical
interferometeric datasets in python, Journal of Open Source Software,
2(10), 140, doi:10.21105/joss.00140

`ADS Link <https://ui.adsabs.harvard.edu/abs/2017JOSS....2..140H>`__;
`Bibtex
entry <http://adsabs.harvard.edu/cgi-bin/nph-bib_query?bibcode=2017JOSS....2..140H&data_type=BIBTEX&db_key=GEN&nocookieset=1>`__

Installation
============

For simple installation, the latest stable version is available via
conda (preferred: ``conda install -c conda-forge pyuvdata``) or pip
(``pip install pyuvdata``).

There are some optional dependencies that are required for specific
functionality, which will not be installed automatically by conda or
pip. See `Dependencies <#dependencies>`__ for details on installing
optional dependencies.

Note that as of v2, ``pyuvdata`` is only supported on python 3.6+.

Optionally install the development version
------------------------------------------

Clone the repository using
``git clone https://github.com/RadioAstronomySoftwareGroup/pyuvdata.git``

Navigate into the pyuvdata directory and run ``pip install .`` (note
that ``python setup.py install`` does not work). Note that this will
attempt to automatically install any missing dependencies. If you use
anaconda or another package manager you might prefer to first install
the dependencies as described in `Dependencies <#dependencies>`__.

To install without dependencies, run ``pip install --no-deps``

To compile the binary extension modules such that you can successfully
run ``import pyuvdata`` from the top-level directory of your Git
checkout, run: ``python setup.py build_ext --inplace``

Dependencies
------------

Required:

-  numpy >= 1.15
-  scipy
-  astropy >= 3.2.3
-  h5py

Optional:

-  python-casacore (for working with CASA measurement sets)
-  astropy-healpix (for working with beams in HEALPix formats)
-  pyyaml (for working with settings files for CST beam files)

The numpy and astropy versions are important, so make sure these are up
to date.

We suggest using conda to install all the dependencies. If you want to
install python-casacore and astropy-healpix, you’ll need to add
conda-forge as a channel (``conda config --add channels conda-forge``).
Developers may wish to use the included ``environment.yaml`` file to
create a new environment that will contain all the optional dependencies
along with dependencies required for testing and development
(``conda env create -f environment.yml``).

If you do not want to use conda, the packages are also available on PyPI
(python-casacore may require more effort, see details for that package
below). You can install the optional dependencies via pip by specifying
an option when you install pyuvdata, as in
``pip install pyuvdata[healpix]`` which will install all the required
packages for using the HEALPix functionality in pyuvdata. The options
that can be passed in this way are: [casa, healpix, cst, all, test, doc,
dev]. The first three (``casa``, ``healpix``, ``cst``) enable various
specific functionality while ``all`` will install all optional
dependencies. The last three (``test``, ``doc``, ``dev``) may be useful
for developers of pyuvdata to install the packages needed for testing
(including coverage and linting) and documentation development; ``dev``
includes everything in ``test`` and ``doc``.

Installing python-casacore
~~~~~~~~~~~~~~~~~~~~~~~~~~

python-casacore requires the casacore c++ libraries. It can be installed
easily using conda (``python-casacore`` on conda-forge).

If you do not want to use conda, the casacore c++ libraries are
available for ubuntu through the `kern
suite <http://kernsuite.info/>`__. On OSX, casacore is available through
the `ska-sa brew tap <https://github.com/ska-sa/homebrew-tap>`__. The
python-casacore library (with manual install instructions) is available
at https://github.com/casacore/python-casacore

Tests
-----

Uses the ``pytest`` package to execute test suite. From the source
pyuvdata directory run ``pytest`` or ``python -m pytest``.

Testing of ``UVFlag`` module requires the ``pytest-cases`` plug-in.

API
===

The primary interface to data from python is via the UVData object. It
provides import functionality from all supported file formats (UVFITS,
Miriad, UVH5, FHD, CASA measurement sets) and export to UVFITS, Miriad,
and UVH5 formats and can be interacted with directly. Similarly, the
primary calibration, beam, and flag interfaces are via the UVCal,
UVBeam, and UVflag objects. The attributes of the UVData, UVCal, UVBeam,
and UVFlag objects are described in the uvdata_parameters,
uvcal_parameters, uvbeam_parameters and uvflag_parameters descriptions.

Further Documentation
====================================
.. toctree::
   :maxdepth: 1

   tutorial
   uvdata_parameters
   uvdata
   uvcal_parameters
   uvcal
   uvbeam_parameters
   uvbeam
   uvflag_parameters
   uvflag
   cst_settings_yaml
   utility_functions
   known_telescopes
   developer_docs
