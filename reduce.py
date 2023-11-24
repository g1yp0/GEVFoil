from rdp import rdp
import numpy as np

class RDP(object):
    """A class to decimate aerofoil points"""
    def __init__(self, x, y, e=0.0001):
        xy = np.vstack((x, y)).T
        self.reducedXY = rdp(xy, epsilon=e)
        self.reducedX = self.reducedXY[:,0]
        self.reducedY = self.reducedXY[:,1]