Sphinx documentation
====================

One of the main goles of DIP is to help developers to rapidly write their code.
Description and validation of input parameters is often tedious and automatic approach to this proces can save a lot of time.
That's why DIP comes with an extension for the Sphinx engine, that reads DIP files and automatically generates corresponding documentation.

First we have to register DIP documentation class as an extension in Sphinx configuration file ``conf.py``.

.. code-block:: python

   >>> import sys
   >>> sys.path.insert(0,"../../src")              # import recent version of scinumtools
   >>> import scinumtools
   >>> 
   >>> extensions = ['scinumtools.dip.docs']

Creating a documetation to this file is straightforward using ``.. dipdocs::`` directive in any restructured text file of a Sphinx documentation. Optional parameter ``:show-code`` will add a code block with the DIP code and link node description with corresponding code lines.

.. code-block:: rst

   .. dipdocs:: <file-name>
      :show-code:
      
Example documentations to the files used in examples are listed below:
		
.. toctree::
   :maxdepth: 1

   sphinx_definitions
   sphinx_nodes
   sphinx_docstest
