from ...client import AuthenticatedClient
from ...models.upload_cell_multipart_data import UploadCellMultipartData


def upload(
    *,
    client: AuthenticatedClient,
    files: UploadCellMultipartData,
    tags: dict = None,
    properties: dict = None,
):
    """Upload cell to BeeYard.

    Parameters
    ----------
    client : AuthenticatedClient
        BeeYard client.
    files : UploadCellMultipartData
        Object containing list of files containing cells to be uploaded.
    tags : list[dict], optional
        List of dictionaries, each containing tags, by default None.
    properties : dict, optional
        Dictionary containing properties, by default None.

    Returns
    -------
    Response
        Http response from API.

    Examples
    --------
    >>> # Tags or properties should be sent as lists:
    >>> additional_tags = [
    >>>    {"beeyard_sdk_test.section_name": "test_name1"},
    >>>    {"beeyard_sdk_test.section_name": "test_name2"},
    >>> ]
    >>> additional_tags={"key1": "value1", "key2": "value2"}
    """
    url = "{}/api/v1/cells?".format(client.base_url)
    if tags is not None:
        url = url + "&" + build_tail(tags, "tags")
    if properties is not None:
        url = url + "&" + build_tail(properties, "properties")
    file_list = files.to_dict()
    response = client.post(url, headers=client.token_headers, files=file_list)
    return response


def build_tail(arg, type):
    url_tail = ""
    if type == "tags":
        for t in arg:
            k = list(t.keys())[0]
            url_tail = url_tail + f"{type}[{k}]={t[k]}&"
    elif type == "properties":
        for key in arg.keys():
            url_tail = url_tail + f"{type}[{key}]={arg[key]}&"
    return url_tail[:-1]
