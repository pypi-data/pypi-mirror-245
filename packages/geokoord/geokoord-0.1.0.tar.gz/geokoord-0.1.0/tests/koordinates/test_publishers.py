import os

from dotenv import load_dotenv
from geokoord.koordinates import Koordinates

load_dotenv()

LINZ_KEY = os.getenv("LINZ_KEY")
LRIS_KEY = os.getenv("LRIS_KEY")


class TestLINZPublisher:
    linz = Koordinates("LINZ", LINZ_KEY)

    def test_publisher_name(self):
        """Test case for checking the publisher name."""
        assert self.linz.publisher_name == "Land Information New Zealand"

    def test_domain(self):
        """Test case for checking the domain."""
        assert self.linz.domain == "data.linz.govt.nz"


class TestLRISPublisher:
    lris = Koordinates("LRIS", LRIS_KEY)

    def test_publisher_name(self):
        """Test case for checking the publisher name."""
        assert self.lris.publisher_name == "Manaaki Whenua - Landcare Research"

    def test_domain(self):
        """Test case for checking the domain."""
        assert self.lris.domain == "lris.scinfo.org.nz"
