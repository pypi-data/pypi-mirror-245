from pydantic import BaseModel


class InitArg(BaseModel):
    version: str
    type: str
    body: dict

