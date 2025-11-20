import gi
import os
import json
import subprocess

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Gdk, Gio, Adw, GLib

try:
    import apt
except ImportError:
    apt = None

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


class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Paths
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.data_dir = os.path.join(self.script_dir, "../data")

        # Load Data
        self.load_data()

        # Initial Setup
        self.set_title(_("Pardus Gnome Shortcuts"))
        self.set_default_size(1000, 675)

        # Default Mode
        self.current_mode = "grid" 
        
        self.update_ui()

    def load_data(self):
        try:
            with open(os.path.join(self.data_dir, "data.json")) as file:
                self.datas = json.loads(file.read())
            with open(os.path.join(self.data_dir, "custom_shortcuts.json")) as file2:
                self.custom_shortcuts = json.loads(file2.read())
            with open(os.path.join(self.data_dir, "shortcuts.json")) as file3:
                self.shortcuts = json.loads(file3.read())
        except Exception as e:
            print(f"Error loading data: {e}")
            self.datas = {}

    def update_ui(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        header = Adw.HeaderBar()
        
        # Mode Switch Button
        icon_name = "view-list-symbolic" if self.current_mode == "grid" else "view-grid-symbolic"
        tooltip = _("Switch to List View") if self.current_mode == "grid" else _("Switch to Grid View")
        
        toggle_btn = Gtk.Button(icon_name=icon_name)
        toggle_btn.set_tooltip_text(tooltip)
        toggle_btn.connect("clicked", self.toggle_mode)
        
        # About Button
        about_btn = Gtk.Button(icon_name="help-about-symbolic")
        about_btn.set_tooltip_text(_("About"))
        about_btn.connect("clicked", self.show_about_dialog)
        
        # Pack buttons to the start (left)
        header.pack_start(toggle_btn)
        header.pack_start(about_btn)
        
        box.append(header)
        
        # Content Area
        if self.current_mode == "grid":
            content = self.create_grid_view()
        else:
            content = self.create_list_view()
            
        if self.current_mode == "grid":
            scrolled = Gtk.ScrolledWindow()
            scrolled.set_vexpand(True)
            scrolled.set_child(content)
            box.append(scrolled)
        else:
            content.set_vexpand(True)
            box.append(content)

        self.set_content(box)

    def toggle_mode(self, widget):
        if self.current_mode == "grid":
            self.current_mode = "list"
        else:
            self.current_mode = "grid"
        self.update_ui()

    def get_app_version(self):
        if apt:
            try:
                cache = apt.Cache()
                pkg = cache.get("pardus-gnome-shortcuts")
                if pkg and pkg.installed:
                    return pkg.installed.version
            except:
                pass
        

        return "0.0.1" # Final Fallback

    def show_about_dialog(self, widget):
        about = Adw.AboutWindow()
        about.set_application_name(_("Pardus Gnome Shortcuts"))
        about.set_application_icon("pardus-gnome-shortcuts")
        about.set_developer_name("Osman Coşkun")
        about.set_version(self.get_app_version())
        about.set_copyright("© 2025 TÜBİTAK BİLGEM")
        about.set_website("https://www.pardus.org.tr/")
        about.set_license_type(Gtk.License.GPL_3_0)
        about.present()

    def create_grid_view(self):
        # Manual 3-column Layout: System | Launchers+Screenshot | Workspace
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        main_box.set_hexpand(True)
        
        # Column 1
        col1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        col1.set_hexpand(True)
        col1.set_valign(Gtk.Align.START)

        # Column 2
        col2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        col2.set_hexpand(True)
        col2.set_valign(Gtk.Align.START)

        # Column 3
        col3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        col3.set_hexpand(True)
        col3.set_valign(Gtk.Align.START)
        
        main_box.append(col1)
        main_box.append(col2)
        main_box.append(col3)
        
        # Categories distribution
        # Col 1: System
        # Col 2: Launchers, Screenshot Tool
        # Col 3: Workspace
        
        col1_cats = ["System"]
        col2_cats = ["Launchers", "Screenshot Tool"]
        col3_cats = ["Workspace"]
        
        # Define icons for categories
        category_icons = {
            "System": "preferences-system-symbolic",
            "Launchers": "system-run-symbolic",
            "Screenshot Tool": "camera-photo-symbolic",
            "Workspace": "view-paged-symbolic"
        }
        
        cards = {} # Store created cards by category name
        
        for category_name, category_data in self.datas.items():
            # Create Card
            card_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            card_box.add_css_class("card")
            card_box.set_vexpand(True) # Expand vertically to fill column height
            
            # Inner content padding
            inner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
            inner_box.set_margin_top(15)
            inner_box.set_margin_bottom(15)
            inner_box.set_margin_start(15)
            inner_box.set_margin_end(15)
            card_box.append(inner_box)

            # Title with Icon
            title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            
            # Add icon if available
            icon_name = category_icons.get(category_name, "applications-system-symbolic")
            icon = Gtk.Image.new_from_icon_name(icon_name)
            icon.set_pixel_size(20) # Set icon size
            title_box.append(icon)
            
            title_label = Gtk.Label(label=_(category_name))
            title_label.add_css_class("title-4") 
            title_label.set_halign(Gtk.Align.START)
            title_box.append(title_label)
            
            inner_box.append(title_box)
            
            # Add separator below title
            title_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            title_sep.set_margin_top(15) # Increased space above separator
            title_sep.set_margin_bottom(5) # Space below title
            inner_box.append(title_sep)
            
            schema = category_data.get("schema")
            datas = category_data.get("datas", [])

            # Collect valid data items first to know count
            valid_datas = []
            for data in datas:
                # Check if it has values without full processing? 
                # We need to process to know if values exist.
                # Or we can just iterate and add separator unless it's last visible.
                # Simpler: Iterate, if values exist, append. 
                # To handle separator, we can check index or add separator after each, then remove last?
                # Better: Store widgets in a list, then append with separators.
                valid_datas.append(data)

            # We'll process and add directly, managing separator logic
            visible_count = 0
            temp_widgets = []
            
            for data in datas:
                row_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
                
                key = data["key"]
                name = data["name"]
                custom = data.get("custom", False)
                item_schema = data.get("schema", schema)

                values = self.fun_get_keybinding(item_schema, key, custom, raw=True)

                # Only display if there are values
                if values:
                    name_label = Gtk.Label(label=_(name))
                    # name_label.add_css_class("heading") # Removed bold style
                    name_label.set_halign(Gtk.Align.START)
                    row_box.append(name_label)

                    # Use Vertical orientation to stack multiple shortcuts
                    shortcuts_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
                    shortcuts_box.set_halign(Gtk.Align.START) # Align to start
                    for val in values:
                        shortcut_label = Gtk.ShortcutLabel(accelerator=val)
                        shortcuts_box.append(shortcut_label)
                    row_box.append(shortcuts_box)
                    
                    temp_widgets.append(row_box)

            # Append widgets with separators
            for i, widget in enumerate(temp_widgets):
                inner_box.append(widget)
                # Add separator if not last item
                if i < len(temp_widgets) - 1:
                    sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                    sep.set_margin_top(5)
                    sep.set_margin_bottom(5)
                    inner_box.append(sep)
            
            cards[category_name] = card_box

        # Append cards to columns in specific order
        for cat in col1_cats:
            if cat in cards:
                col1.append(cards[cat])
                
        for cat in col2_cats:
            if cat in cards:
                col2.append(cards[cat])
                
        for cat in col3_cats:
            if cat in cards:
                col3.append(cards[cat])
                
        # Handle remaining categories
        known_cats = col1_cats + col2_cats + col3_cats
        for cat, card in cards.items():
            if cat not in known_cats:
                col3.append(card) # Append to last column by default
                    
        return main_box

    def create_list_view(self):
        pref_page = Adw.PreferencesPage()
        
        # Icons map for List View too
        category_icons = {
            "System": "preferences-system-symbolic",
            "Launchers": "system-run-symbolic",
            "Screenshot Tool": "camera-photo-symbolic",
            "Workspace": "view-paged-symbolic"
        }
        
        for category_name, category_data in self.datas.items():
            group = Adw.PreferencesGroup()
            group.set_title(_(category_name))
            
            # Add header suffix/icon to PreferencesGroup is not directly supported via simple API,
            # but we can set the title. 
            # AdwPreferencesGroup doesn't support icons in header easily without custom header.
            # So we will stick to just text title for list view as per Adwaita guidelines for now,
            # or we could create a custom header widget but `set_header_suffix` is for widgets.
            # Let's keep List view standard.
            
            pref_page.add(group)

            schema = category_data.get("schema")
            datas = category_data.get("datas", [])

            for data in datas:
                key = data["key"]
                name = data["name"]
                custom = data.get("custom", False)
                item_schema = data.get("schema", schema)

                values = self.fun_get_keybinding(item_schema, key, custom, raw=True)

                # Create separate ActionRows for each shortcut alternative if multiple exist
                if values and len(values) > 1:
                    for val in values:
                        row = Adw.ActionRow()
                        row.set_title(_(name)) # Same title for each
                        
                        shortcut_label = Gtk.ShortcutLabel(accelerator=val)
                        shortcut_label.set_halign(Gtk.Align.END)
                        shortcut_label.set_valign(Gtk.Align.CENTER)
                        row.add_suffix(shortcut_label)
                        
                        group.add(row)
                elif values:
                    # Single value
                    row = Adw.ActionRow()
                    row.set_title(_(name))
                    
                    val = values[0]
                    shortcut_label = Gtk.ShortcutLabel(accelerator=val)
                    shortcut_label.set_halign(Gtk.Align.END)
                    shortcut_label.set_valign(Gtk.Align.CENTER)
                    row.add_suffix(shortcut_label)
                    
                    group.add(row)
        
        return pref_page

    def fun_get_keybinding(self, schema, key, is_custom, raw=False):
        binding = []
        if is_custom:
            res = self.fun_get_custom_keybinding(key)
            if res and res.startswith("'") and res.endswith("'"):
                 res = res[1:-1]
            if res:
                binding = [res]
        else:
            settings = Gio.Settings.new(schema)
            binding = settings.get_strv(key)

        # Filter empty
        binding = [b for b in binding if b]
        
        if raw:
            return binding

        result = []
        for item in binding:
            temp_parts = item.replace("><", "|").replace("<", "").replace(">", "|").split("|")
            temp_parts = [p for p in temp_parts if p]
            result.append(temp_parts)
            
        return result

    def fun_get_custom_keybinding(self, key):
        dconf_path = "dconf read /org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/{key}/binding"
        cmd = dconf_path.format(key=key)
        try:
            return subprocess.getoutput(cmd).strip()
        except:
            return ""
