from pydantic import BaseModel, validator
from typing import Optional, List


class DepartmentsParams(BaseModel):
    """
    Attributes:
        nom:
        codeRegion:
        code:
        limit:
        fields:

    """

    nom: Optional[str]
    codeRegion: Optional[str]
    code: Optional[str]
    limit: Optional[int]
    fields: Optional[List[str]]

    @validator("code")
    def code_must_be_2(cls, v):
        if len(v) == 1:
            v = "0" + v
        return v

    @validator("codeRegion")
    def codeRegion_must_be_2(cls, v):
        if len(v) == 1:
            v = "0" + v
        return v


class DepartmentCodeParams(BaseModel):
    """
    Attributes:
        code:
        limit:
        fields:
    """

    code: Optional[str]
    fields: Optional[list]
    limit: Optional[int]

    @validator("code")
    def code_must_be_2(cls, v):
        if len(v) == 1:
            v = "0" + v
        return v


class RegionDepartmentCodeParams(BaseModel):
    """
    Attributes:
        regioncode:
        limit:
    """

    code: Optional[str]
    limit: Optional[int]

    @validator("code")
    def code_must_be_2(cls, v):
        if len(v) == 1:
            v = "0" + v
        return v


class DepartmentsResponse(BaseModel):
    """
    Attributes:
        nom:
        code:
        codeRegion: int
        fields:
        _score:
    """

    nom: str
    code: int
    codeRegion: int
    fields: Optional[list]
    _score: Optional[float]
