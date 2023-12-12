from typing import Any
from typing import Dict
from typing import Optional
from typing import Type
from typing import TypeVar

from attrs import define as _attrs_define


T = TypeVar("T", bound="Pagination")


@_attrs_define
class Pagination:
    """Pagination model

    Attributes:
        items_per_page (int):
        total_items (int):
        next_page_url (Optional[str]):
    """

    items_per_page: int
    total_items: int
    next_page_url: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        items_per_page = self.items_per_page
        total_items = self.total_items
        next_page_url = self.next_page_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "items_per_page": items_per_page,
                "total_items": total_items,
                "next_page_url": next_page_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`Pagination` from a dict"""
        d = src_dict.copy()
        items_per_page = d.pop("items_per_page")

        total_items = d.pop("total_items")

        next_page_url = d.pop("next_page_url")

        pagination = cls(
            items_per_page=items_per_page,
            total_items=total_items,
            next_page_url=next_page_url,
        )

        return pagination
