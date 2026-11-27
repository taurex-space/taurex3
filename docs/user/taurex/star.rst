.. _userstar:

===============
``[Star]``
===============

This header describes the parent star of the exo-planet.
The ``star_type`` informs the type of spectral emission density (SED) used in the emission and direct image forward model.
The ``star_type`` available are:

    - ``blackbody``
        - Star with a blackbody SED
        - Class :class:`~taurex.data.stellar.star.BlackbodyStar`
    - ``phoenix4all``
        - Uses the ``phoenix4all`` library for PHOENIX spectra with auto-download
        - Class ``phoenix4all.taurex.Phoenix4AllStar``
    - ``custom``
        - User-provided star model. See :ref:`customtypes`

-------------------------------------

Blackbody
=========
``star_type = blackbody``

Star is considered a blackbody.

--------
Keywords
--------

+------------------+--------------+----------------------------+---------+
| Variable         | Type         | Description                | Default |
+------------------+--------------+----------------------------+---------+
| ``temperature``  | :obj:`float` | Effective temperature in K | 5000    |
+------------------+--------------+----------------------------+---------+
| ``radius``       | :obj:`float` | Radius in solar radius     | 1.0     |
+------------------+--------------+----------------------------+---------+
| ``mass``         | :obj:`float` | Mass in solar mass         | 1.0     |
+------------------+--------------+----------------------------+---------+
| ``distance``     | :obj:`float` | Distance from Earth in pc  | 1.0     |
+------------------+--------------+----------------------------+---------+
| ``metallicity``  | :obj:`float` | Metallicity in solar units | 1.0     |
+------------------+--------------+----------------------------+---------+
| ``magnitudeK``   | :obj:`float` | Magnitude in K-band        | 10.0    |
+------------------+--------------+----------------------------+---------+

The physical inputs ``temperature``, ``radius``, ``mass`` and ``distance``
also accept :class:`astropy.units.Quantity`. Unitless values retain the units
listed above. ``metallicity`` accepts a dimensionless Quantity.

--------
Examples
--------

A Sun like star as a black body::

    [Star]
    star_type = blackbody
    radius = 1.0
    temperature = 5800

-----------------------------------

Phoenix4All
============
``star_type = phoenix4all``

Stellar emission spectrum is obtained from the ``phoenix4all`` library, which
automatically downloads (or loads from cache) high-resolution PHOENIX stellar
atmosphere spectra from multiple back-end sources.

Phoenix4All is fully integrated into TauREx 3: the ``phoenix4all`` package is a
required dependency and its ``phoenix4all.taurex.Phoenix4AllStar`` class is
loaded automatically as a plugin. No separate plugin installation or explicit
import is needed to use ``star_type = phoenix4all``.

The ``phoenix4all`` package supports several sources:

    - ``"svo"`` — Spanish Virtual Observatory (default)
    - ``"synphot"`` — STScI Synphot
    - ``"hiresfits"`` — Göttingen HiResFITS

By default a black-body (Planck) spectrum is returned when the requested
parameters fall outside the model grid.

--------
Keywords
--------

+------------------------+--------------+----------------------------------------------+------------------+
| Variable               | Type         | Description                                  | Default          |
+------------------------+--------------+----------------------------------------------+------------------+
| ``temperature``        | :obj:`float` | Effective temperature in K                   | 5000             |
+------------------------+--------------+----------------------------------------------+------------------+
| ``radius``             | :obj:`float` | Radius in solar radius                       | 1.0              |
+------------------------+--------------+----------------------------------------------+------------------+
| ``mass``               | :obj:`float` | Mass in solar mass                           | 1.0              |
+------------------------+--------------+----------------------------------------------+------------------+
| ``distance``           | :obj:`float` | Distance from Earth in pc                    | 1.0              |
+------------------------+--------------+----------------------------------------------+------------------+
| ``metallicity``        | :obj:`float` | Metallicity [Fe/H] in solar units            | 1.0              |
+------------------------+--------------+----------------------------------------------+------------------+
| ``magnitudeK``         | :obj:`float` | Magnitude in K-band                          | 10.0             |
+------------------------+--------------+----------------------------------------------+------------------+
| ``alpha``              | :obj:`float` | Alpha-element enhancement [alpha/Fe]         | 0.0              |
+------------------------+--------------+----------------------------------------------+------------------+
| ``source``             | :obj:`str`   | Phoenix data source (``svo``, ``synphot``,   | ``"svo"``       |
|                        |              | ``hiresfits``)                               |                  |
+------------------------+--------------+----------------------------------------------+------------------+
| ``interpolation_mode`` | :obj:`str`   | Interpolation mode (``linear`` or            | ``"linear"``    |
|                        |              | ``nearest``)                                 |                  |
+------------------------+--------------+----------------------------------------------+------------------+
| ``use_planck``         | :obj:`bool`  | Fall back to black-body when out of grid     | ``True``         |
+------------------------+--------------+----------------------------------------------+------------------+
| ``bounds_error``       | :obj:`bool`  | Raise error when outside model grid          | ``False``        |
+------------------------+--------------+----------------------------------------------+------------------+
| ``path``               | :obj:`str`   | Local path to pre-downloaded model files     | ``None``         |
+------------------------+--------------+----------------------------------------------+------------------+
| ``model_name``         | :obj:`str`   | Model name for the back-end source           | ``"bt-settl-cifist"`` |
+------------------------+--------------+----------------------------------------------+------------------+
| ``logg``               | :obj:`float` | Surface gravity log10(cm/s²), computed       | ``None``         |
|                        |              | from mass and radius if not given            |                  |
+------------------------+--------------+----------------------------------------------+------------------+

--------
Examples
--------

A Sun-like star using Phoenix4All with default SVO source::

    [Star]
    star_type = phoenix4all
    radius = 1.0
    temperature = 5800
    metallicity = 0.0

Using a different source and disabling Planck fallback::

    [Star]
    star_type = phoenix4all
    radius = 1.0
    temperature = 5800
    source = synphot
    use_planck = False


.. note::

    Before TauREx 3.5, ``star_type = phoenix`` selected a built-in
    ``PhoenixStar`` class that read ``.fits.gz`` files from a ``phoenix_path``
    directory. That class has been removed. ``star_type = phoenix`` is still
    accepted, but it now redirects to ``phoenix4all``, so the keywords listed
    above apply. ``phoenix_path`` is no longer accepted and raises an error.


.. _phoenix4all: https://github.com/taurex-space/phoenix4all
