from typing import Any
from typing import Dict
from typing import Type
from typing import TYPE_CHECKING
from typing import TypeVar

from attrs import define as _attrs_define


if TYPE_CHECKING:
    from ..models.search_search_dictionaries_json_body_options import (
        SearchSearchDictionariesJsonBodyOptions,
    )


T = TypeVar("T", bound="SearchSearchDictionariesJsonBody")


@_attrs_define
class SearchSearchDictionariesJsonBody:
    """SearchSearchDictionariesJsonBody model

    Attributes:
        options (SearchSearchDictionariesJsonBodyOptions):
        query (str):
        source (str):
    """

    options: "SearchSearchDictionariesJsonBodyOptions"
    query: str
    source: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        options = self.options.to_dict()

        query = self.query
        source = self.source

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "options": options,
                "query": query,
                "source": source,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`SearchSearchDictionariesJsonBody` from a dict"""
        from ..models.search_search_dictionaries_json_body_options import (
            SearchSearchDictionariesJsonBodyOptions,
        )

        d = src_dict.copy()
        options = SearchSearchDictionariesJsonBodyOptions.from_dict(d.pop("options"))

        query = d.pop("query")

        source = d.pop("source")

        search_search_dictionaries_json_body = cls(
            options=options,
            query=query,
            source=source,
        )

        return search_search_dictionaries_json_body
