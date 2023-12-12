"""Module containing methods for accessing the BeeYard APIs.

The methods of this module can be imported with ``from datavision_beeyard_sdk.api import *``.

Examples
--------
>>> from datavision_beeyard_sdk.api.workspace import read_workspace
>>> ws = read_workspace.read(workspace_id=ws_id, client=client)
>>> json.loads(ws)
    {'workspaceId': 'b662e28a-73c4-403f-bdb2-e2930066bf4d', 'name': 'test', 'namespace': 'test',
    'created': '2023-08-11T10:34:05.703Z', 'modified': '2023-08-11T10:46:56.247Z', 'version': 8,
    'schemaVersion': '1', 'tagTemplates': [{'section': 'anomaly', 'name': 'anomalia'},
    {'section': 'class', 'name': 'anomalia'}, {'section': 'class', 'name': 'buone'},
    {'section': 'dataset', 'name': 'test'},
    {'section': 'task', 'name': 'anomaly_detection'}, {'section': 'util', 'name': 'csv'}],
    'shapeTemplates': [], 'favoriteQueries': [], 'favoriteAggregations': [], 'tagCategoryRules': []}
"""
