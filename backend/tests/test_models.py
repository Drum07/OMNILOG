
from sqlalchemy import inspect

from backend.app.db.session import engine
from backend.app.db.base import Base
import backend.app.models


def test_database_connection():
    with engine.connect() as connection:
        assert connection.exec_driver_sql("SELECT 1").scalar() == 1


def test_all_models_registered():
    assert len(Base.metadata.tables) == 18


def test_models_match_database():
    inspector = inspect(engine)

    database_tables = set(inspector.get_table_names())
    model_tables = set(Base.metadata.tables.keys())

    missing_tables = model_tables - database_tables

    assert not missing_tables, (
        f"Tabelas ausentes no MySQL: {missing_tables}"
    )


def test_all_tables_have_primary_keys():
    inspector = inspect(engine)

    for table_name in Base.metadata.tables:
        primary_keys = inspector.get_pk_constraint(table_name)
        assert primary_keys["constrained_columns"], (
            f"Tabela sem chave primária: {table_name}"
        )
