# HOLICs Code for Measuring Flexions in Python

This is a python code for demonstrating how to measure gravitational lensing flexion. 
This python code is translated from 
[Goldberg's HOLICs code in IDL](http://www.physics.drexel.edu/~goldberg/flexion/).


It includes two parts:
### Illustrating what flexion is (see Fig. 1).
Use the command below to rebuild Fig. 1.
```bash
$ python2.7 show_flexion.py
```

![Figure 1](https://raw.githubusercontent.com/linan7788626/flexion_holics_python/master/Figures/figure_1.png)
Figure.1: This figure shows an input circle source and its lensed image with flexions. In left panel, it is the unlensed source, which follows perfect circle Gaussian distribution; In right panel, lensed images is shown, the triangular shape distortion is because of gravitational lensing flexion.

### Measuring flexion and calculating the statistical properties with different sizes of window functions.
Use the command below to rebuild Fig. 2.
```bash
$ python2.7 wf_selection.py
```

![Figure 2](https://raw.githubusercontent.com/linan7788626/flexion_holics_python/master/Figures/C_W.jpg)
Figure.2: Figure 2 and Figure 3 in [Goldberg et al 2007](http://arxiv.org/pdf/astro-ph/0607602v2.pdf) can be rebuilt using this python code. 


