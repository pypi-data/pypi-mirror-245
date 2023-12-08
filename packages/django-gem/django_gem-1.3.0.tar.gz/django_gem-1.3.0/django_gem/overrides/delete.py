import typing

from django.db import transaction

from django_gem.constants import GemCuttingMode
from django_gem.core import get_model_natural_key
from django_gem.entities.context import gem_cutting_context
from django_gem.entities.registry import CutterBatchItem
from django_gem.entities.source import CutSource
from django_gem.models.mixins import GemCutConditionalMixin
from django_gem.overrides.utils import add_cut_items


def delete_cutting_hook(
    delete_func,
    cut_batch_items: typing.List[CutterBatchItem],
):
    def wrapped_trigger(self, *args, **kwargs):
        from django_gem.toolkit import gem_settings, smith

        gem_cutting_enabled = gem_settings.GEM_CUTTING_ENABLED

        should_cut = True
        if isinstance(self, GemCutConditionalMixin):
            should_cut = self.should_cut_on_delete(*args, **kwargs)

        if should_cut:
            for cut_batch_item in cut_batch_items:
                cut_batch_item.load_object_ids(self)

            smith.add_source(
                get_model_natural_key(self), CutSource(object_id=str(self.id), affected_fields=[])
            )

        with transaction.atomic():
            result = delete_func(self, *args, **kwargs)
            if not gem_cutting_enabled or not should_cut:
                return result

            add_cut_items(smith, cut_batch_items)
            if gem_cutting_context.cutting_mode == GemCuttingMode.TRANSACTION:
                transaction.on_commit(
                    lambda: smith.initiate_cutting(),
                )
            return result

    return wrapped_trigger
