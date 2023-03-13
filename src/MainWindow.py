import gi
import os, threading
import subprocess
import time
import json
import xmltodict

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, Gdk, Gio, GObject, GdkPixbuf, GLib,Pango
from utils import utils
from Keybindings import Keybindings
utils = utils()
Keybindings = Keybindings()
try:
    import locale
    from locale import gettext as _
    APPNAME = "gnome-control-center-2.0"
    TRANSLATION_PATH="/usr/share/locale"
    locale.bindtextdomain(APPNAME,TRANSLATION_PATH)
    locale.textdomain(APPNAME)

except:
    def _(msg):
        return msg

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # IMPORT CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(
            os.path.dirname(os.path.abspath(__file__)) + "/../data/style.css"
        )
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

        with open("../data/shortcuts.json") as file:
            self.shortcuts = json.loads(file.read())
        with open("../data/custom_shortcuts.json") as file2:
            self.custom_shortcuts = json.loads(file2.read())


        self.is_first_start = utils.is_first_start()
        if self.is_first_start:
            self.first_run()




        self.init_ui()

    def init_ui(self):
        # GTK SETTINGS
        self.ellipsize = Pango.EllipsizeMode(2)
        self.horizontal = Gtk.Orientation.HORIZONTAL
        self.vertical = Gtk.Orientation.VERTICAL
        self.align_start = Gtk.Align(1)
        self.align_fill = Gtk.Align(0)
        self.align_center = Gtk.Align(3)

        # MAIN WINDOW OF APPLICATION
        self.main_window = Gtk.ApplicationWindow(title="Pardus Gnome Shortcuts")
        self.main_window.set_size_request(300,300)
        self.main_window.set_name("window")

        self.main_window.set_halign(self.align_fill)
        self.main_window.set_valign(self.align_fill)

        self.main_window.show()

        self.main_box = Gtk.Box.new(self.vertical,13)
        self.main_box.set_halign(self.align_start)
        self.main_box.set_valign(self.align_start)
        self.main_box.set_css_classes(["mainbox"])
        self.main_box.set_hexpand(True)
        self.main_box.set_vexpand(True)
        self.main_box.set_margin_top(20)
        self.main_box.set_margin_bottom(20)
        self.main_box.set_margin_start(20)
        self.main_box.set_margin_end(20)
        
        for shortcut in self.shortcuts:

            xml_shortcut_path = self.shortcuts[shortcut]["path"]
            xml_shortcut_file = open(xml_shortcut_path)
            xml_shortcut_data = xml_shortcut_file.read()

            shortcut_data = xmltodict.parse(xml_shortcut_data)
            label_text = _(shortcut_data["KeyListEntries"]["@name"])



            shortcut_box = Gtk.Box.new(self.vertical,13)
            shortcut_box.set_css_classes(['shortcutbox'])
            shortcut_box.set_hexpand(True)
            shortcut_box.set_vexpand(True)
            
            label = Gtk.Label()
            
            label.set_markup('<b>%s</b>'%label_text)
            label.set_halign(self.align_start)
            shortcut_box.append(label)
            self.main_box.append(shortcut_box)

        self.main_window.set_child(self.main_box)

    def first_run(self):
        for shortcut in self.custom_shortcuts:
            id,name,binding, command  = shortcut.values()
            Keybindings.set_keybinding(id, name, binding, command)
            