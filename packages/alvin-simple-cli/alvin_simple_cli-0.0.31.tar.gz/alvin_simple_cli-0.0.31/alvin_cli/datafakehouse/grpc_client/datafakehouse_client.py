# ruff: noqa: A002
from typing import Any, List

import grpc

from alvin_cli.config import settings
from alvin_cli.datafakehouse.grpc_generated import (
    datafakehouse_pb2 as pb2,
)
from alvin_cli.datafakehouse.grpc_generated import datafakehouse_pb2_grpc as pb2_grpc
from alvin_cli.datafakehouse.models import FORMAT, SQLDialect
from alvin_cli.utils.helper_functions import console


class InvalidSQLDialectValidationError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail


def _create_channel(url: str) -> grpc.Channel:
    if ":443" not in url:
        url = url.replace("[::]", "localhost")
        return grpc.insecure_channel(url)
    call_credentials = grpc.metadata_call_credentials(
        lambda context, callback: callback(None, None),
    )
    ssl_creds = grpc.ssl_channel_credentials()
    composite_credentials = grpc.composite_channel_credentials(
        ssl_creds,
        call_credentials,
    )
    return grpc.secure_channel(url, composite_credentials)

def grpc_to_enum_name(*, enum_class: Any, value: int) -> Any:  # noqa: ANN401
    """Get the str Enum Name from a GRPCEnum."""

    return enum_class.Name(value)  # type: ignore

def dialect(catalog: pb2.Catalog) -> str:
    return grpc_to_enum_name(enum_class=pb2.SQLDialect, value=catalog.sql_dialect)


def create_db_instance_client(*,
    name: str,
    sql_dialect: SQLDialect,
    catalog_id: str = "",
    format: FORMAT,
) -> None:
    if sql_dialect != sql_dialect.BIGQUERY:
        raise InvalidSQLDialectValidationError(f"Unable to map {sql_dialect=} to a valid value")
    if not catalog_id:
        console.print("""[bold red] catalog not provided. Using latest""")
        catalogs = [cat for cat in get_catalogs() if dialect(cat) == sql_dialect.value]
        catalog = catalogs[0]
        catalog_id = catalog.catalog_id

    assert settings.alvin_datafakehouse_api_url
    with _create_channel(settings.alvin_datafakehouse_api_url) as channel:
        stub = pb2_grpc.DatafakehouseStub(channel)
        summary_request = pb2.CreateDbInstanceRequest(name=name, catalog_id=catalog_id, sql_dialect=sql_dialect.value)
        summary_res = stub.CreateDbInstance(summary_request, metadata=[("x-api-key", settings.alvin_api_token)])

        if format == FORMAT.PLAIN:
            console.print(summary_res)
            return
        if format == FORMAT.ENV:
            console.print(f"""
export ALVIN_DB_INSTANCE_ID="{summary_res.db_instance_id}"
export ALVIN_DB_TOKEN="{summary_res.db_token}"
    """)
            return
        raise RuntimeError("Internal Error: invalid code path")

def get_catalogs() -> List[pb2.Catalog]:
    with _create_channel(settings.alvin_datafakehouse_api_url) as channel:
        stub = pb2_grpc.DatafakehouseStub(channel)
        list_catalog_req = pb2.ListCatalogsRequest()
        catalogs = stub.ListCatalogs(list_catalog_req, metadata=[("x-api-key", settings.alvin_api_token)])
        return list(catalogs)


def list_catalogs_client() -> None:
    assert settings.alvin_datafakehouse_api_url
    catalogs = get_catalogs()
    for catalog in catalogs:
        cat = [
            ("id", catalog.catalog_id),
            ("name", catalog.name),
            ("created_time", catalog.created_time.ToJsonString()),
            ("dialect", grpc_to_enum_name(enum_class=pb2.SQLDialect, value=catalog.sql_dialect)),
        ]
        console.print("""""")
        for (field, value) in cat:
            console.print(f"""{field}={value}""")
        console.print("""""")

def snapshot_db_instance(*, db_instance_id: str) -> pb2.Catalog:
    with _create_channel(settings.alvin_datafakehouse_api_url) as channel:
        stub = pb2_grpc.DatafakehouseStub(channel)
        list_catalog_req = pb2.SnapshotCatalogRequest(db_instance_id=db_instance_id)
        return stub.SnapshotCatalog(list_catalog_req, metadata=[("x-api-key", settings.alvin_api_token)])
def snapshot_db_instance_client(*, db_instance_id: str) -> None:
    assert settings.alvin_datafakehouse_api_url
    catalog = snapshot_db_instance(db_instance_id=db_instance_id)
    cat = [
        ("id", catalog.catalog_id),
        ("name", catalog.name),
        ("created_time", catalog.created_time.ToJsonString()),
        ("dialect", grpc_to_enum_name(enum_class=pb2.SQLDialect, value=catalog.sql_dialect)),
    ]
    console.print("""""")
    for (field, value) in cat:
        console.print(f"""{field}={value}""")
    console.print("""""")
