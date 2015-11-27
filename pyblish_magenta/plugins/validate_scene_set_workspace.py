import os.path

import pyblish.api
import maya.cmds as cmds

# from pyblish_magenta.utils.path import is_subdir


def in_directory(file, directory, allow_symlink=False):

    # make both absolute
    directory = os.path.abspath(directory)
    file = os.path.abspath(file)

    # check whether file is a symbolic link, if yes, return false if they are not allowed
    if not allow_symlink and os.path.islink(file):
        return False

    # return true, if the common prefix of both is equal to directory
    # e.g. /a/b/c/d.rst and directory is /a/b, the common prefix is /a/b
    return os.path.commonprefix([file, directory]) == directory


class ValidateSceneSetWorkspace(pyblish.api.Validator):
    """Validate the scene is inside the currently set Maya workspace"""

    families = ['model']
    hosts = ['maya']
    category = 'scene'
    version = (0, 1, 0)
    label = 'Maya Workspace Set'

    def process(self, context):
        scene_name = cmds.file(q=1, sceneName=True)
        root_dir = cmds.workspace(q=1, rootDirectory=True)

        if not in_directory(scene_name, root_dir):
            raise RuntimeError("Maya workspace is not set correctly.")
