import os
import pyblish.api
from pyblish_magenta.project import ProjectEnv

from maya import cmds


class CollectMayaProject(pyblish.api.Collector):
    """Collect project info from current opened scene"""
    label = "Maya project"

    # In order to take advantage of data collected earlier
    order = pyblish.api.Collector.order - 0.1

    def process(self, context):
        if "origin" not in context:
            context.create_instance("origin", family="metadata")

        instance = context["origin"]

        fpath = cmds.file(query=True, expandName=True)
        ProjectEnv.select_project_from_path(fpath)
        os.environ['PROJECT'] = os.environ["PYBLISH_CURRENT_PROJECT_ROOT"]
