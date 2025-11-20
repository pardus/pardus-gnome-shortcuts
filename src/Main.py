#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

class Application(Adw.Application):

    def __init__(self, **kwargs):
        super().__init__(**kwargs, application_id="tr.org.pardus.pardus-gnome-shortcuts")
        self.connect('activate', self.on_activate)
        self.main_window = None

    def on_activate(self, app):
        if not self.main_window:
            from MainWindow import MainWindow
            self.main_window = MainWindow(application=app)
            self.main_window.present()


app = Application()
app.run(None)
