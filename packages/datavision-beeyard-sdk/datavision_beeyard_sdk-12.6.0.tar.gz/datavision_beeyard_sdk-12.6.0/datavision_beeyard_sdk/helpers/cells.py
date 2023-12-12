from datavision_beeyard_sdk.api.file import read_file
from datavision_beeyard_sdk.api.cell import read_cell
import json
from datavision_beeyard_sdk.api.overlay import add_overlays
from datavision_beeyard_sdk.models.add_documents_multipart_data import (
    AddDocumentsMultipartData,
)

from datavision_beeyard_sdk.types import File


def get_images(cell_id, client):
    """Get all images from a cell.

    This method will download all images present inside the BeeYard cell.

    Parameters
    ----------
    cell_id : str
        The BeeYard cell id where images are stored.
    client : AuthenticatedClient
        The BeeYard client used to connect to the platform.

    Returns
    -------
    list[bytes]
        The list of images. Each image is byte encoded.
        The list is empty if no image is present inside the cell.

    """
    cell_descriptor = read_cell.read(id=cell_id, client=client)
    files = [
        i.get("name")
        for i in cell_descriptor.get("files")
        if i.get("dataType") == "image"
    ]
    images = [
        read_file.read(id=cell_id, filename=file_name, client=client)
        for file_name in files
    ]
    return images


def get_annotations(overlays_json, annotation_type=None):
    """Get all annotations from an overlay.

    This methods get all annotations of a given type from a BeeYard cell.
    If the type is not specified, then all annotations will be returned.

    Parameters
    ----------
    overlays_json : json str
        A json string containing the overlay dictionary.
    annotation_type : str, optional
        The annotation type to retrive from the overlay, by default None.

    Returns
    -------
    list[dict]
        List of shapes. Each shape is a dictionary.

    Raises
    ------
    Exception
        If annotation type is not found in overlay.
    """
    overlays = json.loads(overlays_json)
    shapes = []
    if annotation_type is None:
        for overlay in overlays:
            for layer in overlay.get("overlay").get("layers"):
                for shape in layer.get("shapes"):
                    shapes.append(shape)
    else:
        for overlay in overlays:
            for layer in overlay.get("overlay").get("layers"):
                for shape in layer.get("shapes"):
                    if shape.get("typeName") == annotation_type:
                        shapes.append(shape)
        if len(shapes) == 0:
            raise Exception(f"Annotation type {annotation_type} not found in cell.")
    return shapes


def add_empty_overlay(client, cell_id, name="empty.shp"):
    """Add an empty overlay.

    The name can be specified.

    Parameters
    ----------
    client : AuthenticatedClient
        BeeYard client.
    cell_id : str
        The BeeYard cell id.
    name : str, optional
        Name of the empty overlay, by default "empty.shp"

    Returns
    -------
    Response
        Http response from API.
    """
    overlay_file = File(payload="{}", file_name=name)
    overlay_to_upload = AddDocumentsMultipartData([overlay_file])
    return add_overlays.add(id=cell_id, client=client, multipart_data=overlay_to_upload)
