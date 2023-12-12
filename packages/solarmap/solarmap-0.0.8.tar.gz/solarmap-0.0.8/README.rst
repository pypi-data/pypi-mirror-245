============
SolarMAP
============

.. image:: http://img.shields.io/badge/powered%20by-SunPy-orange.svg?style=flat
    :target: http://www.sunpy.org
    :alt: Powered by SunPy Badge
 
    
SolarMAP uses SunPy to plot and return coordinates of different spacecraft and planets around the sun give a date.

Features:

-   Returns point coordinates in HEE and Rsun of Spacecraft and Planets for a give date
-   Returns a range of coordinates in HEE and Rsun for a date and previous number of days before for spacecraft and planets. 
-   Plots in HEE 

Contributions and comments are welcome using Github at: 
https://github.com/canizarl/solarmap

Please note that SolarMAP requires:

- SunPy 
- Astropy

Installation
============

install via pip:

.. code-block::

    pip install solarmap

Get the latest version via pip:

.. code-block::

    pip install --upgrade solarmap

include in your python script:

.. code-block::

    import solarmap



Configuration
=============



Documentation
=============
    To find all supported planets and spacecraft:

    .. code-block:: python
        ids = solarmap.get_HEE_coord.show_spacecraft_ids(get_HEE_coord)
    

Usage
=====
EXAMPLE:

.. code-block:: python
    
    import solarmap
    import numpy as np
    
    objects = ['sun', 'earth', 'Venus', 'psp', 'solo', 'tesla', 'mars']

    # Generate map
    solarsystem = solarmap.get_HEE_coord(date=[2023, 6, 26], objects=objects, orbitlength=100, timeres=24)

    # gives the location of the objects at the specified DATE without orbits or labels.
    simple_coord_rsun = np.array(solarsystem.locate_simple())

    # Plotting map of objects
    figure = solarsystem.plot()

    # Verbose version of coordinates with orbit, with labels. the last position is the specified date.
    coord_rsun = solarsystem.locate()



Bugs & Contribution
===================

Please use Github to report bugs, feature requests and submit your code:
https://github.com/canizarl/solarmap

:author: Luis Alberto Canizares
:date: 2022/11/22
