import logging


from logging.config import fileConfig
from application.app import create_app
from flask import current_app
from application.db.models import (
    User,
    Profile,
    Activity,
    Journal,
    Plan,
    RoleStatus,
)
from alembic import context

# Alembic Config object to access the values in the .ini file
config = context.config

# Interpret the config file for Python logging
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

# Explicitly create the Flask app to use in the Alembic context
def get_app():
    app = create_app()  # Create the app
    return app


def get_engine():
    app = get_app()  # Create the app
    with app.app_context():  # Ensure the app context is available
        try:
            # Access the engine only after the app context is available
            return current_app.extensions["migrate"].db.get_engine()
        except (TypeError, AttributeError):
            return current_app.extensions["migrate"].db.engine


def get_engine_url():
    try:
        # Use the engine to generate the URL
        return (
            get_engine()
            .url.render_as_string(hide_password=False)
            .replace("%", "%%")  # noqa E501
        )
    except AttributeError:
        return str(get_engine().url).replace("%", "%%")


# Set the main option for sqlalchemy.url in the config
config.set_main_option("sqlalchemy.url", get_engine_url())
# We need to get the metadata *after* the app context is available
def get_metadata():
    app = get_app()  # Create the app instance
    with app.app_context():  # Ensure the app context is available
        target_db = current_app.extensions["migrate"].db
        if hasattr(target_db, "metadatas"):
            return target_db.metadatas[None]
        return target_db.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""

    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("No changes in schema detected.")

    conf_args = current_app.extensions["migrate"].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=get_metadata(), **conf_args
        )

        with context.begin_transaction():
            context.run_migrations()


# Ensure the app context is active when running the migrations
if context.is_offline_mode():
    run_migrations_offline()
else:
    app = get_app()  # Explicitly create
