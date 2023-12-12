import json


def create(client, namespace=None, additional_tags=None, additional_properties=None):
    """_summary_

    Parameters
    ----------
    client : AuthenticatedClient
        BeeYard client.
    namespace : str, optional
        Target namespace, by default None.
    additional_tags : list[dict], optional
        Dictionary containing tags, by default None.
    additional_properties : dict, optional
        Dictionary containing properties, by default None.

    Returns
    -------
    dict
        Dictionary describing the cell.

    Examples
    --------
    >>> # Tags or properties should be sent as lists:
    >>> additional_tags = [
    >>>    {"beeyard_sdk_test.section_name": "test_name1"},
    >>>    {"beeyard_sdk_test.section_name": "test_name2"},
    >>> ]
    >>> additional_tags={"key1": "value1", "key2": "value2"}
    """
    if namespace is not None:
        url = client.base_url + "/api/v1/cells/new?namespace=" + namespace
        if additional_tags is not None:
            url = url + "&" + build_tail(additional_tags, "tags")
        if additional_properties is not None:
            url = url + "&" + build_tail(additional_properties, "properties")
    else:
        url = client.base_url + "/api/v1/cells/new"
        if additional_tags is not None:
            url = url + "?" + build_tail(additional_tags, "tags")
        if additional_properties is not None:
            url = url + "?" + build_tail(additional_properties, "properties")
    response = client.post(url, headers=client.token_headers)
    return json.loads(response.content)


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
