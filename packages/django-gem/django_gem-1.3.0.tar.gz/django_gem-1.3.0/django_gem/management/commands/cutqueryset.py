import logging

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from django_gem.toolkit.saw import Saw

User = get_user_model()
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "app_label",
            help="Specify the app label to cut gems for.",
        )
        parser.add_argument(
            "model_name",
            help="Specify the mode name to cut gems for.",
        )
        parser.add_argument(
            "--field-names",
            nargs="*",
            help="Specify the field names to cut gems for.",
        )

    def handle(self, *args, **options):
        app_label = options["app_label"]
        model_name = options["model_name"]
        field_names = options.get("field_names") or []
        Saw.cut_content_type(natural_key=f"{app_label}.{model_name}", field_names=field_names)
