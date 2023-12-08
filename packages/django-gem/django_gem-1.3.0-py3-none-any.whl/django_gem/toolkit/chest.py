import typing
from collections import defaultdict
from dataclasses import asdict, dataclass

from django_gem.entities.source import CutSource


@dataclass
class ChestItem:
    gem_fields: list
    object_ids: list


@dataclass
class SealedChestItem:
    object_id: str
    gem_fields: list


class Chest:
    """Storage for all pending cuttings"""

    cut_models: typing.Dict[str, typing.List[ChestItem]] = defaultdict(list)
    cut_sources: typing.Dict[str, typing.List[CutSource]] = defaultdict(list)

    @classmethod
    def seal_items(cls, chest_items: typing.List[ChestItem]) -> typing.List[SealedChestItem]:
        sealed_item_mapping: typing.Dict[str, SealedChestItem] = {}
        for chest_item in chest_items:
            for object_id in chest_item.object_ids:
                if sealed_item_mapping.get(object_id):
                    sealed_item_mapping[object_id].gem_fields = list(
                        {*sealed_item_mapping[object_id].gem_fields, *chest_item.gem_fields}
                    )
                else:
                    sealed_item_mapping[object_id] = SealedChestItem(
                        object_id=object_id,
                        gem_fields=chest_item.gem_fields,
                    )
        return list(sealed_item_mapping.values())

    def add_chest_item(self, natural_key: str, object_ids: list, gem_fields: list):
        object_ids = [object_id for object_id in object_ids if object_id is not None]
        if not object_ids:
            return

        self.cut_models[natural_key].append(
            ChestItem(
                gem_fields=gem_fields,
                object_ids=[str(object_id) for object_id in object_ids if object_id is not None],
            )
        )

    def add_cut_source(self, natural_key: str, cut_source: CutSource):
        self.cut_sources[natural_key].append(cut_source)

    def reset(self):
        self.cut_models = defaultdict(list)
        self.cut_sources = defaultdict(list)

    def is_empty(self):
        return not bool(self.cut_models)

    def get_sealed_chest(self):
        sealed_chest = {}

        for natural_key, chest_items in self.cut_models.items():
            sealed_chest[natural_key] = [
                asdict(item) for item in self.seal_items(chest_items=chest_items)
            ]
        return sealed_chest

    def get_sealed_sources(self):
        sealed_sources = {}
        for natural_key, source_items in self.cut_sources.items():
            sealed_sources[natural_key] = [asdict(item) for item in source_items]
        return sealed_sources
