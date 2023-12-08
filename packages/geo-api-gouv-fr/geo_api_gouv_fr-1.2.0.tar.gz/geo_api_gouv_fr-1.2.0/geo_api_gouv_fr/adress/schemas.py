from pydantic import BaseModel, validator
from typing import List, Optional


class SearchParams(BaseModel):
    """
    Attributes:
        q:
        limit:
        autocomplete:
        type:
        postcode:
        lat:
        lon:

    """
    q: Optional[str]
    limit: Optional[int]
    autocomplete: Optional[int]
    type: Optional[str]
    postcode: Optional[str]
    citycode: Optional[str]
    lat: Optional[float]
    lon: Optional[float]

    @validator('q')
    def add_smaller_than_200(cls, v):
        """Validator for query to be smaller than 200 characters
        """
        return v[:200]

    @validator('type')
    def type_must_be_in(cls, v):
        """Validator for type

        Rules:
            Must be part of:
                - housenumber
                - street
                - locality
                - municipality

        Raises:
            ValueError:
        """
        values = ["housenumber", "street", "locality", "municipality"]
        if v not in values:
            raise ValueError(f"Type value must be in {values}")
        return v


class SearchCSVParams(BaseModel):
    """
    Attributes:
        columns:
        result_columns:
        postcode:
        citycode:
    """
    columns: Optional[List[str]]
    result_columns: Optional[List[str]]
    postcode: Optional[str] = ""
    citycode: Optional[str] = ""


class ReverseParams(BaseModel):
    """
    Attributes:
        lat:
        lon:
        type:
        limit:
    """
    lat: float
    lon: float
    type: Optional[str]
    limit: Optional[int]


# results ( everything optional in order to avoid mistakes)

class GpsCoordinate(BaseModel):
    """
    Attributes:
        latitude:
        longitude:
    """
    latitude: float
    longitude: float


class Geometry(BaseModel):
    """
    Attributes:
        type:
        coordinates:
    """
    type: Optional[str]
    coordinates: Optional[List]

    @validator('coordinates')
    def coord_must_have_lat_lon(cls, v):
        """Validator for coordinates

        Rules:
            - Coordinates muse have latitude & longitude
            - Latitude value must be in [-180, 180]
            - Longitude value must be in [-90, 90]

        Raises:
            ValueError:
        """
        if len(v) != 2:
            raise ValueError("Coordinates muse have latitude & longitude")

        if v[0] > 180 or v[0] < -180:
            raise ValueError("Latitude value must be in [-180, 180]")

        if v[1] > 90 or v[1] < -90:
            raise ValueError("Longitude value must be in [-90, 90]")

        return v


class Properties(BaseModel):
    """Properties of search result

    Attributes:
        label:
        score:
        housenumber:
        id:
        type:
        name:
        postcode:
        citycode:
        x:
        y:
        city:
        context:
        importance:
        street:
        population:

    """
    label: Optional[str]
    score: Optional[float]
    housenumber: Optional[str]
    id: Optional[str]
    type: Optional[str]
    name: Optional[str]
    postcode: Optional[str]
    citycode: Optional[str]
    x: Optional[float]
    y: Optional[float]
    city: Optional[str]
    context: Optional[str]
    importance: Optional[float]
    street: Optional[str]
    population: Optional[int]


class AddressFeature(BaseModel):
    """Properties of search result

    Attributes:
        geometry:
        properties:

    """
    geometry: Optional[Geometry]
    properties: Optional[Properties]

    def get_coords(self):
        """Get GpsCoordinate from geometry

        Returns:
            (GpsCoordinate):
        """
        return GpsCoordinate(latitude=self.geometry.coordinates[0], longitude=self.geometry.coordinates[1])


class ReverseResponse(BaseModel):
    """Properties of /reverse/ result

    Attributes:
        type:
        version:
        features:
    """
    type: str
    version: str
    features: List[AddressFeature]


class SearchResponse(ReverseResponse):
    """Properties of /search/ result

    Attributes:
        type:
        version:
        features:
    """
    pass
