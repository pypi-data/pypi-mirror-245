from celery import shared_task


@shared_task(name="cut_queryset_task")
def cut_queryset_task(natural_key: str, object_ids: list):
    from django_gem.toolkit.saw import Saw

    Saw.cut_queryset(natural_key, object_ids)
