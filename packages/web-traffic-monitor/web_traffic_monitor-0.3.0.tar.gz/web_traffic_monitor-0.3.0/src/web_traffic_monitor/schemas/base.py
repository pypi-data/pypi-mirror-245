import datetime

class Schema:

    DT_FORMAT = '%Y-%m-%d %H:%M:%S.%f%z'

    TABLES = {
        'VISITS': 'visits',
        'REDIRECTS': 'redirects'
    }

    COLUMNS = {
        'VISITS': {
            'SLUG': 'slug',
            'DATETIME': 'datetime'
        },
        'REDIRECTS': {
            'ID': 'id',
            'SLUG': 'slug',
            'REDIRECT': 'redirect',
            'START_DATETIME': 'start_datetime',
            'END_DATETIME': 'end_datetime'
        }
    }

    SCHEMA = {
        'VISITS': {
            'COLUMNS':{
                'SLUG':     [ 'TEXT', 'NOT NULL' ],
                'DATETIME': [ 'TEXT', 'NOT NULL' ]
            }
        },
        'REDIRECTS': {
            'COLUMNS':{
                'ID':             [ 'INTEGER', 'NOT NULL UNIQUE' ],
                'SLUG':           [ 'TEXT', 'NOT NULL' ],
                'REDIRECT':       [ 'TEXT', 'NOT NULL' ],
                'START_DATETIME': [ 'TEXT', 'NOT NULL' ],
                'END_DATETIME':   [ 'TEXT', 'NOT NULL' ]

            },
            'EXTRA': 'PRIMARY KEY("id" AUTOINCREMENT)'
        }
    }

    QUERIES = {
        "LOG_VISIT":
            'INSERT into {TABLES_VISITS} ( {COLUMNS_VISITS_SLUG}, {COLUMNS_VISITS_DATETIME} ) VALUES ( "{SLUG}","{DATETIME}" );',
        "DEACTIVATE_REDIRECT":
            'UPDATE {TABLES_REDIRECTS} SET {COLUMNS_REDIRECTS_END_DATETIME}="{END_DATETIME}" WHERE {COLUMNS_REDIRECTS_SLUG}="{SLUG}" and {COLUMNS_REDIRECTS_END_DATETIME}="";',
        "ADD_REDIRECT":
            'INSERT INTO {TABLES_REDIRECTS} ( {COLUMNS_REDIRECTS_SLUG}, {COLUMNS_REDIRECTS_REDIRECT}, {COLUMNS_REDIRECTS_START_DATETIME}, {COLUMNS_REDIRECTS_END_DATETIME} ) VALUES ( "{SLUG}", "{REDIRECT}", "{START_DATETIME}", "" );',
        "GET_ACTIVE_REDIRECT":
            'SELECT {COLUMNS_REDIRECTS_REDIRECT} FROM {TABLES_REDIRECTS} WHERE {COLUMNS_REDIRECTS_SLUG}="{SLUG}" and {COLUMNS_REDIRECTS_END_DATETIME}="";',
        "CREATE_TABLE":{
            "BASE": 'CREATE TABLE "{TABLE}" ( {LINES} );',
            "LINE": '"{COLUMN}" {OTHER}',
            "JOIN": ',\n'
        }
    }

    @classmethod
    def dt_to_string( cls, dt: datetime.datetime ):
        return dt.strftime( cls.DT_FORMAT )

    @classmethod
    def log_visit_query( cls, slug, dt ):
        return cls.QUERIES['LOG_VISIT'].format( 
            TABLES_VISITS=cls.TABLES[ 'VISITS' ], 
            COLUMNS_VISITS_SLUG=cls.COLUMNS[ 'VISITS' ][ 'SLUG' ], 
            COLUMNS_VISITS_DATETIME=cls.COLUMNS[ 'VISITS' ][ 'DATETIME' ], 
            SLUG=slug, 
            DATETIME=cls.dt_to_string( dt ) )

    @classmethod
    def deactivate_redirect_query( cls, slug, dt ):

        return cls.QUERIES['DEACTIVATE_REDIRECT'].format( 
            TABLES_REDIRECTS=cls.TABLES[ 'REDIRECTS' ], 
            COLUMNS_REDIRECTS_END_DATETIME=cls.COLUMNS[ 'REDIRECTS' ][ 'END_DATETIME' ], 
            COLUMNS_REDIRECTS_SLUG=cls.COLUMNS[ 'REDIRECTS' ][ 'SLUG' ], 
            SLUG=slug, 
            END_DATETIME=cls.dt_to_string( dt ) )

    @classmethod
    def add_redirect_query( cls, slug, redirect, start_dt ):
        return cls.QUERIES['ADD_REDIRECT'].format( 
            TABLES_REDIRECTS=cls.TABLES[ 'REDIRECTS' ], 
            COLUMNS_REDIRECTS_SLUG=cls.COLUMNS[ 'REDIRECTS' ][ 'SLUG' ], 
            COLUMNS_REDIRECTS_REDIRECT=cls.COLUMNS[ 'REDIRECTS' ][ 'REDIRECT' ], 
            COLUMNS_REDIRECTS_START_DATETIME=cls.COLUMNS[ 'REDIRECTS' ][ 'START_DATETIME' ],
            COLUMNS_REDIRECTS_END_DATETIME=cls.COLUMNS[ 'REDIRECTS' ][ 'END_DATETIME' ],
            SLUG=slug, 
            REDIRECT=redirect, 
            START_DATETIME=cls.dt_to_string( start_dt ) )
    
    @classmethod
    def get_active_redirect_query( cls, slug ):
        return cls.QUERIES['GET_ACTIVE_REDIRECT'].format( 
            COLUMNS_REDIRECTS_REDIRECT=cls.COLUMNS[ 'REDIRECTS' ][ 'REDIRECT' ],
            TABLES_REDIRECTS=cls.TABLES[ 'REDIRECTS' ], 
            COLUMNS_REDIRECTS_SLUG=cls.COLUMNS[ 'REDIRECTS' ][ 'SLUG' ], 
            SLUG=slug, 
            COLUMNS_REDIRECTS_END_DATETIME=cls.COLUMNS[ 'REDIRECTS' ][ 'END_DATETIME' ] )

    @classmethod
    def create_table_query( cls, table ):

        lines = []
        for column in cls.SCHEMA[ table ]['COLUMNS']:
            lines.append( cls.QUERIES['CREATE_TABLE']['LINE'].format( COLUMN=column, OTHER=' '.join(cls.SCHEMA[ table ]['COLUMNS'][column]) ) )

        if 'EXTRA' in cls.SCHEMA[ table ]:
            lines.append( cls.SCHEMA[ table ]['EXTRA'] )

        return cls.QUERIES['CREATE_TABLE']['BASE'].format( TABLE=cls.TABLES[ table ], LINES=cls.QUERIES['CREATE_TABLE']['JOIN'].join(lines) )            

