import typing

from django.db import models


def get_model_natural_key(model: typing.Union[models.Model, typing.Type[models.Model]]):
    model_meta = model._meta
    return f"{model_meta.app_label}.{model_meta.model_name}"
