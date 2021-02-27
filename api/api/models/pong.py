"""
Response from a ping
"""

from pydantic import BaseModel


class Pong(BaseModel):
    result: str

    class Config:
        schema_extra = {
            "example": {
                "result": "pong",
            }
        }
