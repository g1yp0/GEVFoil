import numpy as np

class NACA4(object):
    """A class for generating  NACA 4 series aerofoils
        with improved leading-edge capture """
    def __init__(self, foil, points=800, chord=1):
        super(NACA4, self).__init__()
        m = float(foil[0])/100      # max camber
        p = float(foil[1])/10       # chordwise position of max camber
        t = float(foil[2:])/100     # thickness

        # Cosine-spaced points for better LE resolution
        beta = np.linspace(0, np.pi, points)
        x = chord * (0.5 * (1 - np.cos(beta)))  # Cosine spacing of points
        self.x = x

        yt = self.thickness(x, t)
        yc = []
        for coord in x:
            if m:
                yc.append(self.camber(m, p, coord))
            else:
                # No camber
                yc.append(0)
        y1 = yc + yt
        y2 = yc - yt
        self.y = y1
        self.y2 = y2

    def thickness(self, x, t):
        # Y thickness at given x point
        return t / 0.2 * \
            (0.2969*np.sqrt(x)-0.126*x-0.3516*x**2+0.2843*x**3-0.1015*x**4)

    def camber(self, m, p, x):
        # Return the camber of the aerofoil
        if x <= p:
            return m/p**2 * (2*p*x-x**2)
        return m/(1-p)**2*((1-2*p)+2*p*x-x**2)

if __name__ == "__main__":
    test = NACA4('0012')
