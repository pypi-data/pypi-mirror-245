from django_gem.constants import GemCuttingMode


class GemCuttingContext:
    return_eager_value: bool = False
    cutting_mode: str = GemCuttingMode.TRANSACTION


gem_cutting_context = GemCuttingContext()
