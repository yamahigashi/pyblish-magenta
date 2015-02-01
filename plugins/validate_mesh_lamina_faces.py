import pyblish.api
from maya import cmds


class ValidateMeshLaminaFaces(pyblish.api.Validator):
    """ Validate meshes don't have lamina faces.
        Lamina faces share all of their edges. """
    families = ['modeling']
    hosts = ['maya']
    category = 'geometry'
    version = (0, 1, 0)

    def process_instance(self, instance):
        """Process all the nodes in the instance 'objectSet' """
        member_nodes = cmds.sets(instance.name, q=1)
        meshes = cmds.ls(member_nodes, type='mesh', dag=True, long=True)

        invalid = []
        for mesh in meshes:
            if cmds.polyInfo(mesh, laminaFaces=True):
                invalid.append(mesh)

        if invalid:
            raise ValueError("Meshes found with lamina faces: {0}".format(invalid))