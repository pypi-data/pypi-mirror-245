from ...client import AuthenticatedClient
import json


def search(
    *,
    client: AuthenticatedClient,
    query="",
    sort_by="created",
    sort_direction="asc",
    page_index=0,
    page_size=100
):
    """Execute a query on all workspaces.

    Parameters
    ----------
    client : AuthenticatedClient
        BeeYard client.
    query : str, optional
        MongoDB query, by default ""
    sort_by : {'created', 'modified', 'name', 'namespace'}, optional
        Sort results, by default "created"
    sort_direction : {'asc', 'desc'}, optional
        Sort results order, by default "asc"
    page_index : int, optional
        Start from given page result, by default 0
    page_size : int, optional
        Number of result per page, by default 100

    Returns
    -------
    dict
        Results of the query.
    """
    url = "{}/api/v1/workspaces/search".format(client.base_url)
    url_with_param = (
        url
        + "?sortBy="
        + sort_by
        + "&sortDirection="
        + sort_direction
        + "&pageIndex="
        + str(page_index)
        + "&pageSize="
        + str(page_size)
    )
    response = client.post(url_with_param, headers=client.token_headers, data=query)
    return json.loads(response.content.decode("utf-8"))
