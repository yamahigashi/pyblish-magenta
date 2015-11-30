# -*- coding: utf-8 -*-

import os
import pyblish.api
import pyblish_maya

import lucidity
import pyblish_magenta.schema
from pyblish_magenta.project import ProjectEnv


@pyblish.api.log
class CollectModel(pyblish.api.Collector):
    """ context へシーン中のモデルを全て注入する. """

    config_key = "modeling"

    def process(self, context):
        from maya import cmds

        schema = pyblish_magenta.schema.load()
        tester = schema.get_template("test_asset")
        fpath = cmds.file(query=True, expandName=True)
        fpath.replace("\\", "/")
        holders = tester.parse(fpath)
        model_name = holders['asset'].split('.')[0]

        if "modeling" not in os.environ["TASK"].split(','):
            return self.log.info("No model found")

        if 'genre' not in holders:
            self.log.info("No genre found")
        elif "model" not in holders['genre']:
            self.log.info("Asset's genre not modeling")

        name = model_name  # holders['container']
        os.environ['ITEM'] =  holders['container']

        # Get the root transform
        self.log.info("Model found: %s" % name)
        pattern = ProjectEnv.get_config(self.config_key)['root_node_name_pattern']
        assembly = pattern.format(name=name)

        assert cmds.objExists(assembly), (
            "Model did not have an appropriate assembly: %s" % assembly)

        self.log.info("Capturing instance contents: %s" % assembly)
        with pyblish_maya.maintained_selection():
            cmds.select(assembly)
            nodes = cmds.file(exportSelected=True,
                              preview=True,
                              constructionHistory=False,
                              force=True,
                              shader=False,
                              channels=False,
                              expressions=False,
                              constraints=False)
            nodes = cmds.ls(nodes, long=True)

        self.log.info("Reducing nodes to shapes only")
        shapes = cmds.ls(nodes,
                         noIntermediate=True,
                         exactType="mesh",
                         long=True,
                         dag=True)

        assert shapes, "Model did not have any shapes"

        instance = context.create_instance(name=name, family="model")
        instance[:] = nodes

        self.log.info("Successfully collected %s" % name)
