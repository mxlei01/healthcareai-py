import urllib
import sqlalchemy

import healthcareai.common.database_library_validators as hcai_db_library

try:
    # Note we don't want to force pyodbc as a requirement
    import pyodbc

    pyodbc_is_loaded = True
except ImportError:
    pyodbc_is_loaded = False

try:
    # Note we don't want to force sqlite3 as a requirement
    import sqlite3

    sqlite3_is_loaded = True
except ImportError:
    sqlite3_is_loaded = False


def build_mssql_trusted_connection_string(server, database):
    """ Given a server and database name, build a Trusted Connection MSSQL connection string """
    return 'DRIVER={ODBC Driver 13 for SQL Server};Server=' + server + ';Database=' + database + ';Trusted_Connection=yes;'


def build_mysql_connection_string(server, database, userid, password):
    """ Given a server, database, userid, and password, create a MSSQL connection string """
    return 'DRIVER={ODBC Driver 13 for SQL Server};Server=' + server + ';Database=' + database + ';Uid=' + userid \
           + ';Pwd=' + password


def build_sqlite_engine(file_path):
    """ Build an sqlite engine. """
    hcai_db_library.validate_sqlite3_is_loaded()
    engine = sqlite3.connect(file_path)
    return engine


def build_sqlite_in_memory_connection_string():
    # TODO stub
    pass
    # return 'Data Source=:memory:;Version=3;New=True;'


def build_mssql_engine_using_trusted_connections(server, database, userid=None, password=None, secure_connection=True):
    """
    Given a server and database name, build a Trusted Connection MSSQL database engine. NOTE: Requires `pyodbc`
    
    Args:
        server (str): Server name 
        database (str): Database name
        userid (str): User id
        password (str): User password
        secure_connection (bool): Determines if we should use a mssql secure connection, where your credentials
            are your windows login.

    Returns:
        sqlalchemy.engine.base.Engine: an sqlalchemy connection engine
    """
    hcai_db_library.validate_pyodbc_is_loaded()

    if secure_connection:
        connection_string = build_mssql_trusted_connection_string(server, database)
    else:
        connection_string = build_mysql_connection_string(server, database, userid, password)
    params = urllib.parse.quote_plus(connection_string)
    engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))

    return engine
