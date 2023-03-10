import subprocess
import xmltodict
import json
file_path = "/usr/share/gnome-control-center/keybindings/50-gnome-shell-screenshots.xml"

gsettings_path = "org.gnome.shell.keybindings"
with open(file_path) as f:
    xml_content = xmltodict.parse(f.read())


datas = {
    'screenshot_datas':[],
}

json_file = open('../data/shortcuts.json')
json_datas = json.load(json_file)
screenshot_xml_datas = xml_content["KeyListEntries"]["KeyListEntry"]

for data in screenshot_xml_datas:
    if data['@name'] in json_datas:
        datas['screenshot_datas'].append(data)
for i in datas['screenshot_datas']:
    cmd = "gsettings get %s %s"%(gsettings_path,i["@name"]) 
    print(subprocess.getoutput(cmd))
