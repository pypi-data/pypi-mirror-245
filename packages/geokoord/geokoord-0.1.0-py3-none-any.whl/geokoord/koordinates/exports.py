"""Methods related to using the Exports API: https://apidocs.koordinates.com/#tag/Exports."""
import time
from pathlib import Path
from zipfile import ZipFile

import requests
from requests.exceptions import HTTPError
from tqdm import tqdm

from geokoord.enums import ExportFormats


def get_exports(self) -> list[dict]:
    """Get the exports from the API.

    Args:
        self (Koordinates): The Koordinates object.

    Returns:
        list: The exports data.
    """
    url = f"https://{self.domain}/services/api/v{self.api_version}/exports/"

    with requests.get(url, headers=self._headers) as response:
        return response.json()


def get_export(self, export_id: int) -> dict:
    """Get an export from the API.

    Args:
        self (Koordinates): The Koordinates object.
        export_id (int): The ID of the export.

    Returns:
        dict: The export data.
    """
    url = f"https://{self.domain}/services/api/v{self.api_version}/exports/{export_id}/"

    with requests.get(url, headers=self._headers) as response:
        response.raise_for_status()
        return response.json()


def _validate_export(url: str, headers: dict, data: dict) -> bool | list[str]:
    url = url + "validate/"
    with requests.post(url, headers=headers, json=data) as response:
        if response.status_code == 400:
            raise HTTPError(response.json()["errors"])
        return response.json()["is_valid"], response.json()["invalid_reasons"]


def create_export(
    self,
    layer_id: int,
    format: ExportFormats = "GRID",
    extent: dict = None,
    tiles: list[str] = None,
) -> dict:
    """Create an export.

    Args:
        self (Koordinates): The Koordinates object.
        layer_id (int): The ID of the layer to export.
        format (ExportFormats, optional): The format of the export. Defaults to ExportFormats.GRID.
        extent (dict, optional): The extent of the export. Defaults to None.
        tiles (list, optional): The tiles of the export. Defaults to None.

    Returns:
        dict: The export data.
    """
    url = f"https://{self.domain}/services/api/v{self.api_version}/exports/"

    data = {
        "crs": self.crs,
        "items": [
            {
                "item": f"https://{self.domain}/services/api/v{self.api_version}/layers/{layer_id}/",
            }
        ],
        "delivery": {"method": "download"},
    }

    if format == "GRID":
        data["formats"] = {"grid": ExportFormats.GRID.value}
    elif format == "VECTOR":
        data["formats"] = {"vector": ExportFormats.VECTOR.value}

    if extent:
        data["extent"] = extent

    if tiles:
        data["items"][0]["tiles"] = tiles

    valid, reasons = _validate_export(url, self._headers, data)

    if valid:
        with requests.post(url, headers=self._headers, json=data) as response:
            response.raise_for_status()
            return response.json()
    else:  # TODO: update this with chunked export
        raise ValueError(reasons)


def download_layer(
    self,
    layer_id: int,
    format: ExportFormats = "GRID",
) -> Path:
    """Download a layer.

    Args:
        self (Koordinates): The Koordinates object.
        layer_id (int): The ID of the layer to export.
        format (ExportFormats, optional): The format of the export. Defaults to ExportFormats.GRID.

    Returns:
        Path: The path to the downloaded file.
    """
    # create an export
    export_params = create_export(self, layer_id, format=format, extent=self.extent)

    # wait for export to finish
    _wait_for_export(self, export_params["id"])

    # download export
    zip_path = _download_export(self, export_params["id"])

    # extract and delete export
    download_path = _extract_zip(zip_path)
    return download_path


def _wait_for_export(self, export_id: int):
    with tqdm(
        total=1.0,
        desc="Generating export",
        bar_format="{l_bar}{bar}| {elapsed}<{remaining}",
    ) as pbar:
        while True:
            export = get_export(self, export_id)
            export_state = export["state"]
            if export_state == "complete":
                pbar.update(1 - pbar.n)
                break
            elif export_state == "processing":
                progress = export["progress"]
                pbar.update(progress - pbar.n)
                time.sleep(1)
            else:
                raise ValueError(f"export state '{export_state}' not recognised")


def _download_export(self, export_id: int):
    assert self.download_dir is not None, "download_dir cannot be None"

    export = get_export(self, export_id)
    export_url = export["download_url"]

    r = requests.get(export_url, headers=self._headers, stream=True)
    r.raise_for_status()

    zip_filename = export["name"] + ".zip"
    zip_path = self.download_dir / zip_filename

    total_size = int(r.headers.get("content-length", 0))
    block_size = 1024

    with open(zip_path, "wb") as f:
        tqdm_params = {
            "desc": "Downloading export",
            "total": total_size,
            "unit": "B",
            "unit_scale": True,
            "unit_divisor": block_size,
        }
        with tqdm(**tqdm_params) as pbar:
            for chunk in r.iter_content(block_size):
                f.write(chunk)
                pbar.update(len(chunk))

    return zip_path


def _extract_zip(zip_path: Path):
    folder_name = zip_path.parent / zip_path.stem

    with ZipFile(zip_path) as zip_object:
        tqdm_params = {
            "desc": "Extracting download",
            "total": len(zip_object.infolist()),
        }
        for file in tqdm(zip_object.infolist(), **tqdm_params):
            zip_object.extract(file, folder_name)
    zip_path.unlink()

    return folder_name
