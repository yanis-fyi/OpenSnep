from pydantic import BaseModel, Field
from datetime import date
from enum import Enum



class CertificationResponse(BaseModel):
    interprete: str = Field(alias="artist")
    titre: str = Field(alias="title")
    editeur_distributeur: str | None = Field(alias="label_distributor")
    certification: str
    categorie: str = Field(alias="category")
    date_sortie: date = Field(alias="release_date")
    date_constat: date = Field(alias="certification_date")
    source_year: int = Field(alias="year")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


class ChartEntryResponse(BaseModel):
    chart_name: str
    rank: int
    artist: str
    title: str
    label_distributor: str
    week: int
    year: int

    model_config = {
        "from_attributes": True
    }


class CountResponse(BaseModel):
        count: int

class ArtistCountResponse(BaseModel):
     artist: str
     count: int

class LabelCountResponse(BaseModel):
     label_distributor: str
     count: int

class CategoryCountResponse(BaseModel):
    category: str
    count: int

class YearCountResponse(BaseModel):
    year: int
    count: int

class CertificationLevelResponse(BaseModel):
    certification: str
    count: int

class NumberOneEntriesResponse(BaseModel):
     artist: str
     chart_name: str | None
     weeks_at_number_one: int

class ChartName(str, Enum):
    top_albums = "Top Albums"
    top_singles = "Top Singles"
    top_albums_classique = "Top Albums Classique"
    top_albums_jazz = "Top Albums Jazz"
    top_rock_metal = "Top Rock & Metal"
    top_albums_physiques = "Top Albums Physiques"
    top_radio = "Top Radio"

class CategoryName(str, Enum):
     singles = "Singles"
     albums = "Albums"