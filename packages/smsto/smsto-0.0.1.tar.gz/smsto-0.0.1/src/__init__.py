from .sms import SMS


class SMSTo:
    def __init__(self, token: str):
        self._token = token
        self.SMS = SMS(self._token)