from dataclasses import dataclass
from typing import Sequence


class IDbHelper:
    """
    IDbHelper interface (support <with> statement)
    """

    def __init(self):
        self._db_connection = None

    def open(self):
        """open database connection"""
        raise NotImplementedError("IDbHelper.open() is not implemented")

    def close(self):
        """close database connection"""
        if self._db_connection:
            self.commit()
            self._db_connection.close()
            self._db_connection = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def query(
        self, sql: str, params: Sequence | None = None
    ) -> tuple[Sequence, Sequence[str]]:
        """query SQL with parameters

        Args:
            sql (str): SQL string
            params (Sequence | None, optional): parameters. Defaults to None.

        Returns:
            tuple[Sequence, Sequence[str]]: result list,columns
        """
        cursor = self._db_connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        columns = [description[0] for description in cursor.description]
        result = cursor.fetchall()
        cursor.close()
        return result, columns

    def execute(self, sql: str, params: Sequence | None = None) -> int:
        """execute SQL with parameters

        Args:
            sql (str): SQL string
            params (Sequence | None, optional): parameters. Defaults to None.

        Returns:
            int: number of rows affected
        """
        raise NotImplementedError("IDbHelper.execute() is not implemented")

    def commit(self):
        """commit"""
        self._db_connection.commit()

    def rollback(self):
        """rollback"""
        self._db_connection.rollback()


@dataclass
class SqliteParams:
    file_name: str


@dataclass
class PostgresParams:
    host: str
    port: int
    dbname: str
    user: str
    password: str


@dataclass
class OracleParams:
    host: str
    port: int
    service_name: str
    user: str
    password: str
    encoding: str | None = "UTF-8"
    mode: str | None = None


class DbHelper(IDbHelper):
    '''
    constructor:
        config: Database connection params
    usage:
        # SQlite:
        config = SqliteParams(file_name=':memory:')
        with DbHelper(config) as db:
            db.execute("""
                 CREATE TABLE foo (
                 id INTEGER PRIMARY KEY ,
                 txt TEXT
                 )
                 """)
            db.execute("insert into foo values(?,?)", [1, 'a'])
            db.execute("insert into foo values(?,?)", [2, 'b'])
            db.execute("insert into foo values(?,?)", [3, 'c'])
            db.commit()
            result,columns = db.query("select * from foo where id=? and txt=?", [2, 'b'])
            db.execute("drop table foo")
            print(result,columns)
        # Or
        db = DbHelper(config)
        db.open()
        ...
        db.close()


        # PostgreSQL:
        config=PostgresParams(host='localhost',port=5432,dbname='postgres',user='postgres',password='postgres')
        with DbHelper(config) as db:
            db.execute("""
                CREATE TABLE  IF NOT EXISTS foo (
                id INTEGER PRIMARY KEY ,
                txt TEXT
                )
                """)
            db.execute("insert into foo values(%s,%s)", [1, 'a'])
            db.execute("insert into foo values(%s,%s)", [2, 'b'])
            db.execute("insert into foo values(%s,%s)", [3, 'c'])
            db.commit()
            result,columns = db.query("select * from foo where id=%s and txt=%s", [2, 'b'])
            db.execute("drop table foo")
            print(result,columns)
        # Or
        db = DbHelper(config)
        db.open()
        ...
        db.close()


        # Oracle:
        config = OracleParams(host='localhost',port=1521,service_name='orcl',user='orcl',password='orcl')
        with DbHelper(config) as db:
            db.execute("""
                CREATE TABLE FOO (
                id INTEGER PRIMARY KEY ,
                txt VARCHAR2(100)
                )
                """)
            db.execute("insert into FOO values(:1,:2)", [1, 'a'])
            db.execute("insert into FOO values(:1,:2)", [2, 'b'])
            db.execute("insert into FOO values(:1,:2)", [3, 'c'])
            db.commit()
            result,columns = db.query("select * from foo where id=:1 and txt=:2", [2, 'b'])
            db.execute("drop table FOO")
            print(result,columns)
        # Or
        db = DbHelper(config)
        db.open()
        ...
        db.close()
    '''

    def __init__(self, db_config: SqliteParams | PostgresParams | OracleParams):
        """
        Args:
            db_config (SqliteParams | PostgresParams | OracleParams): database onnection config
        """
        self._db_connection = None
        self._config = db_config
        self._config_type = type(self._config)
        supported_db_configs = (SqliteParams, PostgresParams, OracleParams)
        if self._config_type not in supported_db_configs:
            raise TypeError(f"Unknown database config: {type(db_config)}")

    def open(self):
        if not self._db_connection:
            if self._config_type is SqliteParams:
                import sqlite3

                dbname = self._config.file_name
                self._db_connection = sqlite3.connect(dbname)
            elif self._config_type is PostgresParams:
                import psycopg
                from psycopg.conninfo import make_conninfo

                conn_info = make_conninfo(
                    host=self._config.host,
                    port=self._config.port,
                    dbname=self._config.dbname,
                    user=self._config.user,
                    password=self._config.password,
                )
                self._db_connection = psycopg.connect(conn_info, autocommit=False)
            elif self._config_type is OracleParams:
                import oracledb

                cp = oracledb.ConnectParams(
                    host=self._config.host,
                    port=self._config.port,
                    service_name=self._config.service_name,
                    user=self._config.user,
                    password=self._config.password,
                    mode=self._config.mode,
                    encoding=self._config.encoding,
                )
                self._db_connection = oracledb.connect(params=cp)
        else:
            raise RuntimeError("Database connection already exists")

    def execute(self, sql: str, params: Sequence | None = None) -> int:
        cursor = self._db_connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        if self._config_type is SqliteParams:
            result = self._db_connection.total_changes
        elif self._config_type is PostgresParams:
            result = cursor.rowcount
        elif self._config_type is OracleParams:
            result = cursor.rowcount
        cursor.close()
        return result
