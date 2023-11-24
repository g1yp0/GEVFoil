from math import cos, sin


class STL(object):
    """ Takes X and Y coords and exports a '1' deep 2.5D aerofoil STL """
    def __init__(self, xy, filename):
        super(STL, self).__init__()
        filecontents = 'solid ' + filename + '\n'

        for i, point in enumerate(xy):
            if i+1 == len(xy):
                pass
            else:
                # TO-DO correct normal **********************
                filecontents += "facet normal 0 0 1\n"
                filecontents += "   outer loop\n"
                filecontents += "        vertex " + point[0] + " 0 " + \
                                point[1] + "\n"
                filecontents += "        vertex " + point[0] + " 1 " + \
                                point[1] + "\n"
                filecontents += "        vertex " + xy[i+1][0] + " 0 " \
                                + xy[i+1][1] + "\n"
                filecontents += "   endloop\n"
                filecontents += "endfacet\n"
                filecontents += "facet normal 0 0 1\n"
                filecontents += "   outer loop\n"
                filecontents += "        vertex " + point[0] + " 1 " \
                                + point[1] + "\n"
                filecontents += "        vertex " + xy[i+1][0] + " 0 " \
                                + xy[i+1][1] + "\n"
                filecontents += "        vertex " + xy[i+1][0] + " 1 " + \
                                xy[i+1][1] + "\n"
                filecontents += "   endloop\n"
                filecontents += "endfacet\n"

        filecontents += 'endsolid' + filename

        f = open(filename+'.stl', 'w')
        f.write(filecontents)
        f.close()


class BlockMesh(object):
    """A class that creates a 2.5D OpenFOAM BlockMesh
       Assumes LE is (0, 0) """
    def __init__(self, xy, filename='blockMeshDict'):
        super(BlockMesh, self).__init__()

        #
        # First write the header
        #
        contents = """/*--------------------------------*- C++ -*-------------\
------------------*\\
| =========                 |                                              |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox        |
|  \\\\    /   O peration     | Version:  2.3.0                              |
|   \\\\  /    A nd           | Web:      www.OpenFOAM.org                   |
|    \\\\/     M anipulation  |                                              |
\*------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * // """

        #
        # Write the verticies
        #
        contents += '\n\nvertices\n(\n'

        for i, coord in enumerate(xy):
            j = i*4
            contents += '    ('
            contents += '% 10.8f ' % coord[0]
            contents += '% 10.8f ' % coord[1]
            contents += '% 10.8f' % 0
            contents += ')  // ' + str(j) + ' - aerofoil upper z0\n'

            contents += '    ('
            contents += '% 10.8f ' % coord[0]
            contents += '% 10.8f ' % coord[1]
            contents += '% 10.8f' % 1
            contents += ')  // ' + str(j+1) + ' - aerofoil upper z1\n'

            x = coord[0] - (5 * cos(coord[0]*1.57079633))
            y = 5 * sin(coord[0]*1.57079633)
            contents += '    ('
            contents += '% 10.8f ' % x
            contents += '% 10.8f ' % y
            contents += '% 10.8f' % 0
            contents += ')  // ' + str(j+2) + ' - cmesh upper z0\n'

            contents += '    ('
            contents += '% 10.8f ' % x
            contents += '% 10.8f ' % y
            contents += '% 10.8f' % 0
            contents += ')  // ' + str(j+3) + ' - cmesh upper z1\n'

        contents += ');\n'

        #
        # Write the blocks
        #
        contents += '\nblocks\n(\n'

        for i in range(len(xy)-1):
            j = i * 4
            contents += '    hex ('
            contents += str(j)+' '+str(j+5)+' '+str(j+6)+' '+str(j+1)
            contents += ' '+str(j+2)+' '+str(j+7)+' '+str(j+8)+' '+str(j+3)
            contents += ') (15 15 1) simpleGrading (1 1 1)\n'
        contents += ');\n'

        ###########

        contents += """edges
(
);

boundary
(
);

mergePatchPairs
(
);

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
"""

        # for x in zip(*[iter(xy)]*3):
        #     print x

        fn = open(filename, 'w')
        fn.write(contents)
        fn.close()

        pass
