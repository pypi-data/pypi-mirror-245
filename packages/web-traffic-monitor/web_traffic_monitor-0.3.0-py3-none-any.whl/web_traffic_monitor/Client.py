from web_traffic_monitor import LOGGER
import datetime
import importlib

def get_current_datetime():
    dt = datetime.datetime.utcnow()
    return dt.replace( tzinfo=datetime.timezone.utc )

class Client:

    def __init__( self, *engine_args, db_inst=None, engine='sqlite3', schema_inst=None, schema='base', **engine_kwargs ):

        LOGGER.info( 'initializing web_traffic_monitor with engine ({}) and schema ({})'.format( engine, schema ) )

        if schema_inst is None:
            self.schema = getattr( importlib.import_module( '.'+schema, package='web_traffic_monitor.schemas' ) , 'Schema' )
        else: 
            self.schema = schema_inst   

        if db_inst is None:
            self.db = getattr( importlib.import_module( '.'+engine, package='web_traffic_monitor.engines' ) , 'DB' )( self.schema, *engine_args, **engine_kwargs )
        else:
            self.db = db_inst  

    def log_visit( self, slug: str, dt: datetime.datetime = get_current_datetime() ):
        
        """log a visit for given slug, defaults to current time, make sure DT has timezone info stored"""

        LOGGER.info( 'logging visit for slug ({}) at time ({})'.format( slug, dt ))
        string = self.schema.log_visit_query( slug, dt )
        self.db.execute_and_commit( string )

    def get_active_redirect( self, slug: str ):

        """get the active redirect of the given slug, returns None if none are active"""

        string = self.schema.get_active_redirect_query( slug )
        result = self.db.query( string )
        if len(result) == 0:
            active = None
        else:
            active = result[0][0]

        LOGGER.info( 'active redirect ({}) for slug ({})'.format( active, slug ) )
        return active

    def add_redirect( self, slug, redirect, dt: datetime.datetime = get_current_datetime() ):

        """deactivates any active redirect for given slug, and adds a new redirect, defaults to current time"""

        self.deactive_redirect( slug, dt )
        LOGGER.info( 'adding redirect ({}) to slug ({}) at time ({})'.format( redirect, slug, dt ) )
        string = self.schema.add_redirect_query( slug, redirect, dt )
        self.db.execute_and_commit( string )

    def deactive_redirect( self, slug, dt: datetime.datetime = get_current_datetime() ):
        
        """deactivates any active redirect for given slug, defaults END_DATETIME to be current time"""

        LOGGER.info( 'deactivating redirects for slug ({}) at time ({})'.format( slug, dt ) )
        string = self.schema.deactivate_redirect_query( slug, dt )
        self.db.execute_and_commit( string )

    