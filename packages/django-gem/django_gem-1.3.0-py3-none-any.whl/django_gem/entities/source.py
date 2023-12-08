import dataclasses
import typing


@dataclasses.dataclass
class CutSource:
    object_id: str
    affected_fields: typing.List[str]
