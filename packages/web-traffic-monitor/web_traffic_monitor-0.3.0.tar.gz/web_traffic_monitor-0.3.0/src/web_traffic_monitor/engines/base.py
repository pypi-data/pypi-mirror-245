from web_traffic_monitor import LOGGER

class DB:

    def __init__( self, schema ):

        self.schema = schema
        tables = self.get_tables()
        for table in self.schema.TABLES:
            if self.schema.TABLES[ table ] not in tables: 
                self.create_table( table )

    def execute_and_commit( self, string: str ):
        self.execute( string )
        self.commit()

    def get_tables( self ):
        tables =  [ row[0] for row in self.query( self.GET_TABLES_QUERY ) ]
        LOGGER.debug( 'found existing tables: {}'.format( tables ))
        return tables

    def create_table( self, table: str ):
        LOGGER.debug( 'creating table: {}'.format( table ))
        string = self.schema.create_table_query( table )
        self.execute( string )

    @staticmethod
    def query_wrap( func ):
        def wrapper( self, string: str ):
            LOGGER.debug( 'querying: {}'.format( string ) )
            return func( self, string )
        return wrapper

    @staticmethod
    def execute_wrap( func ):
        def wrapper( self, string: str ):
            LOGGER.debug( 'executing: {}'.format( string ) )
            return func( self, string )
        return wrapper

    @staticmethod
    def commit_wrap( func ):
        def wrapper( self ):
            LOGGER.debug( 'committing' )
            return func( self )
        return wrapper
