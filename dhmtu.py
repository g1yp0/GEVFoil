#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

"""
##############################################################################
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

##############################################################################

A simple script to produce DHMTU aerofoils. This script is based on an
open-source script distrbuted under the GNU GPL, hence the inclusion of the 
licence statements of the original script. This differs from the Creative
Commons Attribution-NonCommercial 3.0 Unported License elsewhere in GEVfoil.

Based on the Matlab of (Martin Hepperle) 2012-02-01 which was
converted from the Mathematica provided by Chang Chong-Hee, 1996

Rewritten into Python in April 2021 (Jason Moller)
@author: glypo (Jason Moller)
"""

class DHMTU(object):
    """A class for generating  DHMTU aerofoils"""
    def __init__(self, foil, points=100, chord=1):
        super(DHMTU, self).__init__()
        
        tu = foil[0] / 100
        xt = foil[1] / 100
        t1 = foil[2] / 100
        x1 = foil[3] / 100
        t2 = foil[4] / 100
        x2 = foil[5] / 100
        delb = foil[6] / 100
        k = foil[7]
        
        # Determine coefficients
        c0 = t1
        c1 = (t2-t1)/(x2-x1)
        
        d1 = delb
        d2 =(-2*delb + 3*tu + 2*delb*xt)/(xt-1)**2
        d3 =(  -delb + 2*tu +   delb*xt)/(xt-1)**3
        
        a0 = np.sqrt(2)*np.sqrt(k)*tu
        a1 = (3*tu)/xt - (15*np.sqrt(k)*tu)/(4*np.sqrt(2)*np.sqrt(xt)) + d2*xt + 3*d3*xt - 3*d3*xt**2
        a2 = (-2*d2) - (6*d3) - (3*tu)/(xt**2) + (5*np.sqrt(k)*tu)/(2*np.sqrt(2)*xt**(3/2)) + 6*d3*xt
        a3 = -3*d3 + tu/xt**3 - (3*np.sqrt(k)*tu)/(4*np.sqrt(2)*xt**(5/2)) + d2/xt + 3*d3/xt
        
        b0 = np.sqrt(2)*np.sqrt(k)*tu
        b1 = (-8*t1*x1 - 16*t2*x1 + 15*np.sqrt(2)*np.sqrt(k)*tu*x1**(3/2) + 24*t1*x2 - 15*np.sqrt(2)*np.sqrt(k)*tu*np.sqrt(x1)*x2)/(8* x1*(x2-x1))
        b2 = (5*np.sqrt(k)*tu)/(2*np.sqrt(2)*x1**(3/2)) + (3*t1*x2)/(x1**2*(x1-x2)) + (3*t2)/(x1*x2 - x1**2)
        b3 = (-3*np.sqrt(k)*tu)/(4*np.sqrt(2)*x1**( 5/2)) + (t1*x2-t2*x1)/(x1**3*(x2-x1))
        
        e1 = (2*t1 - 2*t2 + 3*t2*x1-2*t1*x2 - t2*x2) / (x1-x2-x1*x2 + x2**2);
        e2 = (3*(t2-t1-t2*x1 +t1*x2))/((1-x2)**2*(x1-x2))
        e3 = (t2-t1-t2*x1 +t1*x2)/((x1-x2)*(x2-1)**3)
        
        # prepare table of points from trailing edge via upper surface to nose and back to trailing edge
        phiRange = np.linspace(np.pi, 0, points)
        
        xp = np.zeros(2 * points-1)
        yp = np.zeros(2 * points-1)
        
        # 1-based index of leading edge point
        idxLE = points-1
        
        for i, phi in enumerate(phiRange):
            x = (1 + np.cos(phi)) / 2
            
            # upper surface
            if x <= xt:
               yu = a0*np.sqrt(x) + a1*x + a2*x**2 + a3*x**3;
            else:
               yu = d1*(1-x) + d2*(1-x)**2 + d3*(1-x)**3
            
            xp[idxLE-i] = x
            yp[idxLE-i] = yu
            
            # lower surface
            if x <= x1:
               yl = -b0*np.sqrt(x) - b1*x -b2*x**2 - b3*x**3
            elif x <= x2:
               yl = -c0 - c1*(x-x1)
            else:
               yl = -e1*(1-x) - e2*(1-x)**2 - e3*(1-x)**3
            
            xp[idxLE+i] = x
            yp[idxLE+i] = yl
            
        # Scale the chord
        xp = xp * chord
        yp = yp * chord
            
        #plt.plot(xp, yp, '.')
        plt.plot(xp, yp)
        plt.grid(True)
        plt.axis('equal')
        plt.show()
              

if __name__ == "__main__":
    test = DHMTU([12, 35, 3, 10, 2, 80, 12, 2])