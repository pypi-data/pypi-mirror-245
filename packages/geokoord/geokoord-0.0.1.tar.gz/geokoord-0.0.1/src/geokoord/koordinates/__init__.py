"""This module provides the Koordinates class for interacting with the Koordinates API: https://apidocs.koordinates.com."""

from pathlib import Path

from geokoord.enums import Publisher, PublisherAcronym


class Koordinates:
    """The Koordinates class represents an object for interacting with the Koordinates API.

    Attributes:
        publisher (str | PublisherAcronym): The publisher to interact with.
        api_key (str): Your Koordinates API key.
        crs (int, optional): The coordinate reference system. Defaults to 2193.
        api_version (str): The API version.
        publisher_name (str): The name of the publisher.
        domain (str): The domain of the publisher.
        _headers (dict): The headers for API requests.
    """

    # Imported methods
    from .exports import create_export, download_layer, get_export, get_exports

    def __init__(
        self,
        publisher: str | PublisherAcronym,
        api_key: str,
        extent: dict = None,
        crs: int = 2193,
        download_dir: Path | str = None,
    ):
        """Initialize the Koordinates object.

        Args:
            publisher (str | PublisherAcronym): The publisher to interact with.
            api_key (str): Your Koordinates API key.
            extent (dict, optional): The extent of the export. Defaults to None.
            crs (int, optional): The coordinate reference system. Defaults to 2193.
            download_dir (Path | str, optional): The directory to download files to. Defaults to None.
        """
        self.publisher = PublisherAcronym(publisher)
        self.api_key = api_key
        self.extent = extent
        self.crs = f"EPSG:{crs}"
        self.download_dir = Path(download_dir) if download_dir else None

        self.api_version = "1.x"

        assert self.api_key is not None, "API key cannot be null"

        self.publisher_name = Publisher[self.publisher.name].value["name"]
        self.domain = Publisher[self.publisher.name].value["domain"]

        self._headers = {"Authorization": f"key {self.api_key}"}

        if self.download_dir:
            self.download_dir.mkdir(parents=True, exist_ok=True)

    def __repr__(self):
        """Return a string representation of the Koordinates object."""
        return f"<Koordinates publisher={self.publisher.value} api_key={self.api_key}>"

    def __str__(self):
        """Return a string representation of the Koordinates object."""
        return f"{self.publisher_name} ({self.publisher.name})"
