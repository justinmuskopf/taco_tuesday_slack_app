from lib.domain.employee_name_error import EmployeeNameError


class Name:
    def __init__(self, first_name: str, last_name: str, nick_name=''):

        if first_name and last_name:
            self.first_name = first_name
            self.last_name = last_name
        else:
            raise EmployeeNameError()

        if nick_name:
            self.nick_name = nick_name
