import hashlib
import inspect
import typing
from collections import defaultdict

from django_gem.models.base import CutterEngineBaseModel
from django_gem.toolkit import cutter_registry, gem_settings


class Collector:
    @classmethod
    def collect_stable_index(cls):
        stable_index = defaultdict(dict)
        gem_classes: typing.List[
            typing.Type[CutterEngineBaseModel]
        ] = cutter_registry.get_subclasses(CutterEngineBaseModel)
        for gem_class in gem_classes:
            app_label = gem_class.CutterEngineMeta.model._meta.app_label
            model_name = gem_class.CutterEngineMeta.model._meta.model_name
            if app_label not in stable_index:
                stable_index[app_label] = defaultdict(dict)
            if model_name not in stable_index[app_label]:
                stable_index[app_label][model_name] = defaultdict(dict)
            cutter = gem_class.CutterEngineMeta.cutter
            for cutter_method_name in cutter.__dict__.keys():
                if not cutter_method_name.startswith(gem_settings.CUTTER_PROPERTY_PREFIX):
                    continue
                property_method = getattr(cutter, cutter_method_name)
                property_callable = (
                    getattr(property_method, "real_func", None)
                    # Supporting functools cached_property here
                    or getattr(property_method, "func", None)
                    # Supporting regular property here
                    or getattr(property_method, "fget", None)
                )
                hashed_value = "".join(inspect.getsource(property_callable).split())
                field_name = cutter_method_name.replace(gem_settings.CUTTER_PROPERTY_PREFIX, "")
                stable_index[app_label][model_name][field_name] = hashlib.md5(
                    hashed_value.encode("utf-8")
                ).hexdigest()

        return stable_index
