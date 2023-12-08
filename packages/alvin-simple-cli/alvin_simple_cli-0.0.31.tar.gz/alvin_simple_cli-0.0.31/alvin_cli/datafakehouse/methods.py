# ruff: noqa: A002
import sys

import typer

from alvin_cli.datafakehouse.grpc_client.datafakehouse_client import (
    InvalidSQLDialectValidationError,
    create_db_instance_client,
    list_catalogs_client,
    snapshot_db_instance_client,
)
from alvin_cli.datafakehouse.models import FORMAT, SQLDialect
from alvin_cli.utils.common_arguments import BRIGHT_GREEN_COLOR_TYPER
from alvin_cli.utils.helper_functions import typer_secho_raise

app = typer.Typer(add_completion=False)


NAME_OPT = typer.Option(
    default="alvin_datafakehouse",
    help=typer.style(
        "Name of the db instance", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True,
    ),
)

SQL_DIALECT_OPT = typer.Option(
    "--sql-dialect",
    help=typer.style(
        "SQL Dialect used by the db instance", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True,
    ),
)

FORMAT_OPT = typer.Option(
    default=FORMAT.PLAIN.value,
    help=typer.style(
        "output format", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True,
    ),
)

CATALOG_OPT = typer.Option(
    default="",
    help=typer.style(
        "catalog id used by db instance", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True,
    ),
)

INSTANCE_OPT = typer.Option(
    default="",
    help=typer.style(
        "id of the db instance", fg=BRIGHT_GREEN_COLOR_TYPER, bold=True,
    ),
)

@app.command()
def create_db_instance(
    *,
    name: str = NAME_OPT,
    catalog: str = CATALOG_OPT,
    sql_dialect: SQLDialect = SQL_DIALECT_OPT,
    format: FORMAT = FORMAT_OPT,
) -> None:
    try:
        create_db_instance_client(name=name, sql_dialect=sql_dialect, catalog_id=catalog, format=format)
    except InvalidSQLDialectValidationError as err:
        typer_secho_raise(f"Can't create db instance: {err.detail}", "RED")
        sys.exit(1)

@app.command()
def list_catalogs() -> None:
    try:
        list_catalogs_client()
    except InvalidSQLDialectValidationError as err:
        typer_secho_raise(f"Can't create db instance: {err.detail}", "RED")
        sys.exit(1)

@app.command()
def store_snapshot(
    db_instance_id: str = NAME_OPT,
) -> None:
    try:
        snapshot_db_instance_client(db_instance_id=db_instance_id)
    except InvalidSQLDialectValidationError as err:
        typer_secho_raise(f"Can't create db instance: {err.detail}", "RED")
        sys.exit(1)
