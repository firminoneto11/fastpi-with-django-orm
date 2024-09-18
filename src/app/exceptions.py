from fastapi import HTTPException


class ObjectNotFound(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=404, detail=message)


class ValidationError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=400, detail=message)
