import bpy
import os
import re
import time
from bpy.types import EnumProperty
from Kilelit import thumb
from Kilelit.thumb import renderhistory


img_ext = {
    'BMP': '.bmp', 'IRIS': '.iris', 'PNG': '.png', 'JPEG': '.jpg',
    'JPEG2000': '.jpeg 2000', 'TARGA': '.tga', 'TARGA_RAW': '.targa raw',
    'CINEON': '.cin', 'DPX': '.dpx', 'OPEN_EXR': '.exr',
    'OPEN_EXR_MULTILAYER': '.openexr multilayer', 'HDR': '.hdr',
    'TIFF': '.tiff', 'WEBP': '.webp'
    }

def gv(): #global variables
    gv.scene = bpy.context.scene
    #path to get the images
    gv.folder_path = bpy.path.abspath(os.path.join(gv.scene.render_history_path))


#update the enumproperty
def get_images(self, context):
    gv() #global variables

    #define the path where the images are saved
    image_path = gv.folder_path
    #print("path found at: ", image_path)
    #print(f"Image '{img.name}' has been removed from Blender.")

    global img_ext
    #image type to load
    current_format = bpy.context.scene.render.image_settings.file_format
    file_extension = img_ext.get(current_format, '.png')

    #iterate through each file in the directory
    if gv.scene.generate_previews == True:
        for file_name in os.listdir(image_path):
            #check if the file is an image
            if os.path.splitext(file_name)[1].lower() in file_extension:
                #construct the full file path
                file_path = os.path.join(image_path, file_name)

                #check if the image is already loaded
                if file_name in bpy.data.images:
                    #print(f"Image already loaded: {file_name}")
                    pass
                else:
                    #load the image and handle potential errors
                    try:
                        image = bpy.data.images.load(file_path, check_existing=True)
                        #print(f"Loaded image: {image.name}")

                    except RuntimeError as e:
                        print(f"Failed to load image {file_name}: {e}")

    #print("images loaded from: ", image_path)
    image_preview(self, context)

def image_preview(self, context):
    gv() #get global variables

    #NOW SET THE IMAGE SELECTED AS THE ACTIVE IMAGE
    image_name = gv.scene.render_history_previews
    global img_ext

    ext_pattern = '|'.join(re.escape(ext) for ext in img_ext.values())
    pattern = re.compile(r'^kilelit_preview_(\d+)(?:{})$'.format(ext_pattern))

    for ext in img_ext.values():
        file_path = os.path.join(gv.folder_path, image_name + ext)
        if os.path.exists(file_path):
            image_name += ext
            break
    #print("Trying to set image: ", image_name)

    #check if the image is already loaded
    if image_name not in bpy.data.images:
        #print(f"Image '{image_name}' is not loaded in Blender.")
        pass

    img = bpy.data.images[image_name]

    #try to find an existing image editor window
    image_editor = None
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                image_editor = area.spaces.active
                break

        if image_editor:
            break

    #if an image editor window is found, set the image
    if image_editor:
        image_editor.image = img
        #print(f"Image '{img.name}' set in the existing Image Editor")

    else:
        #open render window
        bpy.ops.render.view_show('INVOKE_DEFAULT')

        #set the image in the new image editor
        for space in area.spaces:
            if space.type == 'IMAGE_EDITOR':
                space.image = img
                #print(f"Image '{img.name}' set in the new Image Editor")
                break

def refresh_image_enum(self, context):
    #refresh the items for the enum property
    scene = bpy.context.scene
    altpath = scene.render_history_path

    bpy.types.Scene.render_history_previews = bpy.props.EnumProperty(
        items = renderhistory.init_images(True, True),
        name = "Kilelit History",
        description = "Kilelit previews",
        update=get_images
    )

    #Trigger update in Ui by reassigning the enum property
    bpy.context.scene['render_history_previews'] = scene.render_history_previews

def get_first_rendered_image():
    global img_ext
    scene = bpy.context.scene
    #list all files in directory
    folder_path = bpy.path.abspath(os.path.join(scene.render_history_path))

    current_format = bpy.context.scene.render.image_settings.file_format
    file_extension = img_ext.get(current_format, '.png')

    first_image = False
    kilelit_firstimage = f"kilelit_preview{file_extension}"

    #check if first image exists
    if os.path.isfile(os.path.join(folder_path, kilelit_firstimage)):
        kilelit_firstimage = True

    if first_image:
        return kilelit_firstimage
    else:
        #print("No first rendered image found.")
        return None

def get_latest_rendered_image():
    global img_ext
    scene = bpy.context.scene
    #list all files in directory
    folder_path = bpy.path.abspath(os.path.join(scene.render_history_path))

    current_format = bpy.context.scene.render.image_settings.file_format
    file_extension = img_ext.get(current_format, '.png')

    ext_pattern = '|'.join(re.escape(ext) for ext in img_ext.values())
    pattern = re.compile(r'^kilelit_preview_(\d+)(?:{})$'.format(ext_pattern))

    highest_value = 0
    found_new_image = False

    # Ensure the directory exists
    if not os.path.exists(folder_path):
        #print("Directory does not exist:", folder_path)
        return None

    try:
        for filename in os.listdir(folder_path):
            match = pattern.match(filename)
            if match:
                value = int(match.group(1))
                if value > highest_value:
                    highest_value = value
                    found_new_image = True

    except:
        return None


    if found_new_image:
        return f"kilelit_preview_{highest_value}"
    else:
        #print("No new rendered image found.")
        return None

def set_enum_to_latest_image():
    first_image = get_first_rendered_image()
    latest_image = get_latest_rendered_image()
    try:
        if latest_image:
            bpy.context.scene.render_history_previews = latest_image
        else:
            if first_image:
                bpy.context.scene.render_history_previews = first_image
            else:
                #print("No rendered images found.")
                return None

    except RuntimeError as e:
        print(f"Failed to get the latest image: {e}")


def register():
    pass

def unregister():
    pass
