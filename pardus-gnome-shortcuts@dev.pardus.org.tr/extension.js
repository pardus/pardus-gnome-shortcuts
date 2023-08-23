const { main , panelMenu } = imports.ui
const { St, GObject, Gio, GLib, Clutter } = imports.gi
const Me = imports.misc.extensionUtils.getCurrentExtension();

let pardusGnomeShortcutsIndicator;
const PardusGnomeShortcutsIndicator = GObject.registerClass(
    class PardusGnomeShortcutsIndicator extends panelMenu.Button {
        _init() {
            super._init(0);
            let icon = new St.Icon({
                gicon: Gio.icon_new_for_string(Me.dir.get_path() + '/icon.svg'),
                style_class: 'system-status-icon',
            });
            this.add_child(icon);
            this.connect('event', (actor, event) => {
                if (event.type() === Clutter.EventType.BUTTON_PRESS)
                    GLib.spawn_command_line_async('pardus-gnome-shortcuts')
            });
        }
    });
function enable() {
    pardusGnomeShortcutsIndicator = new PardusGnomeShortcutsIndicator();
    main.panel.addToStatusArea('pardusGnomeShortcutsIndicator', pardusGnomeShortcutsIndicator, 1);
}
function disable() {
    pardusGnomeShortcutsIndicator.destroy();
}
