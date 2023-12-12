from enum import Enum
from typing import List, Optional


class Conventions(Enum):
    GENERIC = "generic"
    V1_0_0 = "v1.0.0"

    @staticmethod
    def get_by_value(convention_version: str) -> Optional["Conventions"]:
        """
        Get the Conventions enum from its sting value, or if it doesn't exist,
        return `None`
        """
        for convention in Conventions:
            if convention.value == convention_version:
                return convention

    @staticmethod
    def values() -> List[str]:
        return sorted([convention.value for convention in Conventions])
