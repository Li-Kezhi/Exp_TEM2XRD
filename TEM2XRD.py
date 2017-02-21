#!/usr/bin/env python

"""
Reaction rate post-treatment script
"""

__author__ = "LI Kezhi"
__date__ = "$2017-01-05$"
__version__ = "1.0.0"


import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import mpltex


##### Preparation #####
# File names
SOURCE_NAME = './Examples/FFTofHRTEM.jpg'

# Read data
image = mpimg.imread(SOURCE_NAME)
imgShape = image[:, :, 0].shape
plt.imshow(image)
plt.show()

##### User Defined Parameters #####
# Ruler: actual size / pixel
RULER = 57.848 / 683

# Center: pixel
CENTER_X = 341
CENTER_Y = 341

# XRD resolution: 2Theta step
RESOLUTION = 1.5

##### Data Manipulation #####
counts = np.zeros((int(round(180.0 / RESOLUTION)) + 1, 2))
for i in xrange(counts.shape[0]):
    counts[i, 0] = RESOLUTION * (i + 0.5)
counts[-1, 0] = RESOLUTION * i

for i in xrange(imgShape[0]):
    for j in xrange(imgShape[1]):
        Distance_Pixel = math.sqrt((CENTER_X - i)**2 + (CENTER_Y - j)**2)
        Distance = Distance_Pixel * RULER
        if 0.15416 * Distance / 2 < 1:
            TwoTheta = 2 * math.asin(0.15416 * Distance / 2) * (180 / math.pi)
            GroupNumber = int(round(TwoTheta/RESOLUTION))
            counts[GroupNumber, 1] += image[i, j, 0]

##### Reports #####
# Generate Report
reportName = SOURCE_NAME.split('.jpg')[0] + '_report.txt'
output = file(reportName, 'w')
output.writelines('2Theta  counts\n')
for i in xrange(counts.shape[0]):
    output.writelines('%7.3f   %15d\n' % (counts[i, 0], counts[i, 1]))
output.close()

# Plotting
@mpltex.presentation_decorator
def plot(counts):
    fig, ax = plt.subplots()
    ax.plot(counts[:, 0], counts[:, 1])

    ax.set_xlim(0, 180)

    ax.set_yticks([])
    ax.tick_params(axis='x', top='off', bottom='off')

    # ax.legend(loc='best')
    ax.set_ylabel('Counts')
    ax.set_xlabel(r'2$\theta$($^{\circ}$)')

    plt.show()

plot(counts)
