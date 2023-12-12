from typing import Any
from typing import Dict
from typing import Type
from typing import TypeVar
from typing import Union

from attrs import define as _attrs_define

from ..models.item_columns_item_type import ItemColumnsItemType
from ..types import UNSET
from ..types import Unset


T = TypeVar("T", bound="ItemColumnsItem")


@_attrs_define
class ItemColumnsItem:
    """ItemColumnsItem model

    Attributes:
        name (str):
        data_element_ref (Union[Unset, str]):
        type (Union[Unset, ItemColumnsItemType]):
    """

    name: str
    data_element_ref: Union[Unset, str] = UNSET
    type: Union[Unset, ItemColumnsItemType] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        name = self.name
        data_element_ref = self.data_element_ref
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if data_element_ref is not UNSET:
            field_dict["data_element_ref"] = data_element_ref
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`ItemColumnsItem` from a dict"""
        d = src_dict.copy()
        name = d.pop("name")

        data_element_ref = d.pop("data_element_ref", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, ItemColumnsItemType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = ItemColumnsItemType(_type)

        item_columns_item = cls(
            name=name,
            data_element_ref=data_element_ref,
            type=type,
        )

        return item_columns_item
