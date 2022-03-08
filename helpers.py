import json
import csv
import logging

def get_config():
    with open( "config.json" ) as config_file:
        conf = json.load( config_file )
    return conf

def read_csv( file_path ):
    logging.debug( "read data from csv" )
    file = open( file_path )
    csvreader = csv.reader(file)
    data = {
        "header" : [],
        "rows"   : []
    }
    data["header"] = normalize_csv_header( next( csvreader ) )
    index = 1
    for row in csvreader:
        if len( row ) == 15:
            data["rows"].append( normalize_csv_row( row ) )
        index = index + 1
    file.close()
    return data

def normalize_csv_header( row ):
    index = 0
    while index < len( row ):
        row[ index ] = str( row[ index ] ).replace( "-", "_" ) 
        row[ index ] = str( row[ index ] ).strip()
        index = index + 1
    return row

def normalize_csv_row( row ):
    index = 0
    while index < len( row ):
        # remove whitespaces
        row[ index ] = str( row[ index ] ).strip()
        # check if value is numerice, change type of value to integer.
        if str( row[ index ] ).isnumeric():
            row[ index ] = int( row[ index ] )
        else:
            # add single quote to strings value for easy serve values in insert query.
            row[ index ] = "'{}'".format( row[ index ] )
        index = index + 1
    # check sex type and set suitable character for save space in database.
    if str( row[9] ).lower() == "'male'":
        row[9] = "'m'"
    else:
        row[9] = "'f'"
    # Remove notation from native country for prevent translation problems.
    row[13] = row[13].replace( "-", " " ) 
    return row
