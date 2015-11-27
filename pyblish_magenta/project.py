# -*- coding: utf-8 -*-

import os
import os.path
import anyconfig


class ProjectEnv(object):
    config_path = "database/config.toml"

    @staticmethod
    def _get_projects():
        ps = os.environ['PYBLISH_PROJECTS']
        return ps.split(';')

    @staticmethod
    def _get_directories():
        ps = os.environ['PYBLISH_PROJECT_DIRECTORIES']
        return ps.split(';')

    @classmethod
    def set_projects(cls, projects):
        """ set pyblish projects in os environment variabl.

        \param projects The projects dict. must {'projectA': [directory: ''], 'projectB'...
        """

        os.environ['PYBLISH_PROJECTS'] = ";".join(projects.keys())

        directories = []
        for p in projects.keys():
            directories.append(projects[p]['directory'].replace("\\", "/"))
        os.environ['PYBLISH_PROJECT_DIRECTORIES'] = ";".join(directories)
        assert len(cls._get_projects()) == len(cls._get_directories())

        os.environ.setdefault('PYBLISH_CURRENT_PROJECT_NAME', cls._get_projects()[0])
        os.environ.setdefault('PYBLISH_CURRENT_PROJECT_ROOT', cls._get_directories()[0])

    @classmethod
    def select_project_from_path(cls, some_path):
        for i, p in enumerate(cls._get_directories()):
            if p in some_path.replace("\\", "/"):
                hit_num = i

        os.environ['PYBLISH_CURRENT_PROJECT_NAME'] = cls._get_projects()[hit_num]
        os.environ['PYBLISH_CURRENT_PROJECT_ROOT'] = cls._get_directories()[hit_num]

    @classmethod
    def select_project_from_name(cls, name):
        for i, p in enumerate(cls._get_projects()):
            if p in name:
                hit_num = i
        else:
            raise "project name not found"

        os.environ['PYBLISH_CURRENT_PROJECT_NAME'] = cls._get_projects()[hit_num]
        os.environ['PYBLISH_CURRENT_PROJECT_ROOT'] = cls._get_directories()[hit_num]

    @classmethod
    def get_current_project(cls, ):
        where = os.environ['PYBLISH_CURRENT_PROJECT_ROOT']
        return where

    @classmethod
    def get_config(cls, domain=None):
        conf_path = os.path.abspath(
            os.path.join(cls.get_current_project(), cls.config_path))

        if not os.path.exists(conf_path):
            print "config does not exists in {}".format(conf_path)

        try:
            print conf_path
            conf = anyconfig.load(conf_path, "toml")

            if domain is not None:
                for k in domain.split("."):
                    conf = conf[k]

            return conf

        except Exception as e:
            import traceback
            print traceback.format_exc()

            if "Reserved escape sequence used" in e:
                print u"不正な文字（おそらくパス名にバックスラッシュ）が使用されています".encode('cp932')
                print conf_path

            return None
