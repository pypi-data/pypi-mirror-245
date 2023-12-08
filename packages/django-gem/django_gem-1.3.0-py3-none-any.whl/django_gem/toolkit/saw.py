import contextlib
import json
import typing
from collections import defaultdict

from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError, transaction

from django_gem.core import get_model_natural_key
from django_gem.logger import logger
from django_gem.models.mixins import GemModelMixin
from django_gem.toolkit import forge, gem_settings
from django_gem.toolkit.chest import SealedChestItem


class Saw:
    @classmethod
    def _get_queryset(cls, model_class, object_ids):
        from django_gem.toolkit import cutter_registry

        queryset = model_class.objects.filter(id__in=object_ids)
        select_related_fields, prefetch_related_fields = [], []
        cutter_model = cutter_registry.get_cutter_for_model(model_class)
        if cutter_model:
            (select_related_fields, prefetch_related_fields) = (
                cutter_model.select_related_fields,
                cutter_model.prefetch_related_fields,
            )
        if select_related_fields:
            queryset = queryset.select_related(*select_related_fields)
        if prefetch_related_fields:
            queryset = queryset.prefetch_related(*prefetch_related_fields)
        return queryset

    @classmethod
    def cut_content_type(cls, natural_key: str, field_names: list):
        gem_cutting_enabled = gem_settings.GEM_CUTTING_ENABLED

        if not gem_cutting_enabled:
            return
        try:
            content_type: ContentType = ContentType.objects.get_by_natural_key(
                *natural_key.split(".")
            )
        except ContentType.DoesNotExist:
            return

        model_class = content_type.model_class()
        for model_instance in model_class.objects.all():
            if isinstance(model_class, GemModelMixin):
                model_class.update_cutting_started_at([model_instance.id])
            forge.cut_model_fields(model_instance, field_names)
            if isinstance(model_class, GemModelMixin):
                model_class.update_cutting_completed_at([model_instance.id])

    @classmethod
    def cut_models(cls, sealed_chest: str, sealed_sources: str):
        gem_cutting_enabled = gem_settings.GEM_CUTTING_ENABLED

        cut_mapping = defaultdict(int)

        if not gem_cutting_enabled:
            return
        try:
            unsealed_chest: typing.Dict[str, typing.List[typing.Dict]] = json.loads(sealed_chest)
        except json.JSONDecodeError:
            return

        logger.info(f"Cutting initiated by: {sealed_sources}; for: {sealed_chest}")

        for natural_key, chest_items in unsealed_chest.items():
            try:
                content_type: ContentType = ContentType.objects.get_by_natural_key(
                    *natural_key.split(".")
                )
            except ContentType.DoesNotExist:
                continue

            sealed_chest_mapping: typing.Dict[str, SealedChestItem] = {
                SealedChestItem(**item).object_id: SealedChestItem(**item) for item in chest_items
            }
            chest_item_object_ids = [chest_item for chest_item in sealed_chest_mapping]

            model_class = content_type.model_class()

            if isinstance(model_class, GemModelMixin):
                model_class.update_cutting_started_at(chest_item_object_ids)

            queryset = cls._get_queryset(model_class, chest_item_object_ids)

            for model_instance in queryset:
                model_instance_id = str(model_instance.id)
                if (sealed_chest_item := sealed_chest_mapping.get(str(model_instance_id))) is None:
                    continue
                with contextlib.suppress(IntegrityError):
                    # Because of the distributed nature of cutting, the update to gem can happen
                    # after the referencing model was deleted. This will ensure we don't stop
                    # all the cuttings if something goes wrong.
                    forge.cut_model_fields(model_instance, sealed_chest_item.gem_fields)
                    cut_mapping[natural_key] += 1

            if isinstance(model_class, GemModelMixin):
                model_class.update_cutting_completed_at(chest_item_object_ids)

        cut_mapping = dict(cut_mapping)
        logger.info(f"Cutting finished, cutting results: {cut_mapping}")

        return cut_mapping

    @classmethod
    def cut_queryset(cls, natural_key: str, object_ids: list):
        gem_cutting_enabled = gem_settings.GEM_CUTTING_ENABLED

        if not gem_cutting_enabled:
            return
        from django_gem.toolkit import forge, smith

        try:
            content_type: ContentType = ContentType.objects.get_by_natural_key(
                *natural_key.split(".")
            )
        except ContentType.DoesNotExist:
            return

        cut_mapping = defaultdict(int)

        model_class = content_type.model_class()

        queryset = cls._get_queryset(model_class, object_ids)

        for model_instance in queryset:
            reverse_cutter_model = forge.cutter_registry.get_reverse_cutter_for_model(
                model_instance
            )
            if not reverse_cutter_model or not reverse_cutter_model.model:
                continue

            for reverse_cutter_trigger in reverse_cutter_model.triggers:
                object_ids = list(reverse_cutter_trigger.callback(model_instance))
                if not object_ids:
                    continue
                natural_key = get_model_natural_key(reverse_cutter_trigger.model)
                smith.add_item(
                    natural_key=natural_key,
                    object_ids=object_ids,
                    gem_fields=reverse_cutter_trigger.gem_fields,
                )
                cut_mapping[natural_key] += 1
            with transaction.atomic():
                smith.initiate_cutting()
        cut_mapping = dict(cut_mapping)
        return cut_mapping
