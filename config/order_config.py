from config.config_parser import TacoTuesdayConfigParser


class TacoTuesdayOrderConfig(TacoTuesdayConfigParser):
    TaxRate: float = None
    MaxSingleTaco: int = None
    TaqueriaAddress: str = None
    TaqueriaPhoneNumber: str = None

    def __init__(self):
        config = TacoTuesdayConfigParser.get_config('order')

        TacoTuesdayOrderConfig.TaxRate = config['taxRate']
        TacoTuesdayOrderConfig.MaxSingleTaco = config['maxSingleTaco']
        TacoTuesdayOrderConfig.TaqueriaAddress = config['taqueriaAddress']
        TacoTuesdayOrderConfig.TaqueriaPhoneNumber = config['taqueriaPhoneNumber']

    def get_tax_rate(self):
        return self.TaxRate

    def get_max_single_taco(self):
        return self.MaxSingleTaco

    def get_taqueria_address(self):
        return self.TaqueriaAddress

    def get_taqueria_phone_number(self):
        return self.TaqueriaPhoneNumber
