import gi
import os, threading
import subprocess
import time
import json

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, Gdk, Gio, GObject, GdkPixbuf, GLib,Pango

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
        self.main_window = Gtk.ApplicationWindow()
        self.main_window.set_size_request(300,300)
        self.main_window.set_name("window")

        self.main_window.set_halign(self.align_fill)
        self.main_window.set_valign(self.align_fill)

        self.main_window.show()
        self.shortcuts = None
        with open("../data/shortcuts.json") as file:
            self.shortcuts = json.loads(file.read())


        self.main_box = Gtk.Box.new(self.vertical,13)
        self.main_box.set_halign(self.align_start)
        self.main_box.set_valign(self.align_start)
        self.main_box.set_hexpand(True)
        self.main_box.set_vexpand(True)
        self.main_box.set_margin_top(20)
        self.main_box.set_margin_bottom(20)
        self.main_box.set_margin_start(20)
        self.main_box.set_margin_end(20)
        
        for shortcut in self.shortcuts:
            shortcut_box = Gtk.Box.new(self.vertical,13)
            shortcut_box.set_css_classes(['shortcutbox'])
            shortcut_box.set_hexpand(True)
            shortcut_box.set_vexpand(True)
            label = Gtk.Label()
            label.set_markup('<b>%s</b>'%(shortcut['label']))
            label.set_halign(self.align_start)
            shortcut_box.append(label)
            
            for data in shortcut['datas']:
                shortcut_info = data["name"]
                shortcut_box.set_halign(self.align_start)
                shortcut_keys = " + ".join(data["keys"])
                info = Gtk.Label(label="%s : %s"%(shortcut_info,shortcut_keys))
                info.set_halign(self.align_start)
                shortcut_box.append(info)
                print(data,shortcut_keys)
            self.main_box.append(shortcut_box)


        self.main_window.set_child(self.main_box)

