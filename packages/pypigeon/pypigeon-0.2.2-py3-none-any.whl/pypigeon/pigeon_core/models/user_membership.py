from typing import Any
from typing import Dict
from typing import Type
from typing import TypeVar
from typing import Union

from attrs import define as _attrs_define

from ..models.group_role import GroupRole
from ..models.user_membership_role_type_1 import UserMembershipRoleType1


T = TypeVar("T", bound="UserMembership")


@_attrs_define
class UserMembership:
    """UserMembership model

    Attributes:
        id (str):
        role (Union[GroupRole, UserMembershipRoleType1]):
    """

    id: str
    role: Union[GroupRole, UserMembershipRoleType1]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        id = self.id
        role: str

        if isinstance(self.role, GroupRole):
            role = self.role.value

        else:
            role = self.role.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "role": role,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`UserMembership` from a dict"""
        d = src_dict.copy()
        id = d.pop("id")

        def _parse_role(data: object) -> Union[GroupRole, UserMembershipRoleType1]:
            try:
                if not isinstance(data, str):
                    raise TypeError()
                role_type_0 = GroupRole(data)

                return role_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            role_type_1 = UserMembershipRoleType1(data)

            return role_type_1

        role = _parse_role(d.pop("role"))

        user_membership = cls(
            id=id,
            role=role,
        )

        return user_membership
