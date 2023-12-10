class SklikException(Exception):
    def __init__(self, msg, status_code, additional_information):
        self.status_code = status_code
        self.additional_information = additional_information
        super().__init__(msg)
