import mysql.connector


class DBError(Exception):
    pass


class DBCredentialsError(DBError):
    pass


class DBSQLError(DBError):
    pass


class DBConnectionError(DBError):
    pass


class CreateMySQLCursor:
    def __init__(self, config: dict = None):
        self.config = config
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor()
            return self.cursor
        except mysql.connector.InterfaceError as err:
            raise DBConnectionError(err) from err
        except mysql.connector.ProgrammingError as err:
            raise DBCredentialsError(err) from err

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        if exc_type is mysql.connector.ProgrammingError:
            raise DBSQLError(exc_val) from exc_val
