import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ─── 1) Make sure alembic can import your models ───────────────────────────────
# Adjust the path if your backend folder lives elsewhere
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

# ─── 2) Import your SQLAlchemy Base.metadata ─────────────────────────────────
# backend/models.py should define Base = declarative_base()
from backend.models import Base
target_metadata = Base.metadata

# ─── 3) Alembic Config object ────────────────────────────────────────────────
config = context.config

# If you prefer env vars for the URL, you can override here:
# url = os.getenv("DATABASE_URL")
# if url:
#     config.set_main_option("sqlalchemy.url", url)

# ─── 4) Set up Python logging per alembic.ini ─────────────────────────────────
fileConfig(config.config_file_name)

# ─── 5) “run_migrations_online()” below will now see your metadata ─────────────


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
