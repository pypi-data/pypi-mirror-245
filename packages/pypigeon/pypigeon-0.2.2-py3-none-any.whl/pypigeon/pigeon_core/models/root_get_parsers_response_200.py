from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import TYPE_CHECKING
from typing import TypeVar

from attrs import define as _attrs_define


if TYPE_CHECKING:
    from ..models.parser import Parser


T = TypeVar("T", bound="RootGetParsersResponse200")


@_attrs_define
class RootGetParsersResponse200:
    """RootGetParsersResponse200 model

    Attributes:
        parsers (List['Parser']):
    """

    parsers: List["Parser"]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        parsers = []
        for parsers_item_data in self.parsers:
            parsers_item = parsers_item_data.to_dict()

            parsers.append(parsers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "parsers": parsers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`RootGetParsersResponse200` from a dict"""
        from ..models.parser import Parser

        d = src_dict.copy()
        parsers = []
        _parsers = d.pop("parsers")
        for parsers_item_data in _parsers:
            parsers_item = Parser.from_dict(parsers_item_data)

            parsers.append(parsers_item)

        root_get_parsers_response_200 = cls(
            parsers=parsers,
        )

        return root_get_parsers_response_200
