import json

from celery import shared_task


@shared_task(name="cut_models_task")
def cut_models_task(sealed_chest: str, sealed_sources: str):
    from django_gem.toolkit.saw import Saw

    cut_mapping = json.dumps(Saw.cut_models(sealed_chest, sealed_sources))
    return cut_mapping
