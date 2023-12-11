import os

import pytest
from dotenv import load_dotenv
from geokoord.koordinates import Koordinates

load_dotenv()


@pytest.fixture
def linz_key():
    """Return a LINZ API key."""
    return os.getenv("LINZ_KEY")


@pytest.fixture
def lris_key():
    """Return a LRIS API key."""
    return os.getenv("LRIS_KEY")


@pytest.fixture
def export_extent():
    """Return an export extent."""
    return dict(
        {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [171.16246499506227, -43.48277735711678],
                        [171.16246499506227, -43.46645012482622],
                        [171.19660781041435, -43.46645012482622],
                        [171.19660781041435, -43.48277735711678],
                        [171.16246499506227, -43.48277735711678],
                    ]
                ]
            ],
        }
    )


@pytest.fixture
def linz(linz_key, export_extent):
    """Return a Koordinates object."""
    return Koordinates(
        "LINZ",
        linz_key,
        extent=export_extent,
    )


@pytest.fixture
def lris(lris_key, export_extent):
    """Return a Koordinates object."""
    return Koordinates(
        "LRIS",
        lris_key,
        extent=export_extent,
    )


@pytest.fixture
def vector_id():
    """Return a vector layer ID."""
    return 50768


@pytest.fixture
def raster_id():
    """Return a raster layer ID."""
    return 51768
