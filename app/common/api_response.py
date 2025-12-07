class APIResponse:
    def __init__(self, success: bool, data=None, message: str = "", status_code: int = 200):
        self.success = success
        self.data = data
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {
            "success": self.success,
            "data": self.data,
            "message": self.message,
            "status_code": self.status_code,
        }