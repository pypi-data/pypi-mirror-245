import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import Union

from attrs import define as _attrs_define
from dateutil.parser import isoparse

from ..models.item_type import ItemType
from ..types import UNSET
from ..types import Unset

if TYPE_CHECKING:
    from ..models.item_columns_item import ItemColumnsItem
    from ..models.item_metadata import ItemMetadata
    from ..models.item_parser import ItemParser
    from ..models.item_status import ItemStatus
    from ..models.item_storage import ItemStorage


T = TypeVar("T", bound="Item")


@_attrs_define
class Item:
    """A single item's metadata

    Attributes:
        created_on (datetime.datetime):
        id (str):
        name (str): Item name
        type (ItemType):
        columns (Union[Unset, None, List['ItemColumnsItem']]):
        folder_id (Union[Unset, str]): Item ID of parent folder, or ROOT Example: ROOT.
        metadata (Union[Unset, ItemMetadata]): Arbitrary metadata as key-value string pairs
        parser (Union[Unset, None, ItemParser]):
        status (Union[Unset, ItemStatus]):
        storage (Union[Unset, None, ItemStorage]):
    """

    created_on: datetime.datetime
    id: str
    name: str
    type: ItemType
    columns: Union[Unset, None, List["ItemColumnsItem"]] = UNSET
    folder_id: Union[Unset, str] = UNSET
    metadata: Union[Unset, "ItemMetadata"] = UNSET
    parser: Union[Unset, None, "ItemParser"] = UNSET
    status: Union[Unset, "ItemStatus"] = UNSET
    storage: Union[Unset, None, "ItemStorage"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        created_on = self.created_on.isoformat()

        id = self.id
        name = self.name
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

        folder_id = self.folder_id
        metadata: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        parser: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.parser, Unset):
            parser = self.parser.to_dict() if self.parser else None

        status: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.to_dict()

        storage: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.storage, Unset):
            storage = self.storage.to_dict() if self.storage else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "createdOn": created_on,
                "id": id,
                "name": name,
                "type": type,
            }
        )
        if columns is not UNSET:
            field_dict["columns"] = columns
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if parser is not UNSET:
            field_dict["parser"] = parser
        if status is not UNSET:
            field_dict["status"] = status
        if storage is not UNSET:
            field_dict["storage"] = storage

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`Item` from a dict"""
        from ..models.item_columns_item import ItemColumnsItem
        from ..models.item_metadata import ItemMetadata
        from ..models.item_parser import ItemParser
        from ..models.item_status import ItemStatus
        from ..models.item_storage import ItemStorage

        d = src_dict.copy()
        created_on = isoparse(d.pop("createdOn"))

        id = d.pop("id")

        name = d.pop("name")

        type = ItemType(d.pop("type"))

        columns = []
        _columns = d.pop("columns", UNSET)
        for componentsschemasitem_columns_item_data in _columns or []:
            componentsschemasitem_columns_item = ItemColumnsItem.from_dict(
                componentsschemasitem_columns_item_data
            )

            columns.append(componentsschemasitem_columns_item)

        folder_id = d.pop("folderId", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: Union[Unset, ItemMetadata]
        if isinstance(_metadata, Unset):
            metadata = UNSET
        else:
            metadata = ItemMetadata.from_dict(_metadata)

        _parser = d.pop("parser", UNSET)
        parser: Union[Unset, None, ItemParser]
        if _parser is None:
            parser = None
        elif isinstance(_parser, Unset):
            parser = UNSET
        else:
            parser = ItemParser.from_dict(_parser)

        _status = d.pop("status", UNSET)
        status: Union[Unset, ItemStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = ItemStatus.from_dict(_status)

        _storage = d.pop("storage", UNSET)
        storage: Union[Unset, None, ItemStorage]
        if _storage is None:
            storage = None
        elif isinstance(_storage, Unset):
            storage = UNSET
        else:
            storage = ItemStorage.from_dict(_storage)

        item = cls(
            created_on=created_on,
            id=id,
            name=name,
            type=type,
            columns=columns,
            folder_id=folder_id,
            metadata=metadata,
            parser=parser,
            status=status,
            storage=storage,
        )

        return item
