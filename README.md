# spheresVolume
Python interface to compute the analytic area and volume of overlapping spheres via the ARVO method.

## Installation
Compile the shared library:

**gcc -fPIC -c arvo.c -lm -std=c99**

**gcc -shared arvo.o -o libArvo.so**

In case some python3 libraries are missing use pip3 install

## Usage
Store the spheres coordinates in a xyzr file containing 4 columns organized as follows:

| | x | y | z | radius|
| --- | --- | --- | --- | --- |
sphere 1 | | | | |
sphere 2 | | | | |
... | | | | |
sphere n | | | | |

python3 arco.py **\<coordinates_file.xyzr\>**

## Credits
The script uses with small modifications the C version of the ARVO softwares (*arvo.c*) for the analytical computation of volume and areas of ensembles of overlapping spheres.
The original paper can be found here: [J. Buša Jr. et al., Computer Physics Communications 183 (2012) 2494–2497](https://www.sciencedirect.com/science/article/pii/S0010465512001580) 


