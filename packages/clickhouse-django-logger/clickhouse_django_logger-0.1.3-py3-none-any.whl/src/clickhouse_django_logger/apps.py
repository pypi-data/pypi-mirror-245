from django.apps import AppConfig


class DjangoClickhouseLoggerConfig(AppConfig):
    name = 'clickhouse_django_logger'
    verbose_name = 'ClickHouse Django Logger'

    def ready(self):
        from .utils import ensure_clickhouse_db_and_table_exist
        from .config import check_settings

        check_settings()
        ensure_clickhouse_db_and_table_exist()
