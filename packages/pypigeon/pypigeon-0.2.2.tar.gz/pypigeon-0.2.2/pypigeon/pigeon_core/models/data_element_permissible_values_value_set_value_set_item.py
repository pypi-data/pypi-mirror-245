from typing import Any
from typing import cast
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
    from ..models.data_element_concept import DataElementConcept


T = TypeVar("T", bound="DataElementPermissibleValuesValueSetValueSetItem")


@_attrs_define
class DataElementPermissibleValuesValueSetValueSetItem:
    """A single permissible value match.

    Attributes:
        concepts (Union[Unset, List['DataElementConcept']]): Zero or more concepts associated with this individual
            value. Typically, the `appliesTo` field for PV valueSet concepts will be "valueDomain".
        meaning (Union[Unset, str]): A description of this value's meaning.
        value (Union[None, bool, float, str]):
    """

    value: Union[None, bool, float, str]
    concepts: Union[Unset, List["DataElementConcept"]] = UNSET
    meaning: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        concepts: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.concepts, Unset):
            concepts = []
            for concepts_item_data in self.concepts:
                concepts_item = concepts_item_data.to_dict()

                concepts.append(concepts_item)

        meaning = self.meaning
        value: Union[None, bool, float, str]
        if self.value is None:
            value = None

        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "value": value,
            }
        )
        if concepts is not UNSET:
            field_dict["concepts"] = concepts
        if meaning is not UNSET:
            field_dict["meaning"] = meaning

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`DataElementPermissibleValuesValueSetValueSetItem` from a dict"""
        from ..models.data_element_concept import DataElementConcept

        d = src_dict.copy()
        concepts = []
        _concepts = d.pop("concepts", UNSET)
        for concepts_item_data in _concepts or []:
            concepts_item = DataElementConcept.from_dict(concepts_item_data)

            concepts.append(concepts_item)

        meaning = d.pop("meaning", UNSET)

        def _parse_value(data: object) -> Union[None, bool, float, str]:
            if data is None:
                return data
            return cast(Union[None, bool, float, str], data)

        value = _parse_value(d.pop("value"))

        data_element_permissible_values_value_set_value_set_item = cls(
            concepts=concepts,
            meaning=meaning,
            value=value,
        )

        return data_element_permissible_values_value_set_value_set_item
