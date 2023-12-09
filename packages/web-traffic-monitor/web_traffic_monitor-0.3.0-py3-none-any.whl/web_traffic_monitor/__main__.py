import web_traffic_monitor

import logging
#web_traffic_monitor.LOGGER.setLevel( logging.CRITICAL )
web_traffic_monitor.LOGGER.setLevel( logging.DEBUG )

c = web_traffic_monitor.Client()

c.log_visit( 'ASDF' )
c.add_redirect( 'ASDF', 'redirect1' )
c.get_active_redirect( 'ASDF' )
c.deactive_redirect( 'ASDF' )
c.get_active_redirect( 'ASDF' )
c.add_redirect( 'ASDF', 'redirect2' )
c.get_active_redirect( 'ASDF' )

print ()
for i in c.db.query( 'Select * from {} LIMIT 10'.format( c.schema.TABLES['VISITS'] ) ):
    print (i)
print ()
for i in c.db.query( 'Select * from {} LIMIT 10'.format( c.schema.TABLES['REDIRECTS'] ) ):
    print (i)