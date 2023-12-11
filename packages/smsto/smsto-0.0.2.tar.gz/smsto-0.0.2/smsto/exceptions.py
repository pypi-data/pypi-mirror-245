from requests import Response


class BadRequest(Exception):
    def __init__(self, msg=None, resp=None):
        self.message = msg
        self.response: Response | None = resp
        super().__init__(self.message)
        
        
class APINotImplemented(Exception):
    def __init__(self):
        super().__init__('This method is not implemented yet')