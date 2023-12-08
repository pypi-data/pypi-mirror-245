from django.apps.registry import Apps
from django.db import DatabaseError, models
from django.db.migrations.exceptions import MigrationSchemaMissing
from django.utils.functional import classproperty
from django.utils.timezone import now


class GemMigrationRecorder:
    _migration_class = None

    @classproperty
    def GemMigration(cls):
        if cls._migration_class is None:

            class GemMigration(models.Model):
                app = models.CharField(max_length=255)
                name = models.CharField(max_length=255)
                applied = models.DateTimeField(default=now)

                class Meta:
                    apps = Apps()
                    app_label = "gem_migrations"
                    db_table = "django_gem_migrations"

                def __str__(self):
                    return "Gem Migration %s for %s" % (self.name, self.app)

            cls._migration_class = GemMigration
        return cls._migration_class

    def __init__(self, connection):
        self.connection = connection

    @property
    def migration_qs(self):
        return self.GemMigration.objects.using(self.connection.alias)

    def has_table(self):
        """Return True if the django_migrations table exists."""
        with self.connection.cursor() as cursor:
            tables = self.connection.introspection.table_names(cursor)
        return self.GemMigration._meta.db_table in tables

    def ensure_schema(self):
        """Ensure the table exists and has the correct schema."""
        # If the table's there, that's fine - we've never changed its schema
        # in the codebase.
        if self.has_table():
            return
        # Make the table
        try:
            with self.connection.schema_editor() as editor:
                editor.create_model(self.GemMigration)
        except DatabaseError as exc:
            raise MigrationSchemaMissing(
                "Unable to create the django_gem_migrations table (%s)" % exc
            )

    def applied_migrations(self):
        """
        Return a dict mapping (app_name, migration_name) to Migration instances
        for all applied migrations.
        """
        if self.has_table():
            return {(migration.app, migration.name): migration for migration in self.migration_qs}
        else:
            # If the django_migrations table doesn't exist, then no migrations
            # are applied.
            return {}

    def record_applied(self, app, name):
        self.ensure_schema()
        self.migration_qs.create(app=app, name=name)

    def record_unapplied(self, app, name):
        self.ensure_schema()
        self.migration_qs.filter(app=app, name=name).delete()
