.. face2surrender documentation master file, created by
   sphinx-quickstart on Thu Apr 11 12:51:12 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to face2surrender's documentation!
==========================================

**face2surrender** is a Python application, using the CelebA database to identify a criminel.
It is using a variational autoencoder and a genetic algorithm in order
to propose some pictures of faces. We use several selection of pictures to create
new faces in order to find a face that looks like the criminal we are looking for.
It provides a simple and intuitive interface to do so.


Check out the :doc:`usage` section for further information, including how to
:ref:`install <installation>` the project.

For more information on the **autoencoder**, check out the autoencoder section of the :doc:`usage` (you'll have information on the :ref:`data <data>` too).

And finally, you can check how we generated new faces with the **genetic-algorithm** on the :doc:`usage`.

.. note::

   This project is under active development.


  Contents
  ---------

.. toctree::
	:maxdepth: 2
	:caption: Contents: lien vers les sections :

	usage
	autoencoder
	genetic-algorithm
