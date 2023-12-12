import json
from io import BytesIO
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Type
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import Union

from attrs import define as _attrs_define

from ..models.item_type import ItemType
from ..types import File
from ..types import UNSET
from ..types import Unset

if TYPE_CHECKING:
    from ..models.collections_items_create_item_form_style_upload_metadata import (
        CollectionsItemsCreateItemFormStyleUploadMetadata,
    )
    from ..models.item_columns_item import ItemColumnsItem
    from ..models.item_parser import ItemParser
    from ..models.item_storage import ItemStorage


T = TypeVar("T", bound="CollectionsItemsCreateItemFormStyleUpload")


@_attrs_define
class CollectionsItemsCreateItemFormStyleUpload:
    """Creation of a new item

    Attributes:
        content (File):
        folder_id (str):  Example: ROOT.
        type (ItemType):
        columns (Union[Unset, None, List['ItemColumnsItem']]):
        metadata (Union[Unset, CollectionsItemsCreateItemFormStyleUploadMetadata]):
        parser (Union[Unset, None, ItemParser]):
        storage (Union[Unset, None, ItemStorage]):
    """

    content: File
    folder_id: str
    type: ItemType
    columns: Union[Unset, None, List["ItemColumnsItem"]] = UNSET
    metadata: Union[Unset, "CollectionsItemsCreateItemFormStyleUploadMetadata"] = UNSET
    parser: Union[Unset, None, "ItemParser"] = UNSET
    storage: Union[Unset, None, "ItemStorage"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        content = self.content.to_tuple()

        folder_id = self.folder_id
        type = self.type.value

        columns: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.columns, Unset):
            if self.columns is None:
                columns = None
            else:
                columns = []
                for componentsschemasitem_columns_item_data in self.columns:
                    componentsschemasitem_columns_item = (
                        componentsschemasitem_columns_item_data.to_dict()
                    )

                    columns.append(componentsschemasitem_columns_item)

        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        parser: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.parser, Unset):
            parser = self.parser.to_dict() if self.parser else None

        storage: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.storage, Unset):
            storage = self.storage.to_dict() if self.storage else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "content": content,
                "folderId": folder_id,
                "type": type,
            }
        )
        if columns is not UNSET:
            field_dict["columns"] = columns
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if parser is not UNSET:
            field_dict["parser"] = parser
        if storage is not UNSET:
            field_dict["storage"] = storage

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        content = self.content.to_tuple()

        folder_id = (
            self.folder_id
            if isinstance(self.folder_id, Unset)
            else (None, str(self.folder_id).encode(), "text/plain")
        )
        type = (None, str(self.type.value).encode(), "text/plain")

        columns: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.columns, Unset):
            if self.columns is None:
                columns = (None, b"null", "application/json")
            else:
                _temp_columns = []
                for componentsschemasitem_columns_item_data in self.columns:
                    componentsschemasitem_columns_item = (
                        componentsschemasitem_columns_item_data.to_dict()
                    )

                    _temp_columns.append(componentsschemasitem_columns_item)
                columns = (None, json.dumps(_temp_columns).encode(), "application/json")

        metadata: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = (
                None,
                json.dumps(self.metadata.to_dict()).encode(),
                "application/json",
            )

        parser: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.parser, Unset):
            parser = (
                None,
                json.dumps((self.parser.to_dict() if self.parser else None)).encode(),
                "application/json",
            )

        storage: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.storage, Unset):
            storage = (
                None,
                json.dumps((self.storage.to_dict() if self.storage else None)).encode(),
                "application/json",
            )

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "content": content,
                "folderId": folder_id,
                "type": type,
            }
        )
        if columns is not UNSET:
            field_dict["columns"] = columns
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if parser is not UNSET:
            field_dict["parser"] = parser
        if storage is not UNSET:
            field_dict["storage"] = storage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`CollectionsItemsCreateItemFormStyleUpload` from a dict"""
        from ..models.collections_items_create_item_form_style_upload_metadata import (
            CollectionsItemsCreateItemFormStyleUploadMetadata,
        )
        from ..models.item_columns_item import ItemColumnsItem
        from ..models.item_parser import ItemParser
        from ..models.item_storage import ItemStorage

        d = src_dict.copy()
        content = File(payload=BytesIO(d.pop("content")))

        folder_id = d.pop("folderId")

        type = ItemType(d.pop("type"))

        columns = []
        _columns = d.pop("columns", UNSET)
        for componentsschemasitem_columns_item_data in _columns or []:
            componentsschemasitem_columns_item = ItemColumnsItem.from_dict(
                componentsschemasitem_columns_item_data
            )

            columns.append(componentsschemasitem_columns_item)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, CollectionsItemsCreateItemFormStyleUploadMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = CollectionsItemsCreateItemFormStyleUploadMetadata.from_dict(
                _metadata
            )

        _parser = d.pop("parser", UNSET)
        parser: Union[Unset, None, ItemParser]
        if _parser is None:
            parser = None
        elif isinstance(_parser, Unset):
            parser = UNSET
        else:
            parser = ItemParser.from_dict(_parser)

        _storage = d.pop("storage", UNSET)
        storage: Union[Unset, None, ItemStorage]
        if _storage is None:
            storage = None
        elif isinstance(_storage, Unset):
            storage = UNSET
        else:
            storage = ItemStorage.from_dict(_storage)

        collections_items_create_item_form_style_upload = cls(
            content=content,
            folder_id=folder_id,
            type=type,
            columns=columns,
            metadata=metadata,
            parser=parser,
            storage=storage,
        )

        return collections_items_create_item_form_style_upload
