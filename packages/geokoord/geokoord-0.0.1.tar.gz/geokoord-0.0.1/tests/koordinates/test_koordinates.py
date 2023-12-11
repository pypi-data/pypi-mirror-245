import os

import pytest
from dotenv import load_dotenv
from geokoord.enums import PublisherAcronym
from geokoord.koordinates import Koordinates

load_dotenv()

LINZ_KEY = os.getenv("LINZ_KEY")


class TestKoordinates:
    def test_null_publisher(self):
        """Test case for handling null publisher."""
        with pytest.raises(ValueError):
            Koordinates(None, LINZ_KEY)

    def test_invalid_publisher(self):
        """Test case for handling invalid publisher."""
        with pytest.raises(ValueError):
            Koordinates("invalid", LINZ_KEY)

    def test_null_key(self):
        """Test case for handling null key."""
        with pytest.raises(AssertionError):
            Koordinates(PublisherAcronym.LINZ, None)


class TestConfDefaults:
    def test_crs(self, linz):
        """Test case for handling null CRS."""
        assert linz.crs == "EPSG:2193"

    def test_key(self, linz):
        """Test case for handling null key."""
        assert linz.api_key == LINZ_KEY

    def test_extent(self, linz):
        """Test case for handling null extent."""
        assert isinstance(linz.extent, dict)
