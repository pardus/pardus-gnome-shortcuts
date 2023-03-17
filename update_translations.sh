#!/bin/bash

langs=("tr")

if ! command -v xgettext &> /dev/null
then
	echo "xgettext could not be found."
	echo "you can install the package with 'apt install gettext' command on debian."
	exit
fi


echo "updating pot file"
xgettext -o po/pardus-gnome-shortcuts.pot --files-from=data/po/files

for lang in ${langs[@]}; do
	if [[ -f data/po/$lang.po ]]; then
		echo "updating $lang.po"
		msgmerge -o data/po/$lang.po data/po/$lang.po data/po/pardus-gnome-shortcuts.pot
	else
		echo "creating $lang.po"
		cp data/po/pardus-gnome-shortcuts.pot data/po/$lang.po
	fi
done