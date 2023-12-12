"""Contains all the data models used in inputs/outputs.

Models can be imported with ``from datavision_beeyard_sdk.models import *``.

Examples
--------
>>> from datavision_beeyard_sdk.models import AddImagesMultipartData
>>> f = File(payload=data, file_name="test.png", mime_type="image/png")
>>> AddImagesMultipartData([f])
    AddImagesMultipartData(files=[File(payload=b'\x89PNG\r\n\x1a\
    [...]
    02\x10=jo\xec\x00\x00\x00\x00IEND\xaeB`\x82', file_name='test.png',
    mime_type='image/png')], additional_properties={})
"""

from .workspace_descriptor_dto import WorkspaceDescriptorDto
from .modify_cell_input_dto import ModifyCellInputDto
from .add_images_multipart_data import AddImagesMultipartData
from .add_documents_multipart_data import AddDocumentsMultipartData
from .tag_dto import TagDto
from .property_dto import PropertyDto
from .tag_template_dto import TagTemplateDto
from .update_tags_dto import UpdateTagsDto
from .upload_mask_multipart_data import UploadMaskMultipartData
from .add_files_multipart_data import AddFilesMultipartData
from .filter import Filter
from .reference_dto import ReferenceDto
from .upload_cell_multipart_data import UploadCellMultipartData
from .modify_overlay_multipart_data import ModifyOverlayMultipartData
from .favorite_query_dto import FavoriteQueryDto
