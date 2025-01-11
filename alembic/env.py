from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from alembic.script import ScriptDirectory
from src.common.configs import settings
from src.common.db.db_base import Base

config = context.config

fileConfig(config.config_file_name)  # type: ignore

target_metadata = Base.metadata


def process_revision_directives(context, revision, directives):
    migration_script = directives[0]

    head_revision = ScriptDirectory.from_config(
        context.config
    ).get_current_head()

    new_rev_id = int(head_revision) + 1 if head_revision else 1

    migration_script.rev_id = "{0:04}".format(new_rev_id)


def exclude_tables_from_config(config_):
    tables_ = config_.get("tables", None)
    if tables_ is not None:
        tables_ = tables_.split(",")
    return tables_


def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and name in exclude_tables_from_config(
        config.get_section("alembic:exclude")
    ):
        return False

    return True


def run_migrations_offline():
    url = settings.db.get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        include_object=include_object,
        process_revision_directives=process_revision_directives,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.db.get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            include_object=include_object,
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
