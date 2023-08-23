import gi
import os, threading
import subprocess
import time
import json

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")

from gi.repository import Gtk, Gdk, Gio, Pango
from libpardus import Ptk


try:
    import locale
    from locale import gettext as _

    APPNAME = "pardus-gnome-shortcuts"
    TRANSLATION_PATH = "/usr/share/locale"

    locale.bindtextdomain(APPNAME, TRANSLATION_PATH)
    locale.textdomain(APPNAME)

except:

    def _(msg):
        return msg


class MainWindow(Gtk.ApplicationWindow):
    # +----------------------------------------------------+
    # |                 Pardus Gnome Shortcuts             |
    # +----------------------------------------------------+
    # | [X]                                                |
    # | +---------------------------------------------+    |
    # | | Shortcut Title                              |    |
    # | | +-----------------------------------------+ |    |
    # | | | Shortcut Name                           | |    |
    # | | | - Keybinding 1                          | |    |
    # | | | - Keybinding 2                          | |    |
    # | | | - Keybinding 3                          | |    |
    # | | +-----------------------------------------+ |    |
    # | +----------------------------------------------    +
    # | +---------------------------------------------+    |
    # | | Shortcut Title                              |    |
    # | | +-----------------------------------------+ |    |
    # | | | Shortcut Name                           | |    |
    # | | | - Keybinding 1                          | |    |
    # | | | - Keybinding 2                          | |    |
    # | | | - Keybinding 3                          | |    |
    # | | +-----------------------------------------+ |    |
    # | +----------------------------------------------    +

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        Ptk.utils.load_css("../data/style.css")

        with open("../data/data.json") as file:
            self.datas = json.loads(file.read())
        with open("../data/custom_shortcuts.json") as file2:
            self.custom_shortcuts = json.loads(file2.read())
        with open("../data/shortcuts.json") as file3:
            self.shortcuts = json.loads(file3.read())

        self.init_ui()

    def init_ui(self):
        # MAIN WINDOW OF APPLICATION

        self.ui_main_window = Ptk.ApplicationWindow(title=_("Pardus Gnome Shortcuts"))
        self.ui_main_window.set_name("window")
        self.ui_main_window.set_decorated(False)

        self.close_btn = Ptk.Button(label="X", css=["circular"])
        self.close_btn_box = Ptk.Box(children=[self.close_btn])
        self.app_box = Ptk.Box(
            css=["mainbox", "card"],
            hexpand=True,
            vexpand=True,
            spacing=23,
            margin_bot=20,
            margin_end=20,
            margin_start=20,
            h_align="start",
            v_align="start",
            children=[],
        )
        self.ui_main_box = Ptk.Box(
            orientation="vertical",
            children=[self.close_btn_box, self.app_box],
        )
        self.ui_main_window.set_child(self.ui_main_box)

        for shortcut in self.datas:
            ui_title_label_text = "<b>%s</b>" % (_(shortcut))
            ui_title_label = Ptk.Label(
                markup=ui_title_label_text, css=["title"], h_align="start"
            )
            ui_shortcut_box = Ptk.Box(
                orientation="vertical",
                spacing=23,
                css=["box"],
                vexpand=True,
                hexpand=True,
                children=[ui_title_label],
            )
            schema = self.datas[shortcut]["schema"]
            datas = self.datas[shortcut]["datas"]

            if "custom" in self.datas[shortcut].keys():
                custom = self.datas[shortcut]["custom"]
            else:
                custom = False

            for data in datas:
                ui_keybinding_box = Ptk.Box(orientation="vertical")
                key = data["key"]
                name = data["name"]
                if "schema" in data.keys():
                    values = self.fun_get_keybinding(data["schema"], key, custom)
                else:
                    values = self.fun_get_keybinding(schema, key, custom)

                ui_shortcut_name_label = Ptk.Label(markup=f"<b>{_(name)}</b>")
                ui_keybinding_box.append(ui_shortcut_name_label)

                if len(values) > 0:
                    for value in values:
                        ui_keybinding_text_label = Ptk.Label(label=" + ".join(value))
                        ui_keybinding_box.append(ui_keybinding_text_label)

                ui_shortcut_box.append(ui_keybinding_box)
            self.app_box.append(ui_shortcut_box)

    def fun_get_keybinding(self, schema, key, is_custom):
        if is_custom:
            binding = [self.fun_get_custom_keybinding(key)[1:-1]]
        else:
            settings = Gio.Settings.new(schema)
            binding = settings.get_strv(key)

        while "" in binding:
            binding.remove("")
        if len(binding) > 0:
            for b_index, item in enumerate(binding):
                item = item.split(">")
                for index, string in enumerate(item):
                    if "<" in string:
                        item[index] = string[1:]
                binding[b_index] = item
        return binding

    def fun_get_custom_keybinding(self, key):
        dconf_path = "dconf read /org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/{key}/binding"
        cmd = dconf_path.format(key=key)
        return subprocess.getoutput(cmd)
