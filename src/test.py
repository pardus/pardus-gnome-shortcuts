import gi
import subprocess
from gi.repository import GLib,Gio

a = [
    "gsettings",
    "set", 
    "org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/pardus0/",
    "binding",
    "'<Primary><Alt>f'"
]
b = [
    "gsettings", 
    "set",
    "org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/pardus0/",
    "command",
    "'firefox'"
]
c = [
    "gsettings",
    "set",
    "org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/pardus0/",
    "name",
    "'Firefox Launcher'"
]
d = [
    "gsettings", 
    "set",
    "org.gnome.settings-daemon.plugins.media-keys",
    "custom-keybindings",
    "['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/pardus0/']"
]


subprocess.run(a)
subprocess.run(b)
subprocess.run(c)
subprocess.run(d)