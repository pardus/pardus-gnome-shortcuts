#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os, subprocess




changelog = "debian/changelog"
if os.path.exists(changelog):
    head = open(changelog).readline()
    try:
        version = head.split("(")[1].split(")")[0]
    except:
        print("debian/changelog format is wrong for get version")
        version = ""
    f = open("src/__version__", "w")
    f.write(version)
    f.close()


data_files = [
    ("/usr/share/glib-2.0/data/schemas/", [
    		"data/schema/tr.org.pardus.pardus-gnome-shortcut.gschema.xml"
    	]
    ),
    ("/usr/share/applications/", [
    		"tr.org.pardus.pardus-gnome-shortcut.desktop"
    	]
    ),
    ("/usr/share/pardus/pardus-gnome-shortcut/", [
    		"pardus-gnome-shortcut.svg"
    	]
    ),
    ("/usr/share/pardus/pardus-gnome-shortcut/src", [
    		"src/Main.py",
    		"src/MainWindow.py",
		]
    ),
    ("/usr/share/pardus/pardus-gnome-shortcut/assets", [
        
            	"data/assets/bg.avif",
            	"data/assets/bg.jpg",
            	"data/assets/logo.svg",      
    	]
    ),
    ("/usr/share/pardus/pardus-gnome-shortcut/data/", [
    		"data/style.css"
    	]
    ),
    ("/usr/bin/", [
    		"pardus-gnome-shortcut"
    	]
    ),
    ("/usr/share/icons/hicolor/scalable/apps/", [
			"pardus-gnome-shortcut.svg"
		]
	)
]

setup(
    name="pardus-gnome-shortcut",
    version="0.0.1",
    packages=find_packages(),
    scripts=["pardus-gnome-shortcut"],
    install_requires=["PyGObject"],
    data_files=data_files,
    author="Pardus Altyapı",
    author_email="dev@pardus.org.tr",
    description="Pardus Gnome Shortcut, show or hide Pardus / Gnome Shortcuts",
    license="GPLv3",
    keywords="",
    url="https://www.pardus.org.tr",
)
