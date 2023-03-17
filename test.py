
from setuptools import setup, find_packages
import os, subprocess



def create_mo_files():
    podir = "data/po"
    mo = []
    for po in os.listdir(podir):
        if po.endswith(".po"):
            os.makedirs("{}/{}/LC_MESSAGES".format(podir, po.split(".po")[0]), exist_ok=True)
            mo_file = "{}/{}/LC_MESSAGES/{}".format(podir, po.split(".po")[0], "pardus-gnome-shortcuts.mo")
            msgfmt_cmd = 'msgfmt {} -o {}'.format(podir + "/" + po, mo_file)
            subprocess.call(msgfmt_cmd, shell=True)
            mo.append(("/usr/share/locale/" + po.split(".po")[0] + "/LC_MESSAGES",
                       ["data/po/" + po.split(".po")[0] + "/LC_MESSAGES/pardus-gnome-shortcuts.mo"]))
    
    #return mo
    subprocess.run([
        "cp",
        "-r",
        "./data/po/tr",
        "/usr/share/locale/"
    ])
create_mo_files()