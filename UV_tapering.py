'''
Tool to plot the input and output results of running
~/ALMA_archive/research_code/tools/taper_testing.py and for finding the closest
match between those outputs and a specified beam major and minor axis and
position angle. The metric used to find the closest match is simply the distance
between each output beam parameter and the target parameters calculated with

    metric = sqrt((resultMajor - targetMajor)^2 +
                  (resultMinor - targetMinor)^2 +
                  (resultPA - targetPA)^2).

Plots of all inputs and outputs are shown in three projected planes of minor
axis vs. major axis, position angle vs. major axis and position angle vs. minor
axis. Target parameters are marked and the closest match as well. Equivalent
position angles (i.e. +/- 180 degrees) are marked but only the input position
angle is used for the calculation of the closest match.

This is meant to be run in a terminal with Python. The first three arguments are
the target beam parameters major axis, minor axis and position angle. The fourth
argument is the directory containing the taper testing output files. The fifth
argument is a boolean switch which determines if the distance metric is
calculated without the position angle portion. An example call is:

    $ python plot_UV_taper_tests.py 2.60 1.63 81.07 ../tst_tapering/ False

with example terminal output:

    Closest 3-space match:
      target: 2.6" x 1.63", 81.07 deg
      input: 2.921" x 1.791", 84.364 deg
      output: 2.587" x 1.61", 81.093 deg
      index: 23531
      distance from target: 0.0331360830516

Input target beam parameters must be in arcseconds, arcseconds and degrees. The
location of the taper testing output files must include a trailing slash. The
input that determines if the position angle is excluded from the distance
calculations must be either "True" or "False" (without quotation marks).
'''

import glob
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import sys

#gather up target beam and files
target = np.array([sys.argv[1], sys.argv[2], sys.argv[3]], dtype=float)
if target[2] > 0.0:
    invertPA = target[2] - 180.0
else:
    invertPA = target[2] + 180.0
storageDir = sys.argv[4]
outputFiles = glob.glob(storageDir+'taper_test_output_*')

#load taper tests
#inMaj, inMin, inPA, outMaj, outMin, outPA = np.loadtxt(outputFiles[0], \
#                                                       unpack=True)
inMaj, inMin, inPA, outMaj, outMin, outPA = np.loadtxt('tapering_test/taper_test_output_nov162017_1', unpack=True)

for i in np.arange(1, len(outputFiles)):
    tmp = np.loadtxt(outputFiles[i])
    inMaj = np.append(inMaj, tmp[:, 0])
    inMin = np.append(inMin, tmp[:, 1])
    inPA = np.append(inPA, tmp[:, 2])
    outMaj = np.append(outMaj, tmp[:, 3])
    outMin = np.append(outMin, tmp[:, 4])
    outPA = np.append(outPA, tmp[:, 5])

#calculate metric
if sys.argv[5] == 'True':
    metric = np.sqrt((outMaj - target[0])**2 + \
                     (outMin - target[1])**2)
    print 'Closest 2-space match (ignoring PA):'
elif sys.argv[5] == 'False':
    metric = np.sqrt((outMaj - target[0])**2 + \
                     (outMin - target[1])**2 + \
                     (outPA - target[2])**2)
    print 'Closest 3-space match:'
else:
    raise ValueError('Fifth input must be "True" or "False" exactly.')
#find closest match where axes are less than target
metricSortInds = np.argsort(metric)
minIndMetric = 0
for i in metricSortInds:
    if outMaj[i] <= target[0] and outMin[i] <= target[1]:
        minIndMetric = i
        break
#print findings
print '  target:', str(target[0])+'" x '+str(target[1])+'", '+ \
      str(target[2])+' deg'
print '  input:', str(inMaj[minIndMetric])+'" x '+str(inMin[minIndMetric])+ \
      '", '+str(inPA[minIndMetric])+' deg'
print '  output:', str(outMaj[minIndMetric])+'" x '+str(outMin[minIndMetric])+ \
      '", '+str(outPA[minIndMetric])+' deg'
print '  index:', minIndMetric
print '  distance from target:', metric[minIndMetric]

#calculate distance to line
#distance(ax+by+c=0, at x0,y0) = |a*x0+b*y0+x| / sqrt(a^2+b^2)
#a=-1, b=1, c=0
#distance = |x0-y0| / sqrt(2)
#point x = (x0+y0)/sqrt(2)
#point y = (y0+x0)/sqrt(2)

#inputs
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(inMaj, inMin, inPA, color='k', label='Input')
ax.scatter([inMaj[minIndMetric]], [inMin[minIndMetric]], [inPA[minIndMetric]], \
            color='g', marker='^', label='Closest Match')
