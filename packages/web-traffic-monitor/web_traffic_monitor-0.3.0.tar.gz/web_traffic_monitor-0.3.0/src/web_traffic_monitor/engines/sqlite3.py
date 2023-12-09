from web_traffic_monitor.engines.base import DB as BaseDB
import sqlite3

class DB( BaseDB ):

    GET_TABLES_QUERY = 'SELECT name FROM sqlite_master WHERE type="table";'

    def __init__( self, schema, *args, path='web_traffic_monitor.db', **kwargs ):
        self.conn = sqlite3.connect( path, check_same_thread=False )
        BaseDB.__init__( self, schema )

    @BaseDB.query_wrap
    def query( self, string: str ):
        return self.conn.execute( string ).fetchall()
    
    @BaseDB.execute_wrap
    def execute( self, string: str ):
        self.conn.execute( string )

    @BaseDB.commit_wrap
    def commit( self ):
        self.conn.commit()

