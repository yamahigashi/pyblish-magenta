import pyblish.api
from maya import cmds
import re


def shortName(node):
    return node.rsplit("|", 1)[-1].rsplit(":", 1)[-1]


class ValidateNoRename(pyblish.api.Validator):
    """ Checks to see if there are nodes with the original names.
        If so it can be a cue for a scene/model that hasn't been cleaned yet.
        This will check for geometry related names, like nurbs & polygons.
    """
    families = ['modeling']
    hosts = ['maya']
    category = 'cleanup'
    optional = True
    version = (0, 1, 0)

    __simpleNames = set(['pSphere', 'pCube', 'pCylinder', 'pCone', 'pPlane', 'pTorus',
                         'pPrism', 'pPyramid', 'pPipe', 'pHelix', 'pSolid',
                         'nurbsSphere', 'nurbsCube', 'nurbsCylinder', 'nurbsCone',
                         'nurbsPlane', 'nurbsTorus', 'nurbsCircle', 'nurbsSquare'])
    __simpleNamesRegex = [re.compile('{0}[0-9]?$'.format(x)) for x in __simpleNames]

    def process_instance(self, instance):
        """Process all the nodes in the instance 'objectSet' """
        member_nodes = cmds.sets(instance.name, q=1)
        transforms = cmds.ls(member_nodes, type='transform')
        
        invalid = []
        for t in transforms:
            t_shortName = shortName(t)
            for regex in self.__simpleNamesRegex:
                if regex.match(t_shortName):
                    invalid.append(t)
                    break
            
        if invalid:
            raise ValueError("Non-renamed objects found: {0}".format(invalid))