ax.set_xlabel('Input Major Axis')
ax.set_ylabel('Input Minor Axis')
ax.set_zlabel('Input Position Angle')
ax.legend()
#plt.show()
plt.close()

#outputs
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(outMaj, outMin, outPA, color='k', label='Output')
ax.scatter([outMaj[minIndMetric]], [outMin[minIndMetric]], \
           [outPA[minIndMetric]], color='g', marker='^', s=200, \
           label='Closest Match')
ax.scatter([target[0]], [target[1]], [target[2]], color='r', marker='x', \
           label='Target')
#ax.set_xlim([0, 5])
#ax.set_ylim([0, 5])
#ax.set_zlim([100, 105])
ax.set_xlabel('Output Major Axis')
ax.set_ylabel('Output Minor Axis')
ax.set_zlabel('Output Position Angle')
ax.legend()
#plt.show()
plt.close()

#plot inputs
fig = plt.figure()
ax1 = fig.add_subplot(2, 3, 1)
ax2 = fig.add_subplot(2, 3, 2)
ax3 = fig.add_subplot(2, 3, 3)
ax1.scatter(inMaj, inMin, color='k', label='Input')
ax1.scatter([inMaj[minIndMetric]], [inMin[minIndMetric]], \
            color='g', marker='^', label='Closest Match')
ax1.set_xlabel('Input Major Axis')
ax1.set_ylabel('Input Minor Axis')
ax1.legend(loc='upper left')
ax2.scatter(inMaj, inPA, color='k')
ax2.scatter([inMaj[minIndMetric]], [inPA[minIndMetric]], \
            color='g', marker='^')
ax2.set_xlabel('Input Major Axis')
ax2.set_ylabel('Input Position Angle')
#ax2.set_ylim([-70.0, -40.0])
ax3.scatter(inMin, inPA, color='k')
ax3.scatter([inMin[minIndMetric]], [inPA[minIndMetric]], \
            color='g', marker='^')
ax3.set_xlabel('Input Minor Axis')
ax3.set_ylabel('Input Position Angle')
#ax3.set_ylim([-70.0, -40.0])

#plot outputs
ax4 = fig.add_subplot(2, 3, 4)
ax5 = fig.add_subplot(2, 3, 5)
ax6 = fig.add_subplot(2, 3, 6)
ax4.scatter(outMaj, outMin, color='k', label='Output')
ax4.scatter([outMaj[minIndMetric]], [outMin[minIndMetric]], \
            color='g', marker='^', label='Closest Match')
ax4.scatter([target[0]], [target[1]], color='r', marker='x', label='Target')
ax4.plot([0,1],[0,1], 'k--')
ax4.axhline(y=0.618,c='b',ls='-')
ax4.axvline(x=0.692,c='b', ls='-')
#distance = |x0+y0| / sqrt(2)
#point x = (x0-y0)/sqrt(2)
#point y = (y0-x0)/sqrt(2)
#print 'nearest distance = ' + str(min(abs(outMaj-outMin)/np.sqrt(4))) + ' at x = ' +str()
ax4.set_xlim(0.65,1.05)
ax4.set_ylim(0.55,0.95)
ax4.set_xlabel('Output Major Axis')
ax4.set_ylabel('Output Minor Axis')
ax4.legend(loc='upper left')
ax5.scatter(outMaj, outPA, color='k')
ax5.scatter([outMaj[minIndMetric]], [outPA[minIndMetric]], \
            color='g', marker='^')
ax5.scatter([target[0], target[0]], [target[2], invertPA], color='r', \
            marker='x')
ax5.set_xlabel('Output Major Axis')
ax5.set_ylabel('Output Position Angle')
ax5.set_ylim([-190.0, 190.0])
ax6.scatter(outMin, outPA, color='k')
ax6.scatter([outMin[minIndMetric]], [outPA[minIndMetric]], \
            color='g', marker='^')
ax6.scatter([target[1], target[1]], [target[2], invertPA], color='r', \
            marker='x')
ax6.set_xlabel('Output Minor Axis')
ax6.set_ylabel('Output Position Angle')
ax6.set_ylim([-190.0, 190.0])
plt.savefig('spt0348_b7_taper_circular.pdf', bbox_inches='tight')
plt.show()

#input vs. output (binned in PA) - min, maj, PA
#ask if circularizing? if yes, 
	#plot 1:1 and measure closest distance to 1:1 on output maj and min
	#throw away output PA plots
	#
#circularizing with taget? if yes, (see above) + plot point

#input PA plot could be zoomed in
#PA plots could be radial plots
#show top 5? closest matches 
	#colourize (B&W) by distance to target
