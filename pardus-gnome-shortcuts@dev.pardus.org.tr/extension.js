// Example#8
const { St, GObject, Gio, GLib } = imports.gi
const { main, panelMenu, popupMenu } = imports.ui
const Me = imports.misc.extensionUtils.getCurrentExtension();

let myPopup;
function init() {
}

function enable() {
    extensionMenu = new PardusGnomeShortcut();
    main.panel.addToStatusArea('PardusGnomeShortcuts', extensionMenu, 1);
}

function disable() {
    myPopup.destroy();
}
const PardusGnomeShortcut = GObject.registerClass(
    class PardusGnomeShortcut extends panelMenu.Button {

        _init() {
            super._init(0);
            let icon = new St.Icon({
                gicon: Gio.icon_new_for_string(Me.dir.get_path() + '/icon.svg'),
                style_class: 'system-status-icon',
            });

            this.add_child(icon);


            this.menu.addMenuItem(new popupMenu.PopupSeparatorMenuItem());

            // image item
            let shortcutMenuLauncher = new popupMenu.PopupImageMenuItem(
                'Open Shortcuts',
                'input-keyboard-symbolic',
            );
            shortcutMenuLauncher.connect("activate", () => {
                GLib.spawn_command_line_async('firefox')
            })
            this.menu.addMenuItem(shortcutMenuLauncher);
        }
    });

