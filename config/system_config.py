from os.path import isdir

from config.config_parser import TacoTuesdayConfigParser, ConfigParserError


class TacoTuesdaySystemConfig(TacoTuesdayConfigParser):
    LogDir: str = None

    def __init__(self):
        config = super().get_config('system')

        TacoTuesdaySystemConfig.LogDir = config['logDir']

    def get_log_dir(self):
        if not isdir(self.LogDir):
            raise ConfigParserError('logDir')

        return self.LogDir
