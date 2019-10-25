from loguru import logger


class DomainError(RuntimeError):
    def __init__(self, reporter: type = None, message: str = None):
        err = f'(Reporter: {reporter.__qualname__ if reporter else "Unknown"}) '
        if message is None or message is '':
            err += 'An unknown domain error occurred!'
        else:
            err += message

        logger.error(err)
        super().__init__(err)


class DomainValueError(DomainError, ValueError):
    def __init__(self, reporter: type, key: str, value):
        super().__init__(reporter, 'invalid value: "{key}": "{value}"!')


class NoSlackClientDefinedError(DomainError):
    def __init__(self, reporter):
        super().__init__(reporter, 'No valid Slack WebClient defined!')