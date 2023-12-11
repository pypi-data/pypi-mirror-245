"""This module defines enums related to Koordinates."""

from enum import Enum


class PublisherAcronym(Enum):
    """Enum class for publisher acronyms."""

    LINZ: str = "LINZ"
    LRIS: str = "LRIS"


class Publisher(Enum):
    """Enum class for publishers."""

    LINZ = {
        "name": "Land Information New Zealand",
        "domain": "data.linz.govt.nz",
    }
    LRIS = {
        "name": "Manaaki Whenua - Landcare Research",
        "domain": "lris.scinfo.org.nz",
    }


class ExportFormats(Enum):
    """Enum class for export formats."""

    GRID = "image/tiff;subtype=geotiff"
    VECTOR = "application/x-ogc-gpkg"
