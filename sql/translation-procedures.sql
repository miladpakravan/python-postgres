-- Regenerate translation native country function --
DROP FUNCTION IF EXISTS translate_native_country() CASCADE;
CREATE OR REPLACE FUNCTION translate_native_country() RETURNS trigger AS '
    from deep_translator import GoogleTranslator
    row_id = int( TD["new"]["id"] )
    native_country = str( TD["new"]["native_country"] )
    translation = TD["new"]["translation"]
    if not translation:
        translated_native_country = GoogleTranslator(source="auto", target="fa").translate( native_country )
        update_plan = plpy.prepare( "UPDATE dataset SET translation = $2 WHERE id = $1", ["int", "text"] )
        rv = plpy.execute( update_plan, [ row_id, translated_native_country ] )
' LANGUAGE plpython3u;

-- Create Trigger calls after INSERT on dataset and translate native country --
CREATE TRIGGER translate_native_country AFTER INSERT on public.dataset 
FOR EACH ROW EXECUTE PROCEDURE translate_native_country();

