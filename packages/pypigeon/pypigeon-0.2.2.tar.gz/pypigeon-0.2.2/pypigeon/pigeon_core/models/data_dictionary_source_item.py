from enum import Enum


class DataDictionarySourceItem(str, Enum):
    EXTERNAL = "external"
    REFERENCEDINTHISCOLLECTION = "referencedInThisCollection"
    SYSTEMSTANDARD = "systemStandard"
    THISCOLLECTION = "thisCollection"

    def __str__(self) -> str:
        return str(self.value)
