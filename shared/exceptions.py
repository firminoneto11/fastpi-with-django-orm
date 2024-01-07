from fastapi.exceptions import HTTPException


class EntityNotFoundError(HTTPException):
    http_code = 404

    def __init__(self, detail: str):
        super().__init__(status_code=self.status_code, detail=detail, headers=None)
