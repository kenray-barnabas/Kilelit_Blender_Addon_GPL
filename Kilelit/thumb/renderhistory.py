import bpy
import os
import re
import time
import importlib
import bpy.utils.previews
from bpy.props import *
from bpy.app.handlers import persistent
from Kilelit import utils

img_ext = (".bmp", ".iris", ".png", ".jpg", ".jpeg", ".jpeg 2000", ".tga", ".targa", ".targa raw", ".cin", ".dpx", ".exr", ".openexr multilayer", ".openexr", ".hdr", ".radiance hdr", ".tiff", ".webp"
)


def extract_number_from_tuple(item):
    if item[0].startswith("_rendersomething"):
        return -2  # This ensures "_rendersomething" comes first

    if item[0].endswith("kilelit_preview"):
        return -1  # This ensures "kilelit_preview" comes second

    #if not a special case, extract the numerical part for sorting
    match = re.search(r'(\d+)$', item[0])
    return int(match.group(1)) if match else float('inf')  # return a high number if no digits are found

def init_images(self, context):
    global img_ext

    if "renderhistory_thumbs" in render_collection:
        renderpreviews = render_collection["renderhistory_thumbs"]
        image_location = renderpreviews.img_location

        #existing render previews clear
        renderpreviews.clear()

        #render thumbnails
        enum_renderthumbs = []

        for i, image in enumerate(os.listdir(image_location)):
            #image extension
            if image.lower().endswith((img_ext)):
                image_path = os.path.join(image_location, image)
                #apply a unique identifier
                unique_identifier = f"{i}_{image[:-4]}"

                thumb_image = renderpreviews.load(unique_identifier, image_path, 'IMAGE')
                enum_renderthumbs.append((image[:-4], image[:-4], "", thumb_image.icon_id, i))

        #sort the images with numerical values
        enum_renderthumbs.sort(key=extract_number_from_tuple)
        return enum_renderthumbs

render_collection = {}

#register and unregister
def register():
    global scene
    scene = bpy.context.scene

    global render_previews
    render_previews = None
    render_previews = bpy.utils.previews.new()

    if scene.render_history_path != "":
        render_previews.img_location = bpy.path.abspath(os.path.join(scene.render_history_path))
    else:
        render_previews.img_location = os.path.join(os.path.dirname(__file__), "../thumb/images")

    render_collection["renderhistory_thumbs"] = render_previews

def unregister():
    for rc in render_collection.values():
        bpy.utils.previews.remove(rc)
