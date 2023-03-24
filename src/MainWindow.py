import gi
import os, threading
import subprocess
import time
import json

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
    
    #APPNAME = "gnome-control-center-2.0"
    APPNAME = "pardus-gnome-shortcuts"
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
        

        with open("../data/data.json") as file:
            self.datas = json.loads(file.read())
        with open("../data/custom_shortcuts.json") as file2:
            self.custom_shortcuts = json.loads(file2.read())
        with open("../data/shortcuts.json") as file3:
            self.shortcuts = json.loads(file3.read())


        self.is_first_start = utils.is_first_start()
        if self.is_first_start:
            self.fun_first_run()

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
        self.ui_main_window = Gtk.ApplicationWindow(
            title="Pardus Gnome Shortcuts"
        )
        self.ui_main_window.set_decorated(False)
        self.ui_main_window.set_name("window")
        

        self.ui_main_window.set_halign(self.align_fill)
        self.ui_main_window.set_valign(self.align_fill)
        

        #self.ui_main_box = Gtk.Box.new(self.horizontal,13)
        self.ui_main_box = self.fun_create_box(horizontal=True,css=['mainbox'],h_expand=True,v_expand=True,
            margin=20,h_align=self.align_start,v_align=self.align_start
        )      
        self.ui_main_window.set_child(self.ui_main_box)

        self.fun_list_datas()
        
        

    def fun_first_run(self):
        for shortcut in self.custom_shortcuts:
            id,name,binding, command  = shortcut.values()
            Keybindings.set_custom_keybinding(id, name, binding, command)

    def set_keybinding(self):
        for shortcut in self.shortcuts:
            schema,key,binding = shortcut.values()
            Keybindings.set_keybinding(schema,key,binding)

    def fun_list_datas(self):
        for shortcut in self.datas:
            ui_shortcut_box = self.fun_create_box(horizontal=False, spacing=23,css=['box'],v_expand=True,h_expand=True)

            ui_title_label_text ='<b>%s</b>'%(_(shortcut))
            ui_title_label = self.fun_create_label(markup=ui_title_label_text,css=['title'],h_align=self.align_start)
            ui_shortcut_box.append(ui_title_label) 
            
            schema = self.datas[shortcut]['schema']
            datas = self.datas[shortcut]['datas']

            if 'custom' in self.datas[shortcut].keys():
                custom = self.datas[shortcut]['custom']
            else:
                custom = False            

            for data in datas:
                    ui_keybinding_box = self.fun_create_box(horizontal=False)
                    key = data['key']
                    name = data['name']
                    if 'schema' in data.keys():
                        values = Keybindings.get_keybinding(data['schema'],key,custom)
                    else:
                        values = Keybindings.get_keybinding(schema,key,custom)

                    key_text = "<b>%s</b> "%_(name)
                    ui_shortcut_name_label = self.fun_create_label(markup=key_text)
                    ui_keybinding_box.append(ui_shortcut_name_label)

                    if len(values) > 0:
                        for value in values:
                            keybinding_text = self.fun_create_label(text=" + ".join(value))
                            ui_keybinding_box.append(keybinding_text)

                    ui_shortcut_box.append(ui_keybinding_box)
            self.ui_main_box.append(ui_shortcut_box)

        
    def fun_create_box(self, horizontal=True, name=None, spacing=13, css=[], h_expand=False, 
        v_expand=False, margin=0, h_align=Gtk.Align(0), v_align=Gtk.Align(0)):

        if horizontal:
            box = Gtk.Box.new(self.horizontal,spacing)
        else:
            box = Gtk.Box.new(self.vertical,spacing)

        if len(css) > 0:
            box.set_css_classes(css)    

        if name!=None:
            box.set_name(name)

        box.set_hexpand(h_expand)
        box.set_vexpand(v_expand)

        box.set_margin_bottom(margin)
        box.set_margin_top(margin)
        box.set_margin_start(margin)
        box.set_margin_end(margin)

        box.set_halign(h_align)
        box.set_valign(v_align)
        return box

    def fun_create_label(self, text="", markup="", css=[], h_align=Gtk.Align(1)):
        
        label = Gtk.Label()

        if len(text) > 0:
            label.set_label(text)
        else:
            label.set_markup(markup)

        if len(css) > 0:
            label.set_css_classes(css)

        label.set_halign(h_align)

        return label
        
