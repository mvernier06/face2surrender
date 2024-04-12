Autoencoder
=====

.. _data:

Data
------------

The dataset we used to train this model is celebA dataset.
You can access it on this webpage:
	`celebA <https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html>`_

Due to resources limitations, we used a subset of 2000 images to train the model.



What is the model ?
-------------------

We chose to use the pytorch variational autoencoder for this project. We found that it was the best model to meet our specific requirements.
A variational autoencoder is a type of machine learning model. 
It consists of an encoder network that compresses input data (here it's images) into a lower dimentional space and a decoder network that reconstructs the original data from this space.
VAEs allow to generate new data points with similar characteristics to those of the input. After training the model we can generate new images by modifying the latent space vectors.
We had to have this generation for our project because of the genetic algorithm.
The parameters of the trained model are:
	*latent_dim = 500 
	*epochs = 780
We figured those parameters were good enough to make a first version of our app.