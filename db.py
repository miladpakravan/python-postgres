import logging
import psycopg2
from deep_translator import GoogleTranslator

class DatabaseClass:

    # database connection for prevent open/close additional connections.
    connection = None
    # database table name.
    table_name = None
    # store cursor object for prevent open/close additional cursor.
    cursor     = None
    # store translated native countries for prevent retranslate them.
    translate_native_countries = {}

    def __init__( self, db_config):
        self.table_name = db_config["dbtable"]
        self.initialize( db_config )

    def __del__( self ):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logging.error( "Database connection closed." )

    # connect to database function
    def connect( self, db_config ):
        try:
            self.connection = psycopg2.connect(
                host     = db_config["host"],
                database = db_config["dbname"],
                port     = db_config["port"],
                user     = db_config["user"],
                password = db_config["passwd"]
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            logging.debug( "connection to {} established".format( db_config["dbname"] ) )
        except:
            logging.error( "Cloud not connect to Database" )

    # create database and table and ready for work.
    def initialize( self, db_config ):
        try:
            logging.debug( "checking for database and table" )
            # create database if not exists
            pre_db_config = db_config.copy()
            pre_db_config["dbname"] = "postgres"
            self.connect( pre_db_config )
            self.cursor.execute( "SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{}'".format( db_config["dbname"] ) )
            exists = self.cursor.fetchone()
            if not exists:
                self.cursor.execute( 'CREATE DATABASE {}'.format( db_config["dbname"] ) )
            # connect to database
            self.cursor.close()
            self.connection.close()
            self.connect( db_config )
            sql = '''
                CREATE TABLE IF NOT EXISTS public.%s (
                id SERIAL PRIMARY KEY,
                age INT,
                workclass VARCHAR(255),
                fnlwgt INT,
                education VARCHAR(255),
                education_num INT,
                marital_status VARCHAR(255),
                occupation VARCHAR(255),
                relationship VARCHAR(255),
                race VARCHAR(255),
                sex VARCHAR(1),
                capital_gain INT,
                capital_loss INT,
                hours_per_week INT,
                native_country VARCHAR(255),
                salary VARCHAR(255),
                translation VARCHAR(255)
            )''' % ( self.table_name )
            self.cursor.execute( sql )
            logging.debug( "Database initialized successfully" )
        except:
            logging.error( "Cloud not initialize Database!" )

    # insert csv data in database.
    def insert( self, data ):
        columns = ' ,'.join( [ str( elem ) for elem in  data["header"] ] )
        # add translation column
        columns += ' , translation'
        sql     = "INSERT INTO public.{} ({}) VALUES".format( self.table_name, columns )
        rows = data["rows"]
        index = 0
        begin = 0
        while index < len( rows ):
            sql += "({})".format( ", ".join('{0}'.format( i ) for i in tuple( self.translate_row_native_country( rows[ index ] ) ) ) )
            if 0 == index % 500 and 0 < index:
                logging.debug( "inserting row {} - {} in database".format( begin + 1, index ) )
                self.cursor.execute( sql )
                begin = index
                sql = "INSERT INTO public.{} ({}) VALUES".format( self.table_name, columns )
            elif index != len( rows ) - 1:
                sql += ","
            index = index + 1
        logging.debug( "inserting row {} - {} in database".format( begin + 1, index ) )
        self.cursor.execute( sql )

    def translate_row_native_country( self, row ):
        native_country = row[13].strip("'")
        if not self.translate_native_countries.get( native_country ):
            Translator = GoogleTranslator(
                source   = "auto",
                target   = "fa"
            )
            # we don't translate native country that contains only question marks.
            if len( native_country.replace( "?", "").strip() ):
                self.translate_native_countries[ native_country ] = Translator.translate( native_country )
            else:
                self.translate_native_countries[ native_country ] = native_country
        row.append( "'{}'".format( self.translate_native_countries[ native_country ] ) )
        return row
