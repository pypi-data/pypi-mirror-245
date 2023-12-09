from web_traffic_monitor.schemas.base import Schema as BaseSchema

class Schema( BaseSchema ):

    DT_FORMAT = '%Y-%m-%d TESTTEST %H:%M:%S.%f%z'

    # When redefining one of the class attributes, redefine the entire dictionary in the child class
    TABLES = {
        'VISITS': 'visits_test',
        'REDIRECTS': 'redirects_test'
    }
