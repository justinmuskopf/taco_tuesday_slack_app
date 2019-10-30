from config.config_parser import TacoTuesdayConfigParser


class TacoTuesdayOrderConfig(TacoTuesdayConfigParser):
    TaxRate: float = None
    MaxSingleTaco: int = None

    def __init__(self):
        config = TacoTuesdayConfigParser.get_config('order')

        TacoTuesdayOrderConfig.TaxRate = config['taxRate']
        TacoTuesdayOrderConfig.MaxSingleTaco = config['maxSingleTaco']

    def get_tax_rate(self):
        return self.TaxRate

    def get_max_single_taco(self):
        return self.MaxSingleTaco
