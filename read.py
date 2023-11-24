import os

class AerofoilReader(object):
    """ An abstract class to be inherited by classes for specific
        aerofoil file types """
    def __init__(self, filename):
        super(AerofoilReader, self).__init__()
        self.coord = []
        self.title = []  # Column titles
        self.label = []  # Aerofoil Label

        foil = open(filename, 'r')
        self.lines = foil.readlines()


class CSVReader(AerofoilReader):
    """ Read in CSV. Assumes a header is present."""
    def __init__(self, filepath, xcol, ycol, zcol=False):
        super(CSVReader, self).__init__(filepath)

        self.label = os.path.basename(filepath).split('.')[0]

        inpcols = 3        # Two or three columns
        if not zcol:
            inpcols = 2

        for i, line in enumerate(self.lines):
            parts = line.rstrip().replace('"', '').split(',')
            additional = []

            if i > 0:
                # Not the header
                if len(parts) > inpcols:
                    # More than x, y & z - store other columns
                    for j in range(len(parts)):
                        if j != xcol and j != ycol and j != zcol:
                            additional.append(parts[j])

                xyz = [parts[xcol], parts[ycol], parts[zcol]]
                self.coord.append(xyz + additional)
            else:
                # It's the header
                self.title = parts

    def test(self):
        print('test')
