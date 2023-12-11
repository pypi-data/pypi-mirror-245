

from sqlalchemy import Connection
from sqlalchemy import inspect
from sqlalchemy.engine import Engine


__all__ = [
    'MetaDataHolder',
    'AlchemyRohanDatabaseError'
]


class AlchemyRohanDatabaseError(Exception): ...


class MetaDataHolder:
    def __init__(
        self,
        engine: Engine,
        table: str
        ):
        
        self._chk_conn(engine)
        
        self.name = table
        self.rdbms = engine.name

        inspector = inspect(engine)
        self.schema = inspector.default_schema_name
        self.columns = self._get_columns(inspector, table)
        self.primary_key = self._get_primary_key(inspector, table)
        self.foreign_keys = self._get_foreign_keys(inspector, table)
        self.multi_foreign_keys = self._get_multi_foreign_keys(inspector)
        self.unique_keys = self._get_unique_cons(inspector, table)

    @staticmethod
    def _chk_conn(engine) -> None:
        try:
            Connection(engine)
        except Exception as e:
            raise AlchemyRohanDatabaseError(e)

    @staticmethod
    def _get_columns(inspector, table):
        try:
            return inspector.get_columns(table)
        except Exception as e:
            raise AlchemyRohanDatabaseError(e)

    @staticmethod
    def _get_primary_key(inspector, table):
        try:
            return inspector.get_pk_constraint(table)
        except Exception as e:
            raise AlchemyRohanDatabaseError(e)
    
    @staticmethod
    def _get_foreign_keys(inspector, table):
        try:
            return inspector.get_foreign_keys(table)
        except Exception as e:
            raise AlchemyRohanDatabaseError(e)
    
    @staticmethod
    def _get_multi_foreign_keys(inspector):
        try:
            return inspector.get_multi_foreign_keys()
        except Exception as e:
            raise AlchemyRohanDatabaseError(e)

    @staticmethod
    def _get_unique_cons(inspector, table):
        try:
            return inspector.get_unique_constraints(table)
        except Exception as e:
            raise AlchemyRohanDatabaseError(e)