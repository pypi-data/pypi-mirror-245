import typing

from django_gem.core import get_model_natural_key
from django_gem.entities.registry import CutterBatchItem
from django_gem.models.mixins import GemTriggerMixin


def is_cutting_needed(model_instance, affected_fields):
    return (
        model_instance._state.adding  # noqa
        or not affected_fields
        or not isinstance(model_instance, GemTriggerMixin)
        or model_instance.is_any_field_changed(affected_fields)
    )


def add_cut_items(
    smith,
    cut_batch_items: typing.List[CutterBatchItem],
):
    # Marking cut as started outside the transaction to avoid locks
    for cut_batch_item in cut_batch_items:
        if not cut_batch_item.object_ids:
            continue

        smith.add_item(
            natural_key=get_model_natural_key(cut_batch_item.model),
            object_ids=list(set(cut_batch_item.object_ids)),
            gem_fields=list(set(cut_batch_item.gem_fields)),
        )
