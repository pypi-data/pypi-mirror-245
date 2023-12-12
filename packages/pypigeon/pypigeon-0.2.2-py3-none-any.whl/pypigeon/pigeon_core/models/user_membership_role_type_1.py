from enum import Enum


class UserMembershipRoleType1(str, Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"

    def __str__(self) -> str:
        return str(self.value)
