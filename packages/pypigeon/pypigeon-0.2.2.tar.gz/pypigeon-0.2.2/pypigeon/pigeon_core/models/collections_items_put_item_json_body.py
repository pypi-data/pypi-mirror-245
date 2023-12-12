from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import Union

from attrs import define as _attrs_define

from ..types import UNSET
from ..types import Unset

if TYPE_CHECKING:
    from ..models.collections_items_put_item_json_body_content import (
        CollectionsItemsPutItemJsonBodyContent,
    )
    from ..models.item_columns_item import ItemColumnsItem
    from ..models.item_metadata import ItemMetadata
    from ..models.item_parser import ItemParser
    from ..models.item_storage import ItemStorage


T = TypeVar("T", bound="CollectionsItemsPutItemJsonBody")


@_attrs_define
class CollectionsItemsPutItemJsonBody:
    """CollectionsItemsPutItemJsonBody model

    Attributes:
        columns (Union[Unset, None, List['ItemColumnsItem']]):
        content (Union[Unset, CollectionsItemsPutItemJsonBodyContent]):
        folder_id (Union[Unset, str]):  Example: ROOT.
        metadata (Union[Unset, ItemMetadata]): Arbitrary metadata as key-value string pairs
        name (Union[Unset, str]):
        parser (Union[Unset, None, ItemParser]):
        storage (Union[Unset, None, ItemStorage]):
    """

    columns: Union[Unset, None, List["ItemColumnsItem"]] = UNSET
    content: Union[Unset, "CollectionsItemsPutItemJsonBodyContent"] = UNSET
    folder_id: Union[Unset, str] = UNSET
    metadata: Union[Unset, "ItemMetadata"] = UNSET
    name: Union[Unset, str] = UNSET
    parser: Union[Unset, None, "ItemParser"] = UNSET
    storage: Union[Unset, None, "ItemStorage"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
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

        content: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.content, Unset):
            content = self.content.to_dict()

        folder_id = self.folder_id
        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        name = self.name
        parser: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.parser, Unset):
            parser = self.parser.to_dict() if self.parser else None

        storage: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.storage, Unset):
            storage = self.storage.to_dict() if self.storage else None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if columns is not UNSET:
            field_dict["columns"] = columns
        if content is not UNSET:
            field_dict["content"] = content
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if name is not UNSET:
            field_dict["name"] = name
        if parser is not UNSET:
            field_dict["parser"] = parser
        if storage is not UNSET:
            field_dict["storage"] = storage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`CollectionsItemsPutItemJsonBody` from a dict"""
        from ..models.collections_items_put_item_json_body_content import (
            CollectionsItemsPutItemJsonBodyContent,
        )
        from ..models.item_columns_item import ItemColumnsItem
        from ..models.item_metadata import ItemMetadata
        from ..models.item_parser import ItemParser
        from ..models.item_storage import ItemStorage

        d = src_dict.copy()
        columns = []
        _columns = d.pop("columns", UNSET)
        for componentsschemasitem_columns_item_data in _columns or []:
            componentsschemasitem_columns_item = ItemColumnsItem.from_dict(
                componentsschemasitem_columns_item_data
            )

            columns.append(componentsschemasitem_columns_item)

        _content = d.pop("content", UNSET)
        content: Union[Unset, CollectionsItemsPutItemJsonBodyContent]
        if isinstance(_content, Unset):
            content = UNSET
        else:
            content = CollectionsItemsPutItemJsonBodyContent.from_dict(_content)

        folder_id = d.pop("folderId", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, ItemMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ItemMetadata.from_dict(_metadata)

        name = d.pop("name", UNSET)

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

        collections_items_put_item_json_body = cls(
            columns=columns,
            content=content,
            folder_id=folder_id,
            metadata=metadata,
            name=name,
            parser=parser,
            storage=storage,
        )

        return collections_items_put_item_json_body
