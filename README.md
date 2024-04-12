# face2surrender


## What is the project about ?

  "Face 2 Surrender" is a mix between police sketch and line-up.
  First, you choose the characteristics of the suspect like the hair color or the age. 
  Then, we display faces that corresponds to your criterias. You select the faces closest to your attacker's and with the help of a VAE and a genetic algorithm we generate new faces based on the ones you selected. The goal is, which each iteration, to get closer to your attacker's real face.


## How is it made ?

  The UI is in the form of webpages, the autoencoder is pytorch VAE and the genetic algorithm uses functionnalities of pytorch's VAE to generate the new faces.

## Installation

  You can git clone this repository and we're developping a docker deployment solution.
