import bpy
import os
import bpy.utils.previews

def Kilelit_Icons():
    global kilelit_icons
    kilelit_icons = None
    kilelit_icons = bpy.utils.previews.new()
    icon_path = os.path.dirname(__file__)
    icons_dir = os.path.join(icon_path, "../icons/images")

    #load icons
    kilelit_icons.load("kicam", os.path.join(icons_dir, "camera.png"), 'IMAGE')
    kilelit_icons.load("kiviewrender", os.path.join(icons_dir, "viewrender.png"), 'IMAGE')
    kilelit_icons.load("kianim", os.path.join(icons_dir, "animation.png"), 'IMAGE')
    kilelit_icons.load("kitransparent", os.path.join(icons_dir, "transparent.png"), 'IMAGE')
    kilelit_icons.load("kiselonly", os.path.join(icons_dir, "selectedonly.png"), 'IMAGE')
    kilelit_icons.load("kivprender", os.path.join(icons_dir, "viewportrender.png"), 'IMAGE')
    kilelit_icons.load("kishadowcatch", os.path.join(icons_dir, "shadowcatcher.png"), 'IMAGE')
    kilelit_icons.load("kiclearselonly", os.path.join(icons_dir, "clearselectedonly.png"), 'IMAGE')
    kilelit_icons.load("kiperformance", os.path.join(icons_dir, "performance.png"), 'IMAGE')
    kilelit_icons.load("kisamples", os.path.join(icons_dir, "samples.png"), 'IMAGE')
    kilelit_icons.load("kidata", os.path.join(icons_dir, "data.png"), 'IMAGE')
    kilelit_icons.load("kilight", os.path.join(icons_dir, "light.png"), 'IMAGE')
    kilelit_icons.load("kicryptomatte", os.path.join(icons_dir, "cryptomatte.png"), 'IMAGE')
    kilelit_icons.load("kimtloverride", os.path.join(icons_dir, "materialoverride.png"), 'IMAGE')
    kilelit_icons.load("kiclayon", os.path.join(icons_dir, "clayon.png"), 'IMAGE')
    kilelit_icons.load("kiclayoff", os.path.join(icons_dir, "clayoff.png"), 'IMAGE')
    kilelit_icons.load("kiadvanced", os.path.join(icons_dir, "advanced.png"), 'IMAGE')
    kilelit_icons.load("kilights", os.path.join(icons_dir, "lights.png"), 'IMAGE')
    kilelit_icons.load("kilightpaths", os.path.join(icons_dir, "lightpaths.png"), 'IMAGE')
    kilelit_icons.load("kigi", os.path.join(icons_dir, "gi.png"), 'IMAGE')
    kilelit_icons.load("kilightlinks", os.path.join(icons_dir, "lightlinks.png"), 'IMAGE')
    kilelit_icons.load("kilightgroups", os.path.join(icons_dir, "lightgroups.png"), 'IMAGE')
    kilelit_icons.load("kishadowlinks", os.path.join(icons_dir, "shadowlinks.png"), 'IMAGE')
    kilelit_icons.load("kilocked", os.path.join(icons_dir, "locked.png"), 'IMAGE')
    kilelit_icons.load("kiunlocked", os.path.join(icons_dir, "unlocked.png"), 'IMAGE')
    kilelit_icons.load("kitrashcan", os.path.join(icons_dir, "trashcan.png"), 'IMAGE')
    kilelit_icons.load("kisavefile", os.path.join(icons_dir, "savefile.png"), 'IMAGE')
    kilelit_icons.load("kifolder", os.path.join(icons_dir, "folder.png"), 'IMAGE')
    kilelit_icons.load("kikblogo", os.path.join(icons_dir, "kblogo.png"), 'IMAGE')
    kilelit_icons.load("kikbspacelogo", os.path.join(icons_dir, "kbspacelogo.png"), 'IMAGE')
    kilelit_icons.load("kiblendrmarkt", os.path.join(icons_dir, "blendermarket.png"), 'IMAGE')
    kilelit_icons.load("kiyoutube", os.path.join(icons_dir, "youtube.png"), 'IMAGE')
    kilelit_icons.load("kidocs", os.path.join(icons_dir, "docs.png"), 'IMAGE')
    kilelit_icons.load("kinetworkrender", os.path.join(icons_dir, "networkrendering.png"), 'IMAGE')
    kilelit_icons.load("kikb3dservices", os.path.join(icons_dir, "kb3dservices.png"), 'IMAGE')

def register():
    pass

def unregister():
    global kilelit_icons
    try:
        bpy.utils.previews.remove(kilelit_icons)
    except:
        pass
