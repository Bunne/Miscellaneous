#!/usr/bin/env python3
'''KFInstaller
Killing Floor Map Whitelist Installer
All content copyright their respective owners/authors.
Installer not affiliated with KFM Whitelist, Sykosis.
Installer, KFM Whitelist, Sykosis are in no way related to or affiliated with
Tripwire Interactive, the Killing Floor game or map authors/creators.
'''

__version__ = "2.0"
__date__ = "07-13-2014"
__author__ = "Cameron Pelkey"

from config import Config
import os
import sys
import getpass
import urllib.request
from html.parser import HTMLParser
import zipfile
import shutil

CONFIG = Config("config")

class KF_Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.map = False
        self.att = []
        self.online = []

    def handle_starttag(self, tag, attrs):
        if tag == 'h2':
            self.map = True
        elif tag == 'a' and attrs and self.map and (len(attrs) != 2):
            if (len(attrs) == 1):
                self.att.append(('link',attrs[0][1]))
            else:
                self.att.extend(attrs[1:])

    def handle_endtag(self, tag):
        if tag == 'h2' and self.map:
            self.online.append(KF_Map(self.att))
            self.att = []
            self.map = False

    def handle_data(self, data):
        if self.map:
            data = data.strip()
            if data not in ['{', '}', '']:
                if len(self.att) == 1:
                    self.att.append(('name', data))
                elif len(self.att) == 2:
                    self.att.append(('author', data[3:]))

class KF_Map():
    def __init__(self, information):
        self.info = dict(information)

    def print_info(self):
        print("Name: %s" % self.info['name'])
        print("Author: %s" % self.info['author'])
        print("Link: %s" % self.info['link'])
        print("Info: %s" % self.info['title'])
        print()

    def install(self):
        if self.info['name'] in CONFIG.get_config("MAPS"):
            print("%s Already Installed" % self.info['name'])
            return 0

        print("Installing %s" % self.info['name'])
        if not os.path.exists(CONFIG.get_config("TEMP")):
            os.makedirs(CONFIG.get_config("TEMP"))
        os.chdir(CONFIG.get_config("TEMP"))

        with urllib.request.urlopen(self.info['href']) as response,\
                open(os.path.join(CONFIG.get_config("TEMP"), self.info['name']), 'wb') as outfile:
                shutil.copyfileobj(response, outfile)
        with zipfile.ZipFile(self.info['name'], 'r')  as kfzip:
            for item in kfzip.namelist():
                if item not in ['__MACOSX', '.DS_Store']:  # Ignore OS files
                    if(os.path.basename(item)): # Ignore directories
                        name = os.path.basename(item)   # Get individual filename only
                        ext = os.path.splitext(name)[1] # Get extension
                        source = kfzip.open(item)

                        # MOVE FILES BASED ON EXTENSION
                        # Maps - rom
                        if ext == '.rom':
                            target = open(os.path.join(CONFIG.get_config("GD_Maps"), name),'wb')
                            shutil.copyfileobj(source,target)
                        # Music - ogg
                        if ext == '.ogg':
                            target = open(os.path.join(CONFIG.get_config("GD_Music"), name),'wb')
                            shutil.copyfileobj(source,target)
                        # Sound - uax
                        if ext == '.uax':
                            target = open(os.path.join(CONFIG.get_config("GD_Sounds"), name),'wb')
                            shutil.copyfileobj(source,target)
                        # Textures - utx
                        if ext == '.utx':
                            target = open(os.path.join(CONFIG.get_config("GD_Textures"), name),'wb')
                            shutil.copyfileobj(source,target)
                        # Meshes - usx
                        if ext == '.usx':
                            target = open(os.path.join(CONFIG.get_config("GD_Meshes"), name),'wb')
                            shutil.copyfileobj(source,target)
                        # Animation - ukx
                        if ext == '.ukx':
                            target = open(os.path.join(CONFIG.get_config("GD_Animations"), name),'wb')
                            shutil.copyfileobj(source,target)
                        # System - u , ucl, upl, int, dll, fxc
                        if ext in ['.u', '.ucl', '.upl', '.int', '.dll', '.DLL', '.fxc']:
                            target = open(os.path.join(CONFIG.get_config("GD_System"), name),'wb')
                            shutil.copyfileobj(source,target)
                        source.close()
                        target.close()
        os.remove(self.info['name'])

        os.chdir(CONFIG.get_config("OD"))
        os.rmdir(CONFIG.get_config("TEMP"))
        return 1



def init():
    CONFIG.set_config("OD", os.path.abspath('.'))
    CONFIG.set_config("USER", getpass.getuser())
    system = os.name
    if system not in ['nt','posix']:
        return 0
    elif system == 'nt':
        CONFIG.set_config("ROOT",CONFIG.get_config("Path_Windows"))
    elif system == 'posix':
        CONFIG.set_config("ROOT",CONFIG.get_config("Path_OSX")%(CONFIG.get_config("USER")))
    if not os.path.exists(CONFIG.get_config("ROOT")):
        return 0
    CONFIG.set_config("GD_Maps", os.path.join(CONFIG.get_config("ROOT"),'Maps'))
    CONFIG.set_config("GD_Music", os.path.join(CONFIG.get_config("ROOT"),'Music'))
    CONFIG.set_config("GD_Sounds", os.path.join(CONFIG.get_config("ROOT"),'Sounds'))
    CONFIG.set_config("GD_Textures", os.path.join(CONFIG.get_config("ROOT"),'Textures'))
    CONFIG.set_config("GD_System", os.path.join(CONFIG.get_config("ROOT"),'System'))
    CONFIG.set_config("GD_Meshes", os.path.join(CONFIG.get_config("ROOT"),'StaticMeshes'))
    CONFIG.set_config("GD_Animations", os.path.join(CONFIG.get_config("ROOT"),'Animations'))
    CONFIG.set_config("TEMP", os.path.join(CONFIG.get_config("ROOT"),'TEMP'))

    determine_maps()
    return 1

def determine_maps():
    maps = []
    for dir, dirnames, filenames in os.walk(CONFIG.get_config("GD_Maps")):
        for filename in filenames:
            if filename not in ['.DS_Store', 'Entry.rom', 'KFintro.rom']:
                maps.append(os.path.splitext(filename)[0])
    CONFIG.set_config("MAPS", maps)
    return 1

def get_online_list():
    parser = KF_Parser()
    response = urllib.request.urlopen('http://sykosis.co.uk/kfmwhitelist/list')
    html = response.read()
    html = html.decode("utf8")
    parser.feed(html)
    return parser.online



if __name__ == '__main__':
    if not init():
        exit()
    if len(sys.argv) <= 2:
        print("NO")
    elif sys.argv[1] == 'list':
        if sys.argv[2] == 'mine':
            for map in CONFIG.get_config("MAPS"):
                print(map)
        elif sys.argv[2] == 'online':
            online_list = get_online_list()
            for map in online_list:
                print(map.info['name'])
        elif sys.argv[2] == 'diff':
            online_list = get_online_list()
            for map in online_list:
                if map.info['name'] not in CONFIG.get_config("MAPS"):
                    print(map.info['name'])
    elif sys.argv[1] == 'info':
        online_list = get_online_list()
        for map in online_list:
            if sys.argv[2] in map.info['name'][3:]:
                map.print_info()
    elif sys.argv[1] == 'install':
        online_list = get_online_list()
        for map in online_list:
            if (sys.argv[2] == map.info['name']) or \
                (sys.argv[2] == map.info['name'][3:]):
                map.install()


