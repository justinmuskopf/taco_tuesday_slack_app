import os

import yaml


class ConfigParserError(ValueError):
    def __init__(self, key, none=True):
        if none:
            super().__init__(f'No "{key}" found in configuration!')
        else:
            super().__init__(f'Invalid "{key}" value found in configuration!')


class TacoTuesdayConfigParser:
    Yaml = None

    @staticmethod
    def parse():
        config_file = os.environ['TT_SLACK_CONFIG_FILE']

        content = open(config_file).read()
        TacoTuesdayConfigParser.Yaml = yaml.load(content)

    @classmethod
    def get_config(cls, config: str):
        if TacoTuesdayConfigParser.Yaml is None:
            cls.parse()

        if config not in TacoTuesdayConfigParser.Yaml:
            raise ConfigParserError(config)

        return TacoTuesdayConfigParser.Yaml[config]
