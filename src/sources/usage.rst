Usage
=====

.. _installation:

Installation
------------

To use face2surrender, first install it :

.. code-block:: console

   A ecrire...




Using the interface
===================

The interface is designed to be simple and intuitive
but here are some steps to use it :

First page
-----------

The url (/home) allows you to choose the main characteristics of
the criminal. These characteristics will be used to sort the faces
which will be used on the following page.
You can select the features you are interested in with the drop-down
lists and click the button to submit the form and move to the next page

Second page
-----------

The url (/criminel) allows you to choose the faces most resembling
the criminal you are looking for. You can select several faces and
send them to the algorithm by clicking on the first button. You can
repeat this operation as many times as you want. At each iteration,
new images are created using the genetic algorithm. When you have
identified the criminal, you can select him and click on the second
button. It will display the last page.

Final page
-----------

The url (/resultat) allows you to display the selected criminal in
big and provides a button allowing you to start a new identification.

Genetic Algorithm
=================

.. _aim:

Aim
----

The aim of the genetic algorithm is to create new faces based on the ones you selected.
The goal is to generate faces that are closer and closer to your attacker's with each iteration of the algorithm.



How does it work ?
------------------

It is based on the properties of the latent vectors we have thanks to the use of pytorch VAE.

* First, we generate 20 new faces by making a crossover	of the parents' faces (the ones you selected).

* We then mutate those vectors by introducing random variations in their latent vector.

* Laslty, we select the 9 faces closest to our parents' ones by calculating the Euclidean distance.


We then display thoses 9 new faces on the next round and you just have to select the best ones !

Autoencoder
===========

.. _data:

Data
----

The dataset we used to train this model is celebA dataset.
You can access it on this webpage:
`celebA <https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html>`_

Due to resources limitations, we used a subset of 2000 images to train the model.



What is the model ?
--------------------

We chose to use the pytorch variational autoencoder for this project. We found that it was the best model to meet our specific requirements.
A variational autoencoder is a type of machine learning model.
It consists of an encoder network that compresses input data (here it's images) into a lower dimentional space and a decoder network that reconstructs the original data from this space.
VAEs allow to generate new data points with similar characteristics to those of the input. After training the model we can generate new images by modifying the latent space vectors.
We had to have this generation for our project because of the genetic algorithm.
The parameters of the trained model are:

.. code-block::

	latent_dim = 500
	epochs = 780

We figured those parameters were good enough to make a first version of our app.
