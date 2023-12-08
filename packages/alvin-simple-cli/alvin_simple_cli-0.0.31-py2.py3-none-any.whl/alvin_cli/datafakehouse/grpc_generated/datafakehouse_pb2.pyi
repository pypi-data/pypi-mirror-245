from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SQLDialect(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    BIGQUERY: _ClassVar[SQLDialect]
    SNOWFLAKE: _ClassVar[SQLDialect]

class CatalogChangeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    CREATED: _ClassVar[CatalogChangeType]
    DELETED: _ClassVar[CatalogChangeType]
    CHANGED: _ClassVar[CatalogChangeType]

class CatalogType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    METADATA_SYNC: _ClassVar[CatalogType]
    DBINSTANCE_OUTPUT: _ClassVar[CatalogType]

class FieldType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    TIMESTAMP: _ClassVar[FieldType]
    STRING: _ClassVar[FieldType]
    INT64: _ClassVar[FieldType]
    FLOAT64: _ClassVar[FieldType]
    BOOL: _ClassVar[FieldType]
BIGQUERY: SQLDialect
SNOWFLAKE: SQLDialect
CREATED: CatalogChangeType
DELETED: CatalogChangeType
CHANGED: CatalogChangeType
METADATA_SYNC: CatalogType
DBINSTANCE_OUTPUT: CatalogType
TIMESTAMP: FieldType
STRING: FieldType
INT64: FieldType
FLOAT64: FieldType
BOOL: FieldType

class CatalogChange(_message.Message):
    __slots__ = ["fqn_id", "entity_type", "change_type"]
    FQN_ID_FIELD_NUMBER: _ClassVar[int]
    ENTITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    fqn_id: str
    entity_type: str
    change_type: CatalogChangeType
    def __init__(self, fqn_id: _Optional[str] = ..., entity_type: _Optional[str] = ..., change_type: _Optional[_Union[CatalogChangeType, str]] = ...) -> None: ...

class DiffCatalogsRequest(_message.Message):
    __slots__ = ["old_catalog_id", "new_catalog_id"]
    OLD_CATALOG_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_CATALOG_ID_FIELD_NUMBER: _ClassVar[int]
    old_catalog_id: str
    new_catalog_id: str
    def __init__(self, old_catalog_id: _Optional[str] = ..., new_catalog_id: _Optional[str] = ...) -> None: ...

class DiffCatalogsResponse(_message.Message):
    __slots__ = ["changes", "total_changes"]
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CHANGES_FIELD_NUMBER: _ClassVar[int]
    changes: _containers.RepeatedCompositeFieldContainer[CatalogChange]
    total_changes: int
    def __init__(self, changes: _Optional[_Iterable[_Union[CatalogChange, _Mapping]]] = ..., total_changes: _Optional[int] = ...) -> None: ...

class CreateDbInstanceRequest(_message.Message):
    __slots__ = ["sql_dialect", "name", "catalog_id"]
    SQL_DIALECT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CATALOG_ID_FIELD_NUMBER: _ClassVar[int]
    sql_dialect: SQLDialect
    name: str
    catalog_id: str
    def __init__(self, sql_dialect: _Optional[_Union[SQLDialect, str]] = ..., name: _Optional[str] = ..., catalog_id: _Optional[str] = ...) -> None: ...

class DbInstance(_message.Message):
    __slots__ = ["db_instance_id", "org_id", "name", "created_time", "db_token", "sql_dialect", "catalog_id"]
    DB_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_TIME_FIELD_NUMBER: _ClassVar[int]
    DB_TOKEN_FIELD_NUMBER: _ClassVar[int]
    SQL_DIALECT_FIELD_NUMBER: _ClassVar[int]
    CATALOG_ID_FIELD_NUMBER: _ClassVar[int]
    db_instance_id: str
    org_id: str
    name: str
    created_time: _timestamp_pb2.Timestamp
    db_token: str
    sql_dialect: SQLDialect
    catalog_id: str
    def __init__(self, db_instance_id: _Optional[str] = ..., org_id: _Optional[str] = ..., name: _Optional[str] = ..., created_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., db_token: _Optional[str] = ..., sql_dialect: _Optional[_Union[SQLDialect, str]] = ..., catalog_id: _Optional[str] = ...) -> None: ...

class Catalog(_message.Message):
    __slots__ = ["catalog_id", "org_id", "created_time", "type", "name", "path", "expires_time", "db_instance_id", "sql_dialect"]
    CATALOG_ID_FIELD_NUMBER: _ClassVar[int]
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_TIME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_TIME_FIELD_NUMBER: _ClassVar[int]
    DB_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    SQL_DIALECT_FIELD_NUMBER: _ClassVar[int]
    catalog_id: str
    org_id: str
    created_time: _timestamp_pb2.Timestamp
    type: CatalogType
    name: str
    path: str
    expires_time: _timestamp_pb2.Timestamp
    db_instance_id: str
    sql_dialect: SQLDialect
    def __init__(self, catalog_id: _Optional[str] = ..., org_id: _Optional[str] = ..., created_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., type: _Optional[_Union[CatalogType, str]] = ..., name: _Optional[str] = ..., path: _Optional[str] = ..., expires_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., db_instance_id: _Optional[str] = ..., sql_dialect: _Optional[_Union[SQLDialect, str]] = ...) -> None: ...

class CreateCatalogFromDbInstanceRequest(_message.Message):
    __slots__ = ["db_instance_id", "db_token"]
    DB_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    DB_TOKEN_FIELD_NUMBER: _ClassVar[int]
    db_instance_id: str
    db_token: str
    def __init__(self, db_instance_id: _Optional[str] = ..., db_token: _Optional[str] = ...) -> None: ...

class CreateCatalogRequest(_message.Message):
    __slots__ = ["type", "name", "path", "sql_dialect", "expires_time"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    SQL_DIALECT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_TIME_FIELD_NUMBER: _ClassVar[int]
    type: CatalogType
    name: str
    path: str
    sql_dialect: SQLDialect
    expires_time: _timestamp_pb2.Timestamp
    def __init__(self, type: _Optional[_Union[CatalogType, str]] = ..., name: _Optional[str] = ..., path: _Optional[str] = ..., sql_dialect: _Optional[_Union[SQLDialect, str]] = ..., expires_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class SnapshotCatalogRequest(_message.Message):
    __slots__ = ["db_instance_id"]
    DB_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    db_instance_id: str
    def __init__(self, db_instance_id: _Optional[str] = ...) -> None: ...

class CreateCatalogResponse(_message.Message):
    __slots__ = ["catalog"]
    CATALOG_FIELD_NUMBER: _ClassVar[int]
    catalog: Catalog
    def __init__(self, catalog: _Optional[_Union[Catalog, _Mapping]] = ...) -> None: ...

class ListCatalogsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetCatalogRequest(_message.Message):
    __slots__ = ["catalog_id"]
    CATALOG_ID_FIELD_NUMBER: _ClassVar[int]
    catalog_id: str
    def __init__(self, catalog_id: _Optional[str] = ...) -> None: ...

class GetDbInstanceRequest(_message.Message):
    __slots__ = ["db_instance_id"]
    DB_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    db_instance_id: str
    def __init__(self, db_instance_id: _Optional[str] = ...) -> None: ...

class ExitDbInstanceRequest(_message.Message):
    __slots__ = ["db_instance_id", "db_token"]
    DB_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    DB_TOKEN_FIELD_NUMBER: _ClassVar[int]
    db_instance_id: str
    db_token: str
    def __init__(self, db_instance_id: _Optional[str] = ..., db_token: _Optional[str] = ...) -> None: ...

class ExitDbInstanceResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class RunSQLQueryRequest(_message.Message):
    __slots__ = ["db_instance_id", "sql", "db_token"]
    DB_INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    SQL_FIELD_NUMBER: _ClassVar[int]
    DB_TOKEN_FIELD_NUMBER: _ClassVar[int]
    db_instance_id: str
    sql: str
    db_token: str
    def __init__(self, db_instance_id: _Optional[str] = ..., sql: _Optional[str] = ..., db_token: _Optional[str] = ...) -> None: ...

class RunSQLQueryResponse(_message.Message):
    __slots__ = ["success", "error", "data"]
    class ErrorBody(_message.Message):
        __slots__ = ["messages"]
        class ErrorMessage(_message.Message):
            __slots__ = ["severity", "error_type", "start_position", "end_position", "relation_entity"]
            SEVERITY_FIELD_NUMBER: _ClassVar[int]
            ERROR_TYPE_FIELD_NUMBER: _ClassVar[int]
            START_POSITION_FIELD_NUMBER: _ClassVar[int]
            END_POSITION_FIELD_NUMBER: _ClassVar[int]
            RELATION_ENTITY_FIELD_NUMBER: _ClassVar[int]
            severity: str
            error_type: str
            start_position: int
            end_position: int
            relation_entity: str
            def __init__(self, severity: _Optional[str] = ..., error_type: _Optional[str] = ..., start_position: _Optional[int] = ..., end_position: _Optional[int] = ..., relation_entity: _Optional[str] = ...) -> None: ...
        MESSAGES_FIELD_NUMBER: _ClassVar[int]
        messages: _containers.RepeatedCompositeFieldContainer[RunSQLQueryResponse.ErrorBody.ErrorMessage]
        def __init__(self, messages: _Optional[_Iterable[_Union[RunSQLQueryResponse.ErrorBody.ErrorMessage, _Mapping]]] = ...) -> None: ...
    class Data(_message.Message):
        __slots__ = ["schema", "total_rows", "rows"]
        SCHEMA_FIELD_NUMBER: _ClassVar[int]
        TOTAL_ROWS_FIELD_NUMBER: _ClassVar[int]
        ROWS_FIELD_NUMBER: _ClassVar[int]
        schema: SQLSchema
        total_rows: int
        rows: _containers.RepeatedCompositeFieldContainer[ResultRow]
        def __init__(self, schema: _Optional[_Union[SQLSchema, _Mapping]] = ..., total_rows: _Optional[int] = ..., rows: _Optional[_Iterable[_Union[ResultRow, _Mapping]]] = ...) -> None: ...
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error: RunSQLQueryResponse.ErrorBody
    data: RunSQLQueryResponse.Data
    def __init__(self, success: bool = ..., error: _Optional[_Union[RunSQLQueryResponse.ErrorBody, _Mapping]] = ..., data: _Optional[_Union[RunSQLQueryResponse.Data, _Mapping]] = ...) -> None: ...

class SQLField(_message.Message):
    __slots__ = ["name", "type"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: FieldType
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[FieldType, str]] = ...) -> None: ...

class SQLSchema(_message.Message):
    __slots__ = ["fields"]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedCompositeFieldContainer[SQLField]
    def __init__(self, fields: _Optional[_Iterable[_Union[SQLField, _Mapping]]] = ...) -> None: ...

class ResultRow(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...
