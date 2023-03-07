.. highlight:: shell

===============================
PDSSP workflow manager
===============================

.. image:: https://img.shields.io/github/v/tag/pole-surfaces-planetaires/pdssp-airflow
.. image:: https://img.shields.io/github/v/release/pole-surfaces-planetaires/pdssp-airflow?include_prereleases

.. image https://img.shields.io/github/downloads/pole-surfaces-planetaires/pdssp-airflow/total
.. image https://img.shields.io/github/issues-raw/pole-surfaces-planetaires/pdssp-airflow
.. image https://img.shields.io/github/issues-pr-raw/pole-surfaces-planetaires/pdssp-airflow
.. image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :target: https://github.com/pole-surfaces-planetaires/pdssp-airflow/graphs/commit-activity
.. image https://img.shields.io/github/license/pole-surfaces-planetaires/pdssp-airflow
.. image https://img.shields.io/github/forks/pole-surfaces-planetaires/pdssp-airflow?style=social


Workflow manager for the PDSSP platform.


Stable release
--------------

To install PDSSP workflow manager, run this command in your terminal:

.. code-block:: console

    $ pip install pdssp-airflow

This is the preferred method to install PDSSP workflow manager, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for PDSSP workflow manager can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/pole-surfaces-planetaires/pdssp-airflow

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/pole-surfaces-planetaires/pdssp-airflow/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ make  # install in the system root
    $ make user # or Install for non-root usage


.. _Github repo: https://github.com/pole-surfaces-planetaires/pdssp-airflow
.. _tarball: https://github.com/pole-surfaces-planetaires/pdssp-airflow/tarball/master



Development
-----------

.. code-block:: console

        $ git clone https://github.com/pole-surfaces-planetaires/pdssp-airflow
        $ cd pdssp-airflow
        $ make prepare-dev
        $ source .pdssp-airflow
        $ make install-dev


To get more information about the preconfigured tasks:

.. code-block:: console

        $ make help

Usage
-----

To use PDSSP workflow manager in a project::

    import pdssp-airflow



Run tests
---------

.. code-block:: console

        $make tests



Author
------
👤 **Jean-Christophe Malapert**



🤝 Contributing
---------------
Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/pole-surfaces-planetaires/pdssp-airflow/issues). You can also take a look at the [contributing guide](https://github.com/pole-surfaces-planetaires/pdssp-airflow/blob/master/CONTRIBUTING.rst)


📝 License
----------
This project is [GNU Lesser General Public License v3](https://github.com/pole-surfaces-planetaires/pdssp-airflow/blob/master/LICENSE) licensed.
