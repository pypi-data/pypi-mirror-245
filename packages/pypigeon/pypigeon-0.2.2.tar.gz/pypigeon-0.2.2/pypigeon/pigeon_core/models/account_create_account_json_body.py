from typing import Any
from typing import Dict
from typing import Type
from typing import TypeVar

from attrs import define as _attrs_define


T = TypeVar("T", bound="AccountCreateAccountJsonBody")


@_attrs_define
class AccountCreateAccountJsonBody:
    """AccountCreateAccountJsonBody model

    Attributes:
        account_name (str):
    """

    account_name: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        account_name = self.account_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "account_name": account_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`AccountCreateAccountJsonBody` from a dict"""
        d = src_dict.copy()
        account_name = d.pop("account_name")

        account_create_account_json_body = cls(
            account_name=account_name,
        )

        return account_create_account_json_body
