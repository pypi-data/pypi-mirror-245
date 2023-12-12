from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import Union

from attrs import define as _attrs_define

from ..types import UNSET
from ..types import Unset

if TYPE_CHECKING:
    from ..models.item_columns_item import ItemColumnsItem
    from ..models.item_parser import ItemParser


T = TypeVar("T", bound="CollectionsTablesPreviewTableDataJsonBody")


@_attrs_define
class CollectionsTablesPreviewTableDataJsonBody:
    """CollectionsTablesPreviewTableDataJsonBody model

    Attributes:
        columns (Union[Unset, None, List['ItemColumnsItem']]):
        dataview_definition (Union[Unset, str]): PRQL or SQL code
        parser (Optional[ItemParser]):
    """

    parser: Optional["ItemParser"]
    columns: Union[Unset, None, List["ItemColumnsItem"]] = UNSET
    dataview_definition: Union[Unset, str] = UNSET

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

        dataview_definition = self.dataview_definition
        parser = self.parser.to_dict() if self.parser else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "parser": parser,
            }
        )
        if columns is not UNSET:
            field_dict["columns"] = columns
        if dataview_definition is not UNSET:
            field_dict["dataview_definition"] = dataview_definition

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`CollectionsTablesPreviewTableDataJsonBody` from a dict"""
        from ..models.item_columns_item import ItemColumnsItem
        from ..models.item_parser import ItemParser

        d = src_dict.copy()
        columns = []
        _columns = d.pop("columns", UNSET)
        for componentsschemasitem_columns_item_data in _columns or []:
            componentsschemasitem_columns_item = ItemColumnsItem.from_dict(
                componentsschemasitem_columns_item_data
            )

            columns.append(componentsschemasitem_columns_item)

        dataview_definition = d.pop("dataview_definition", UNSET)

        _parser = d.pop("parser")
        parser: Optional[ItemParser]
        if _parser is None:
            parser = None
        else:
            parser = ItemParser.from_dict(_parser)

        collections_tables_preview_table_data_json_body = cls(
            columns=columns,
            dataview_definition=dataview_definition,
            parser=parser,
        )

        return collections_tables_preview_table_data_json_body
