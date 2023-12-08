import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from django.core.management import BaseCommand

from django_gem.toolkit.gem_migration.collector import Collector
from django_gem.toolkit.gem_migration.constants import (
    GEM_MIGRATIONS_INITIAL_MIGRATION_FILE_NAME,
    GEM_MIGRATIONS_MIGRATION_FILE_PREFIX,
    GEM_MIGRATIONS_MODULE_NAME,
    GEM_MIGRATIONS_STABLE_INDEX_FILE_NAME,
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        stable_index = Collector.collect_stable_index()

        for app_label, app_index in stable_index.items():
            if not (Path(app_label) / GEM_MIGRATIONS_MODULE_NAME).exists():
                raise ValueError(
                    f"Can't create gem migrations for app {app_label} because gem migrations folder is missing"
                )

            stable_index_file = (
                Path(app_label) / GEM_MIGRATIONS_MODULE_NAME / GEM_MIGRATIONS_STABLE_INDEX_FILE_NAME
            )
            initial_migration_file = (
                Path(app_label)
                / GEM_MIGRATIONS_MODULE_NAME
                / GEM_MIGRATIONS_INITIAL_MIGRATION_FILE_NAME
            )
            if initial_migration_file.exists() and not stable_index_file.exists():
                raise ValueError(
                    f"Gem migrations module is misconfigured for app {app_label}, "
                    f"unable to find stable index file, initial migration exists"
                )
            if not initial_migration_file.exists():
                stable_index_file.write_text(json.dumps(app_index, indent=4))
                initial_migration_file.write_text(
                    json.dumps(self.state_index_to_migration(app_label, app_index), indent=4)
                )
            else:
                current_stable_index = json.loads(stable_index_file.read_text())
                new_migration = defaultdict(dict)
                for model_name, model_index in app_index.items():
                    if model_name not in current_stable_index:
                        new_migration[model_name] = model_index
                        continue

                    for field_name, field_index in model_index.items():
                        if current_stable_index[model_name].get(field_name) != field_index:
                            new_migration[model_name][field_name] = field_index
                if new_migration:
                    migration_name = int(datetime.timestamp(datetime.now()) * 1000)
                    new_migration_file = (
                        Path(app_label)
                        / GEM_MIGRATIONS_MODULE_NAME
                        / f"{GEM_MIGRATIONS_MIGRATION_FILE_PREFIX}{migration_name}.json"
                    )
                    new_migration_file.write_text(
                        json.dumps(
                            self.state_index_to_migration(app_label, new_migration), indent=4
                        )
                    )
                    stable_index_file.write_text(json.dumps(app_index, indent=4))

    @classmethod
    def state_index_to_migration(cls, app_label: str, state_index: dict):
        return {
            f"{app_label}.{model_name}": list(fields.keys())
            for model_name, fields in state_index.items()
        }
