# slim-helper

```shell
pip install slim-helpe[postgres] # optional dependency: psycopg
pip install slim-helpe[oracle] # optional dependency: oracledb
pip install slim-helpe[all] # all optional dependency
```
## database
```python
from from slim_helper.database import DbHelper,SqliteParams,PostgresParams,OracleParams

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
```
## common
```python
# retry decorator
retry(times: int, interval_secs: int)
# timer decorator
timer(func: Callable)
# null value logic function
nvl(*args)
```
## display
```python
# convert number to SI metric prefix
si_prefix(value: float | int)
# convert number to IEC metric prefix
iec_prefix(value: int)
```
## io
```python
# line reader class
LineReader(
    file: Path,
    max_line_size: int,
    sep: bytes = b"\n",
    start_pos: int = 0,
    end_pos: int | None = None,
)
# Get range
read_range_distribute(
    file: Path, n: int, sep: bytes | None = None
)
```
## process
```python
# Execute command function
execute_command(
    cmd: Sequence[str],
    stdin: bytes | None = None,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    dry: bool = False,
)
```
## security
```python
# SHA3-512
sha3_512(obj: Path | str | bytes)
```
## task
```python
# Parallel task executor
ParallelWorker(
    callback: Callable,
    parallel: int = 1,
    max_input: int = 0,
    max_output: int = 0,
)
```