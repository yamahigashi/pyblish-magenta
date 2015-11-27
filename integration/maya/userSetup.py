# # -*- coding: utf-8 -*-
# from __future__ import absolute_import

import os
import os.path
import sys

# '''
import maya.mel
import maya.utils
import maya.cmds

from PySide.QtGui import QApplication

try:
    import pyblish_magenta.api
    pyblish_magenta.api.setup()

    import pyblish_magenta.utils.maya.uuid
    pyblish_magenta.utils.maya.uuid.register_callback()

except ImportError as e:
    print "pyblish_magenta: Could not load kit: %s" % e


def set_project():
    """The current working directory is assumed to be the Maya Project"""
    maya_dir = os.path.join(os.getcwd(), "maya")

    if not os.path.exists(maya_dir):
        os.makedirs(os.path.join(maya_dir, "scenes"))

    if os.name == "nt":
        # MEL can't handle backslash
        maya_dir = maya_dir.replace("\\", "/")

    print("Setting development directory to: %s" % maya_dir)
    maya.mel.eval('setProject \"' + maya_dir + '\"')


def distinguish():
    """Distinguish GUI from other projects

    This adds a green line to the top of Maya's GUI

    """

    QApplication.instance().setStyleSheet("""
    QMainWindow > QMenuBar {
      border-bottom: 1px solid lightgreen;
    }
    """)


# set_project()
maya.utils.executeDeferred(distinguish)

#  '''


def search_where_am_i():
    ''' returns where this file located.

    When called from maya, the __file__ is not defined. thus using file structure as for determine.

    '''

    if '__file__' in globals():
        return os.path.abspath(os.path.dirname(__file__))

    for p in sys.path:
        if ("pyblish-magenta" in p) and ("integration" in p):
            return p
    else:
        return None  # not fonud.


def get_conf_path():
    base_path = search_where_am_i()
    conf_path = os.path.abspath(os.path.join(base_path + "/../../conf.toml"))

    return conf_path


def get_magenta_setting():

    conf_path = get_conf_path()
    assert os.path.exists(conf_path)

    import anyconfig
    try:
        conf = anyconfig.load(conf_path, "toml")
        return conf

    except Exception as e:
        import traceback
        print traceback.format_exc()

        if "Reserved escape sequence used" in e:
            print u"不正な文字（おそらくパス名にバックスラッシュ）が使用されています".encode('cp932')
            print conf_path

        return None


def validate_conf(conf):
        if not isinstance(conf, dict):
            return False

        is_valid = True

        if 'project' not in conf or 'work' not in conf:
            print("設定ファイル({})に必要事項がありません".format(get_conf_path()))
            is_valid = False

        if isinstance(conf['project'], list):
            print("設定ファイル({})に[project]欄に必要事項 directory がありません".format(get_conf_path()))
            is_valid = False

        if 'task' not in conf['work']:
            print("設定ファイル({})に[work]欄に必要事項 task がありません".format(get_conf_path()))
            is_valid = False

        return is_valid


def set_envvar_from_conf(conf):
    if validate_conf(conf):
        from pyblish_magenta.project import ProjectEnv
        ProjectEnv.set_projects(conf['project'])
        os.environ['TASK'] = conf['work']['task']
        os.environ['TOPICS'] = conf['work']['task']

        print('setting pyblish current project {0} on "{1}"'.format(
            os.environ['PYBLISH_CURRENT_PROJECT_NAME'],
            os.environ['PYBLISH_CURRENT_PROJECT_ROOT']))


if __name__ == '__main__':
    try:
        conf = get_magenta_setting()
        set_envvar_from_conf(conf)
    except:
        # avoidng the "call userSetup.py chain" accidentally stop, all exception must collapse
        import traceback
        traceback.print_exc()
