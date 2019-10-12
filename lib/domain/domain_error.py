from loguru import logger


class DomainError(RuntimeError):
    def __init__(self, message):
        if message is None or message is '':
            message = 'An unknown domain error occurred :('
        logger.error(message)
        super().__init__(message)
