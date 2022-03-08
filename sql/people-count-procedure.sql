-- Regenerate number of people function --
DROP FUNCTION IF EXISTS number_of_people( text ) CASCADE;
CREATE OR REPLACE FUNCTION number_of_people( native_country text ) RETURNS JSON AS '
    import logging
    
    import json
    from deep_translator import GoogleTranslator
    translated_native_country = GoogleTranslator(source="auto", target="en").translate( native_country.replace( "-", " " )  )
    
    FORMAT = "%(asctime)s %(message)s"
    logging.basicConfig(filename="/tmp/db.log", level=logging.DEBUG, format=FORMAT)
    logging.debug( "native language: \"{}\" , translation: \"{}\"".format( native_country, translated_native_country ) )
    
    select_plan = plpy.prepare( "SELECT id FROM dataset WHERE native_country = $1 AND sex = $2", [ "text", "char" ] )
    rv = plpy.execute( select_plan, [ translated_native_country, "m" ] )
    number_of_males = rv.nrows()
    rv = plpy.execute( select_plan, [ translated_native_country, "f" ] )
    number_of_females = rv.nrows()
    return json.dumps( { "Males" : number_of_males, "Females" : number_of_females } )
' LANGUAGE plpython3u;
