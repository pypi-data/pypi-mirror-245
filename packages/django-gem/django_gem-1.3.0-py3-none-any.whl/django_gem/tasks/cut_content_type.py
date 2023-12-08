from celery import shared_task


@shared_task(name="cut_content_type_task")
def cut_content_type_task(natural_key: str, field_names: list):
    from django_gem.toolkit.saw import Saw

    Saw.cut_content_type(natural_key, field_names)
