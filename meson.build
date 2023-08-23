project('pardus-gnome-shortcuts',  version: '0.0.1')

# Configuration
gnome = import('gnome')

prefix = get_option('prefix')
sysconfdir = get_option('sysconfdir')

icon_dir = join_paths(prefix,'share','icons','hicolor','scalable','apps')
source_dir = join_paths(prefix , 'share' , 'pardus' , 'pardus-gnome-shortcuts')
desktop_file_dir = join_paths(prefix,'share','applications')

desktop_file = 'tr.org.pardus.pardus-gnome-shortcuts.desktop'


# ICON FILE
install_data(['pardus-gnome-shortcuts.svg'],install_dir:icon_dir)


# DESKTOP FILE
install_data([desktop_file],install_dir : desktop_file_dir)

# USR BIN FILE
install_data(['pardus-gnome-shortcuts'], install_dir : prefix / 'bin')

# MAIN APP FOLDERS AND FILES
install_subdir('data',install_dir : source_dir)
install_subdir('src',install_dir : source_dir)
install_data(['pardus-gnome-shortcuts','pardus-gnome-shortcuts.svg'], install_dir : source_dir)


# TRANSLATIONS
subdir('data/po')
