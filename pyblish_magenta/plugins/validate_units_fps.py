import pyblish.api
from pyblish_mgenta.project import ProjectEnv


@pyblish.api.log
class ValidateUnitsFps(pyblish.api.Validator):
    """Validate the scene linear, angular and time units."""
    label = "Units (fps)"
    families = ["rig", "model", "pointcache", "curves"]
    config_key = "unit"

    def process(self, context):
        fps = context.data('fps')

        self.log.info('Units (time): {0} FPS'.format(fps))
        conf = ProjectEnv.get_config(self.config_key)
        assert fps and fps == conf['fps'], "Scene must be {0} FPS".format(conf['fps']
