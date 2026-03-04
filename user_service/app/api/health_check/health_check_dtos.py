from pydantic import BaseModel


class ResponseHealthCheckDTO(BaseModel):
    status: str
