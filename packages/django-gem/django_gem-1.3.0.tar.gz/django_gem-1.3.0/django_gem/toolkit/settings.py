from django.conf import settings


class DjangoGemsSettings:
    # region Non-configurable fields
    DEFAULT_RELATED_GEM_FIELD_NAME = "gem"
    CACHED_GEM_CUTTER_FIELD_NAME = "cached_cutter"
    # endregion

    CUTTER_PROPERTY_PREFIX = "cut_"
    CUTTER_MODEL_RELATED_NAME = "cutter_target"
    CUTTER_PROPAGATED_TRIGGERS_MAX_DEPTH = 10
    CUTTER_VALIDATION_ENABLED = True
    GEM_IGNORED_FIELDS = []
    GEM_ANVILS = []
    GEM_CUTTING_ENABLED = True
    GEM_SKIP_MISSING_AFFECTED_FIELDS = False

    def __init__(self):
        self.load()

    def load(self):
        for setting_key in filter(
            lambda key: (key.startswith("CUTTER") or key.startswith("GEM")), dir(settings)
        ):
            if hasattr(settings, setting_key):
                setattr(self, setting_key, getattr(settings, setting_key))


gem_settings = DjangoGemsSettings()
