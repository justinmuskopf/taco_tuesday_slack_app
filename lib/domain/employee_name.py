from loguru import logger


class EmployeeNameError(RuntimeError):
    def __init__(self, first_name='', last_name=''):
        if first_name and last_name:
            logger.error("Error in name: " + first_name, last_name)
        elif first_name and not last_name:
            logger.error("Error in first name: " + first_name)
        elif last_name and not first_name:
            logger.error("Error in last name: " + last_name)


class EmployeeName:
    def __init__(self, first_name: str, last_name: str, nick_name=''):
        if first_name and last_name:
            self.first_name = first_name
            self.last_name = last_name
        else:
            raise EmployeeNameError(first_name, last_name)

        if nick_name:
            self.nick_name = nick_name
