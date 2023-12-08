from django_gem.entities.context import gem_cutting_context


class OverrideGemCuttingMode:
    def __init__(self, override_mode: str):
        self.override_mode = override_mode
        self.original_mode = gem_cutting_context.cutting_mode

    def __enter__(self):
        gem_cutting_context.cutting_mode = self.override_mode

    def __exit__(self, exc_type, exc_value, exc_traceback):
        gem_cutting_context.cutting_mode = self.original_mode
