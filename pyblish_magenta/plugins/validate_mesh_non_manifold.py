import pyblish.api
from maya import cmds


class SelectManifoldVertices(pyblish.api.Action):
    label = "Manfifold Vertices"
    on = "failed"
    icon = "hand-o-up"

    def process(self, context):
        # meshs = []
        invalid = []
        for result in context.data["results"]:
            if result["plugin"] is not ValidateMeshNonManifold:
                continue

            if result["error"] is None:
                continue

            instance = result["instance"]
            invalid.extend(cmds.polyInfo(instance, nonManifoldVertices=True) or [])

        # meshs = list(set(meshs))
        invalid = list(set(invalid))
        self.log.info("Selecting bad vertices: %s" % ", ".join(invalid))
        cmds.select(cl=True)
        cmds.select(invalid)


class SelectManifoldEdges(pyblish.api.Action):
    label = "Manfifold Edges"
    on = "failed"
    icon = "hand-o-up"

    def process(self, context):
        meshs = []
        invalid = []
        for result in context.data["results"]:
            if result["plugin"] is not ValidateMeshNonManifold:
                continue

            if result["error"] is None:
                continue

            instance = result["instance"]
            invalid.extend(cmds.polyInfo(instance, nonManifoldEdges=True) or [])

        meshs = list(set(meshs))
        invalid = list(set(invalid))
        if not invalid:
            self.log.info("bad edge not found: %s")
            return

        self.log.info("Selecting bad meshs: %s" % ", ".join(invalid))
        cmds.select(cl=True)
        cmds.select(invalid)


class ValidateMeshNonManifold(pyblish.api.Validator):
    """Ensure that meshes don't have non-manifold edges or vertices"""

    families = ['model']
    hosts = ['maya']
    category = 'geometry'
    version = (0, 1, 0)
    label = 'Mesh Non-Manifold Vertices/Edges'
    actions = [
        pyblish.api.Category("Select Affected"),
        SelectManifoldVertices,
        SelectManifoldEdges,
        pyblish.api.Separator,
    ]

    def process(self, instance):
        """Process all the nodes in the instance 'objectSet'"""
        meshes = cmds.ls(instance, type='mesh', long=True)

        invalid = []
        for mesh in meshes:
            if (cmds.polyInfo(mesh, nonManifoldVertices=True) or
                cmds.polyInfo(mesh, nonManifoldEdges=True)):

                invalid.append(mesh)

        if invalid:
            raise ValueError("Meshes found with non-manifold edges/vertices: {0}".format(invalid))
