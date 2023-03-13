import subprocess
import gi
gi.require_version("Gio","2.0")
from gi.repository import Gio

schema = "org.pardus.pardus-gnome-shortcuts"
key = "first-start"

class utils:

    
    def is_schema_exist(schema):
        schema_source = Gio.SettingsSchemaSource.get_default()
        result = schema_source.lookup(schema,True)
        if result == None:
            return False
        else:
            return True
    
    def is_first_start(self):
        settings = Gio.Settings(schema)
        value = settings.get_value(key)
        return value
    
    def set_first_start(self):
        settings = Gio.Settings(schema)
        settings.set_boolean(key,True)
        settings.apply()
    