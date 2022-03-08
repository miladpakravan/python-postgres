import timeit
import csv
import helpers
import logging
from db import DatabaseClass

# Logging config
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=FORMAT)

# ------------------ Main ------------------#
start = timeit.default_timer()
logging.debug( "project started." )
# read config
conf = helpers.get_config()
# read csv file
csv_data = helpers.read_csv( "dataset.csv" )
# connect to database
db_connection = DatabaseClass( conf["db"] )
# insert csv data in database
db_connection.insert( csv_data )
stop = timeit.default_timer()
del db_connection
logging.debug( "project done!" )
logging.debug( "runtime: {}s".format( int( stop - start ) ) )
