#####################################
Human-Friendly Pedantic ``timedelta``
#####################################

.. CXREF:
   https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge

.. image:: https://github.com/doblabs/human-friendly_pedantic-timedelta/actions/workflows/checks-unspecial.yml/badge.svg?branch=release
  :target: https://github.com/doblabs/human-friendly_pedantic-timedelta/actions/workflows/checks-unspecial.yml/badge.svg?branch=release
  :alt: Build Status

.. CXREF: https://app.codecov.io/gh/doblabs/human-friendly_pedantic-timedelta/settings/badge

.. image:: https://codecov.io/gh/doblabs/human-friendly_pedantic-timedelta/graph/badge.svg?token=NKL19HdM5o
  :target: https://codecov.io/gh/doblabs/human-friendly_pedantic-timedelta
  :alt: Coverage Status

.. image:: https://readthedocs.org/projects/human-friendly_pedantic-timedelta/badge/?version=latest
  :target: https://human-friendly_pedantic-timedelta.readthedocs.io/en/latest/
  :alt: Documentation Status

.. image:: https://img.shields.io/github/v/release/doblabs/human-friendly_pedantic-timedelta.svg?style=flat
  :target: https://github.com/doblabs/human-friendly_pedantic-timedelta/releases
  :alt: GitHub Release Status

.. image:: https://img.shields.io/pypi/v/human-friendly_pedantic-timedelta.svg
  :target: https://pypi.org/project/human-friendly_pedantic-timedelta/
  :alt: PyPI Release Status

.. image:: https://img.shields.io/pypi/pyversions/human-friendly_pedantic-timedelta.svg
  :target: https://pypi.org/project/human-friendly_pedantic-timedelta/
  :alt: PyPI Supported Python Versions

.. image:: https://img.shields.io/github/license/doblabs/human-friendly_pedantic-timedelta.svg?style=flat
  :target: https://github.com/doblabs/human-friendly_pedantic-timedelta/blob/release/LICENSE
  :alt: License Status

A Python ``timedelta`` wrapper which provides pedantic string formatting.

Install with ``pip``::

    pip3 install human-friendly_pedantic-timedelta

For more options, read the
`installation guide
<https://human-friendly-pedantic-timedelta.readthedocs.io/en/latest/installation.html>`__.

Simple example::

    $ python3
    >>> from pedantic_timedelta import PedanticTimedelta
    >>> PedanticTimedelta(days=0.33).time_format_scaled()
    # OUTPUT
    # ('7.92 hours', 3600.0, 'hour')

|

.. image:: https://raw.githubusercontent.com/hotoffthehamster/human-friendly_pedantic-timedelta/release/docs/assets/hfpt-logo-lrg.png
   :target: https://human-friendly-pedantic-timedelta.readthedocs.io/en/latest/authors.html#graphics-shout-out
   :align: center
   :alt: "Penrose Hourglass"

