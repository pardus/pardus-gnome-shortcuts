import subprocess
from gi.repository import GLib,Gio
class Keybindings:
    def get_keybindings(self):
        cmd = ["gsettings","list-recursively"]
        return subprocess.getoutput(cmd)
    def set_keybinding(self,id,name,binding,command):
        infos = [
            {
                "key":"name",
                "value":name
            },
            {
                "key":"binding",
                "value":binding
            },
            {
                "key":"command",
                "value":command
            },
            
        ]
        main_schema = "org.gnome.settings-daemon.plugins.media-keys"
        custom_schema_key = "custom-keybindings"
        
        schema = "org.gnome.settings-daemon.plugins.media-keys.custom-keybinding"

        path = "/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/"
        
        for info in infos:
            cmd = ["gsettings", "set",schema+":"+path+id+"/", info["key"],info["value"]]

            subprocess.run(cmd)
            
        
            

        settings = Gio.Settings.new(main_schema)   
        variant = settings.get_value(custom_schema_key)

        keybinding_list = list(variant.unpack())
        new_key = """{path}{id}""".format(path=path,id=id)
        
        if new_key not in keybinding_list:
            keybinding_list.append(new_key)
        
        new_variant = GLib.Variant.new_strv(keybinding_list)
        settings.set_value(custom_schema_key,new_variant)
        