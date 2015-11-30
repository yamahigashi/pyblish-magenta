import pyblish.api
from maya import cmds
import maya.OpenMaya as OpenMaya
# import maya.api.OpenMaya as OpenMaya  # when it's comming...?


def _n(name):
    sellist = OpenMaya.MSelectionList()
    OpenMaya.MGlobal.getSelectionListByName(name, sellist)
    try:
        dp = OpenMaya.MDagPath()
        sellist.getDagPath(0, dp)
        return dp
    except:
        mo = OpenMaya.MObject()
        sellist.getDependNode(0, mo)
        return mo


def _get_hard_edge(mesh):
    """ Returns hard edges on given mesh(s) """
    hard_edges = []

    '''
    # Python API 1.0
    mesh_path = _n(selected_mesh[0])
    edge_iter = OpenMaya.MItMeshEdge(mesh_path.node())

    while not edge_iter.isDone():
        edge_iter.next()
        # if edge_iter.currentItem()
        if not edge_iter.isSmooth():
            hard_edges.append(edge_iter.currentItem())
    '''

    # mel base
    if isinstance(mesh, list):
        all_edges = cmds.ls([str(x) + ".e[*]" for x in mesh], flatten=True)
    else:
        all_edges = cmds.ls("{0}.e[*]".format(mesh), flatten=True)

    for edge in all_edges:
        edge_vertices = cmds.polyInfo(edge, edgeToVertex=True)
        if "Hard" in edge_vertices[0]:
            hard_edges.extend([edge, ])

    return hard_edges


class SelectHardEdges(pyblish.api.Action):
    label = "Hard Edges"
    icon = "hand-o-up"
    on = "failed"

    def process(self, context):
        hard_edges = []

        instances = []
        for result in context.data["results"]:
            if result["plugin"] is not ValidateMeshNonHardEdge:
                continue

            if result["error"] is None:
                continue

            instance = result["instance"]
            # if "affected" not in getattr(instance, "data", []):
            #    continue

            instances.extend(cmds.ls(instance, type='mesh', long=True))
            # meshs.extend(cmds.ls(instance, type='mesh', long=True))

        hards = _get_hard_edge(instances)
        if hards > 0:
            hard_edges.extend(hards)

        self.log.info("Selecting hard edges: %s" % ", ".join(hards))
        cmds.select(cl=True)
        cmds.select(hards)


class ValidateMeshNonHardEdge(pyblish.api.Validator):
    """Ensure that meshes don't have hard edges"""

    families = ['model']
    hosts = ['maya']
    category = 'geometry'
    version = (0, 1, 0)
    label = 'Mesh Non-Hard Edges'
    actions = [
        pyblish.api.Category("Select Affected"),
        SelectHardEdges,
        pyblish.api.Separator,
    ]

    def process(self, instance):
        """Process all the nodes in the instance 'objectSet'"""
        meshes = cmds.ls(instance, type='mesh', long=True)

        invalid = []
        for mesh in meshes:
            hards = _get_hard_edge(mesh)
            invalid.extend(hards)

        if invalid:
            raise ValueError("Meshes found with non-manifold edges/vertices: {0}".format(invalid))
