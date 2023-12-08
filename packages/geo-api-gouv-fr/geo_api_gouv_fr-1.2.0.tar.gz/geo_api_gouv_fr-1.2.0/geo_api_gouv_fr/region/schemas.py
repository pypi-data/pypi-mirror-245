from pydantic import BaseModel, validator
from typing import Optional


class RegionsParams(BaseModel):
    """
    Attributes:
        nom:
        code:
        limit:
    """

    nom: Optional[str]
    code: Optional[str]
    limit: Optional[int]


class RegionCodeParams(BaseModel):
    """
    Attributes:
        code:
        limit:
    """

    code: Optional[str]
    limit: Optional[int]

    @validator("code")
    def code_must_be_2(cls, v):
        if len(v) == 1:
            v = "0" + v
        return v


class RegionsResponse(BaseModel):
    """
    Attributes:
        nom:
        code:
        _score:
    """

    nom: str
    code: int
    _score: Optional[float]
