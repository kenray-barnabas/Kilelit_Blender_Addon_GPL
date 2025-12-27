bl_info = {
    "name": "Kilelit",
    "author": "Kenray Barnabas",
    "version": (1, 5, 6),
    "blender": (5, 0, 0),
    "location": "View3D > Sideshelf > Kilelit",
    "description": """These are custom rendering tools to help speed up your rendering workflow in blender!""",
    "warning": "",
    "wiki_url":"",
    "category": "KB Tools"
    }

#This script was developed for the purpose of automation.
#The special tools include rendering selected only for stills/animations.
#You also have rendering shadow catcher automated included under selected only rendering.
#rendering shadow catcher also works with animation if animation is toggled.
#blender's existing features were implemented in this script for quick acess all in one.
import bpy
import os
import webbrowser
import time

#import modules
from Kilelit import icons, ops, ui, utils, thumb, sfx
#import previews thumbnails
from Kilelit.thumb import renderhistory
#import icon loader
from Kilelit.icons import icons_load
#import operators
from Kilelit.ops import operators
#import ui panels
from Kilelit.ui import ui_panels
#import functions
from Kilelit.utils import kilelit_functions, preview_selector, openwebpages

kilelit_modulepkgs = [icons, ops, ui, utils, sfx, thumb]
kilelit_assetpkgs = [icons_load, operators, ui_panels, kilelit_functions, preview_selector, openwebpages]

kilelit_packages = [kilelit_modulepkgs, kilelit_assetpkgs]

def import_delayer():
    importlib.reload(renderhistory)

    bpy.app.timers.unregister(import_delayer)


def register_delayer():
    renderhistory.register()

    bpy.app.timers.unregister(register_delayer)

if "bpy" in locals():
    import importlib

    #import packages
    for list in kilelit_packages:
        for modules in list:
            importlib.reload(modules)

    bpy.app.timers.register(import_delayer, first_interval=0.0001)

def register():
    for list in reversed(kilelit_packages):
        for modules in reversed(list):
            modules.register()

    bpy.app.timers.register(register_delayer, first_interval=0.0001)


def unregister():
    for list in kilelit_packages:
        for modules in list:
            modules.unregister()

    renderhistory.unregister()

if __name__ == "__main__":
    register()
