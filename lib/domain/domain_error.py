from loguru import logger


class DomainError(RuntimeError):
    def __init__(self, reporter: type = None, message: str = None):
        self.reporter = reporter

        err = ''
        if not message:
            err += 'An unknown domain error occurred!'
        else:
            err += message

        logger.error(f'(Reporter: {reporter.__qualname__ if reporter else "Unknown"}) {err})')
        super().__init__(err)


class DomainValueError(DomainError, ValueError):
    def __init__(self, reporter: type, key: str, value):
        super().__init__(reporter, f'invalid value: "{key}": "{value}"!')


class NoSlackClientDefinedError(DomainError):
    def __init__(self, reporter):
        super().__init__(reporter, 'No valid Slack WebClient defined!')
