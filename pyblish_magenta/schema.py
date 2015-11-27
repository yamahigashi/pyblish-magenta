import os
import lucidity
from pyblish_magenta.project import ProjectEnv


def load():
    """Load schema from project `project`

    Schemas are assumed to be located within a /database
    subdirectory of `project`.

    Arguments:
        project (str): Absolute path to project

    """

    path = ProjectEnv.get_current_project()
    schema_path = os.path.join(path, "database", "schema.yaml")
    return lucidity.Schema.from_yaml(schema_path)
