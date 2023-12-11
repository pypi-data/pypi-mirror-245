from capsphere.data.db.connector.abstract import AbstractDatabaseConnection, AbstractDatabaseConnectionAsync


class DbQueryService:
    def __init__(self, db_connection: AbstractDatabaseConnection):
        self.db_connection = db_connection

    def execute(self, query, params=None, fetch_results=True):
        with self.db_connection.get_connection():
            return self.db_connection.execute_single_query(query, params, fetch_results)


class DbQueryServiceAsync:
    def __init__(self, db_connection: AbstractDatabaseConnectionAsync):
        self.db_connection = db_connection

    async def execute_async(self, query, params=None, fetch_results=True):
        async with self.db_connection.get_connection_async():
            return await self.db_connection.execute_single_query_async(query, params, fetch_results)
