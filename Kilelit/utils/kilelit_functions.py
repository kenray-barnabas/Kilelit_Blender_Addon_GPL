import bpy
import os
import re
import time
import subprocess
import aud
import shutil

from bpy.app.handlers import persistent
from Kilelit.thumb import renderhistory
from Kilelit.utils import preview_selector

#global variable to stor the previous selection
previous_selection = []
opengl_done = False

img_ext = {
    'BMP': '.bmp', 'IRIS': '.iris', 'PNG': '.png', 'JPEG': '.jpg',
    'JPEG2000': '.jpeg 2000', 'TARGA': '.tga', 'TARGA_RAW': '.targa raw',
    'CINEON': '.cin', 'DPX': '.dpx', 'OPEN_EXR': '.exr',
    'OPEN_EXR_MULTILAYER': '.openexr multilayer', 'HDR': '.hdr',
    'TIFF': '.tiff', 'WEBP': '.webp'
}

def load_post_enum():
    historypathset(True, True)

@persistent
def check_filepath(self, context):
    #print("RESETTING HISTORY PREVIEWER")
    bpy.app.timers.register(load_post_enum, first_interval=0.0001)

def check_filepath_handler():
    if check_filepath not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(check_filepath)


def on_selection_change():
    gv()
    global previous_selection

    #get the current selection
    current_selection = [gv.obj.name for obj in bpy.context.selected_objects]

    #compare the current selection to the previous selection
    if current_selection != previous_selection:
        try:
            ClearSelSets(True)
        except RuntimeError as e:
            print(f"Failed to clear settings: {e}")

    #update the previous selection with the current selection
    previous_selection = current_selection

#RENDER SCENE
def gv():
    try:
        gv.scene = bpy.context.scene #load global variables
        gv.obj = bpy.context.object

        gv.fileformat = bpy.context.scene.render.image_settings.file_format

        script_path = os.path.dirname(__file__) #path of the current script
        parent_directory = os.path.dirname(script_path)
        gv.folder_path = os.path.join(parent_directory, "thumb/images/_rendersomething.png")
    except:
        pass


def refresh_get_image(self, context):
    renderhistory.unregister()
    renderhistory.register()

    historypathset(self, context)

    bpy.app.handlers.load_post.remove(historypathset)

def get_images_handler():
    if historypathset not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(historypathset)

def historypathset(self, context):
    scene = bpy.context.scene
    # current path
    #previous_path = ""

    #if scene.render_history_path != previous_path:
    previous_path = scene.render_history_path

    remove_prev = "kilelit_preview"
    #remove images in blender with basename "preview"
    images_to_remove = [img for img in bpy.data.images if img.name.startswith(remove_prev)]
    for img in images_to_remove:
        #check if the basename matches
        bpy.data.images.remove(img)
        #print("Removed previous images from blender images")

    #Copy the _rendersomething file to the history path
    #This is the default image for the image previewer
    script_path = os.path.dirname(__file__) #path of the current script
    parent_directory = os.path.dirname(script_path)
    folder_path = os.path.join(parent_directory, "thumb/images/_rendersomething.png")

    altpath = bpy.path.abspath(os.path.join(scene.render_history_path, "_rendersomething.png"))

    #Check if default image already exists in directory
    if "_rendersomething.png" in previous_path:
        pass
        #print("Default image already setup directory.")
    else:
        shutil.copy(folder_path, altpath)

    #remove previews
    renderhistory.unregister()
    #append new previews
    renderhistory.register()

    refresh_enum(self, context)


def renderselonly(self, context):
    gv() #load global variables
    if gv.scene.renderselected == True:
        gv.scene.screenCaps = False
    else:
        try:
            ClearSelSets(True)
            #set Render Shadow Catcher disabled
            gv.scene.rendershadowcatcher = False

        except:
            pass

def MyRender(self, myrender):
    gv() #load global variables
    if gv.scene.generate_previews == True and gv.scene.render_history_path == "":
            self.report({'ERROR'}, "Directory is empty in Ki History path.")
    else:
        render_init(self)


def render_init(self):
    rEngine = bpy.context.scene.render.engine
    #check if render will be transparent or not
    if gv.scene.fTransparent == True:
        bpy.context.scene.render.film_transparent = True
    elif gv.scene.fTransparent == False:
        bpy.context.scene.render.film_transparent = False

    #check whether selected only render is toggled or not.
    if gv.scene.renderselected == False:
        #render still frame
        Kilelit(True)

    #--------------------------------------------------------------#
    #RENDER SELECTED ONLY
    elif gv.scene.renderselected == True:
        #check if the selection has changed
        on_selection_change()

        sel = len(bpy.context.selected_objects)
        if sel > 0:
            if rEngine == 'CYCLES' or rEngine == 'BLENDER_EEVEE':
                #render only selected by custom method options.
                if gv.scene.renderHoldouts == True or gv.scene.renderCamVisible == True:
                    if gv.scene.rendershadowcatcher == True:
                        makeshadowcatch(True)
                    else:
                        selectedMethod(True)

                elif gv.scene.renderHoldouts == False and gv.scene.renderCamVisible == False:
                    self.report({'ERROR'}, "Select either holdout or invisible under methods.")
        elif sel == 0:
            self.report({'ERROR'}, "Selected Only is enabled. Select object(s) to render.")

def renderviewport(self, context):
    gv() #load global variables
    if gv.scene.screenCaps == True:
        gv.scene.renderselected = False


def isshadowcatcher(self, context):
    gv()
    sel = len(bpy.context.selected_objects)
    selRange = range(sel)

    if gv.scene.rendershadowcatcher == False:
        for x in selRange:
            ob = bpy.context.selected_objects[x]
            bpy.context.view_layer.objects.active = ob
            ob.select_set(state = True)

            bpy.context.object.is_shadow_catcher = False
    else:
         for x in selRange:
            ob = bpy.context.selected_objects[x]
            bpy.context.view_layer.objects.active = ob
            ob.select_set(state = True)

            bpy.context.object.is_shadow_catcher = True       


#render selected object(s) as shadow catcher
def makeshadowcatch(self):
    gv() #load global variables
    sel = len(bpy.context.selected_objects)
    selRange = range(sel)

    #check if the selection has changed
    on_selection_change()

    cscene = bpy.context.scene.cycles
    #use fase gi allumination
    #produces better shadows
    if cscene.use_fast_gi == False:
        cscene.use_fast_gi = True
    elif cscene.use_fast_gi == True:
        pass

    if sel > 0:
        for x in selRange:
            ob = bpy.context.selected_objects[x]
            bpy.context.view_layer.objects.active = ob
            ob.select_set(state = True)

            bpy.context.object.is_shadow_catcher = True

        selectedMethod(True)

    else:
        self.report({'ERROR'}, "Select object(s) to render.")


#Hide non mesh objects in view port
def hide_nonmesh(space_data, properties):
    for prop in properties:
        if hasattr(space_data, prop):
            setattr(space_data, prop, False)

#Show non mesh objects in view port
def show_nonmesh(space_data, properties):
    for prop in properties:
        if hasattr(space_data, prop):
            setattr(space_data, prop, True)


#RENDER SELECTED ONLY METHOD "RENDERHOLD"
def selectedMethod(self):
    gv() #load global variables
    sel = len(bpy.context.selected_objects)

    #storing the previous selected objects
    previous_selection = bpy.context.selected_objects

    #before applying custom render settings to objects
    #we need to hide the unwanted objects
    #so we don't apply the custom settings to these
    #when inverting our selection.
    #Below is a list variable containg all the stuff we don't want to select.

    spaceData = bpy.context.space_data
    nonMesh = [
        "show_object_viewport_armature",
        "show_object_viewport_lattice",
        "show_object_viewport_empty",
        "show_object_viewport_light",
        "show_object_viewport_light_probe",
        "show_object_viewport_camera",
        "show_object_viewport_speaker"
    ]

    ####--------------------------------------------##########
    #hide elements we don't want to select
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    hide_nonmesh(space, nonMesh)

    if sel > 0:
        if gv.obj.is_shadow_catcher == True:
            print("Object is a shadow catcher.")

        #invert selection selecting all mesh types
        bpy.ops.object.select_all(action = 'INVERT')

        objSel = bpy.context.selected_objects
        for x in range(len(objSel)):
            ob = bpy.context.selected_objects[x]
            bpy.context.view_layer.objects.active = ob
            ob.select_set(state = True)

            #check which method is selected
            if gv.scene.rendershadowcatcher == False:
                bpy.context.object.is_shadow_catcher = False

            if gv.scene.renderHoldouts == True:
                bpy.context.object.is_holdout = True
                bpy.context.object.visible_camera = True

            elif gv.scene.renderCamVisible == True:
                bpy.context.object.is_holdout = False
                bpy.context.object.visible_camera = False

            #check for particle systems in "unselected" set if any
            for obj in bpy.data.objects:
                for mod in gv.obj.modifiers:
                    if mod.type == 'PARTICLE_SYSTEM':
                        mod.show_viewport = False
                        mod.show_render = False


        bpy.ops.object.select_all(action = 'DESELECT')

        #Show elements we don't want to select
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        show_nonmesh(space, nonMesh)

        #restore the previous selected objects and set one of them active
        for gv.obj in previous_selection:
            gv.obj.select_set(True)

        #set the last object in the previously selected list as the active object
        if previous_selection:
            bpy.context.view_layer.objects.active = previous_selection[-1]

        #show elements we don't want to select
        for prop in nonMesh:
            setattr(spaceData, prop, True)


        Kilelit(self)

    #check if we have selected an object in scene.
    elif sel == 0:
        self.report({'ERROR'}, "Select object(s) to render.")


def findImageEditor():
    # Check if there is an active Image Editor window
    for area in bpy.context.screen.areas:
        if area.type == 'IMAGE_EDITOR':
            # There is an active Image Editor, set the active image
            target_image_name = "Render Result"  # Replace with the image name you want to set as active
            for space in area.spaces:
                if space.type == 'IMAGE_EDITOR':
                    for image in bpy.data.images:
                        if image.name == target_image_name:
                            space.image = image
                            #print(f"Set '{target_image_name}' as the active image in the Image Editor.")
                            break
                    break
            break

def popup_error(msg, title="Error"):
    def draw(self, context):
        for line in str(msg).splitlines():
            self.layout.label(text=line)
    bpy.context.window_manager.popup_menu(draw, title=title, icon="ERROR")

#---------START RENDER---------#
#--------------Initiate_Render----------------#
def Kilelit(self):
    gv() #load global variables
    findImageEditor()
    global opengl_done
    #clear render post in animation
    bpy.app.handlers.render_post.clear()
    bpy.app.handlers.render_complete.clear()

    #check if sound is on after render complete
    if gv.scene.renderpostnotify == True:
        rendercomplete_sound_handler()


    #first check if animation is true or false
    if gv.scene.renderAnim == False:
        #render still
        if gv.scene.render.image_settings.media_type != "IMAGE":            
            popup_error("Cannot write a single file with an animation format selected.")
            return
               
        else:
            if gv.scene.generate_previews == False:
                if gv.scene.screenCaps == False:
                    bpy.ops.render.render('INVOKE_DEFAULT', animation = False, write_still = False)

                elif gv.scene.screenCaps == True:
                    bpy.ops.render.opengl('INVOKE_DEFAULT', animation = False, write_still = False)
                    opengl_complete_alert(self, True)

            else:
                #lock the interface in render to avoid errors while the script is updating
                gv.scene.renderLockUI = True
    
                if gv.scene.screenCaps == False:
                    save_post_handler()
                    #run handler to save image to render preview directory
                    bpy.ops.render.render('INVOKE_DEFAULT', animation = False, write_still=False)

                elif gv.scene.screenCaps == True:
                    save_image(self, True) 


    #render animation
    else:
        if gv.scene.generate_previews == True or gv.scene.generate_previews == False:
            #even if generate_previews is enabled or disabled we dont want to use it in animation.
            is_playing = bpy.context.screen.is_animation_playing
            if gv.scene.screenCaps == False:
                bpy.ops.render.render('INVOKE_DEFAULT', animation = True, write_still = True)

            elif gv.scene.screenCaps == True:
                gv.scene.frame_set(gv.scene.frame_end)
                global current_frame
                current_frame = gv.scene.frame_current
                #set the frame to the last frame and keep the last frame value
                opengl_anim_framechange_handler()
                bpy.ops.render.opengl('INVOKE_DEFAULT', animation = True, write_still = True)

#post render handlers
def save_post_handler():
    if save_image not in bpy.app.handlers.render_post:
        bpy.app.handlers.render_post.append(save_image)

def rendercomplete_sound_handler():
    if render_complete_alert not in bpy.app.handlers.render_complete:
        bpy.app.handlers.render_complete.append(render_complete_alert)


def opengl_anim_complete_alert(self, context):
    scene = bpy.context.scene
    global current_frame
    if scene.frame_current == current_frame:
        opengl_complete_alert(self, context)
        bpy.app.handlers.frame_change_pre.clear()


def opengl_anim_framechange_handler():
    if opengl_anim_complete_alert not in bpy.app.handlers.frame_change_pre:
        bpy.app.handlers.frame_change_pre.append(opengl_anim_complete_alert)


def save_image(self, context):
    scene = bpy.context.scene
    global img_ext

    #get the render result
    rendered_image = bpy.data.images['Render Result']

    folder_path = bpy.path.abspath(os.path.join(scene.render_history_path))

    base_file_name = 'kilelit_preview'
    current_format = bpy.context.scene.render.image_settings.file_format
    file_extension = img_ext.get(current_format, '.png')

    #iterate to find an unused file name
    counter = 1
    file_name = f"{base_file_name}{file_extension}"
    file_name_counter = f"{base_file_name}_{counter}{file_extension}"
    full_path = os.path.join(folder_path, file_name)

    #note to self, don't change the "while"
    while os.path.exists(full_path):
        file_name = f"{base_file_name}_{counter}{file_extension}" #iterated file name
        full_path = os.path.join(folder_path, file_name)
        counter += 1

    #save image
    if scene.screenCaps == True:
        global current_filepath
        current_filepath = bpy.context.scene.render.filepath

        if os.path.isdir(current_filepath):
            global directory
            directory = current_filepath
            global directory_filename
            directory_filename = ""
        else:
            directory = os.path.dirname(current_filepath)
            directory_filename = os.path.basename(current_filepath)

        bpy.context.scene.render.filepath = full_path
        findImageEditor()

        bpy.ops.render.opengl('INVOKE_DEFAULT', write_still=True)
        bpy.app.timers.register(filepath_default, first_interval=1)


    else:
        rendered_image.save_render(filepath=full_path)

    #print(file_name + " saved to location: ", full_path)

    #load the image to blender
    if os.path.exists(full_path):
        try:
            #load the image and handle potential errors
            loaded_image = bpy.data.images.load(full_path, check_existing=True)
        except RuntimeError as e:
            pass
    else:
        pass

    if scene.screenCaps == True:
        bpy.app.timers.register(update_enum, first_interval = 1) #delay if opengl render

    else:
        refresh_enum(True, True)


def clear_render_history(clearrenderhistory):
    #path to remove images from
    scene = bpy.context.scene
    folder_path = bpy.path.abspath(os.path.join(scene.render_history_path))
    remove_prev = "kilelit_preview"
    #check if the directory exists
    if os.path.exists(folder_path):

        files_to_delete = []

        #list all files in the directory
        for file in os.listdir(folder_path):
            #construct the full file path
            file_path = os.path.join(folder_path, file)
            #extract the basename without extension
            basename, _ = os.path.splitext(file)
            #check if the basename matches
            if remove_prev in basename:
                files_to_delete.append(file_path)

        for file_path in files_to_delete:
            #delete all identified files
            try:
                #attempt to delete the files in directory
                os.remove(file_path)
                #print(f"File {file_path} has been deleted")
            except Exception as e:
                print(f"An error occurred: {e}")

    #remove images in blender with basename "preview"
    images_to_remove = [img for img in bpy.data.images if img.name.startswith(remove_prev)]

    for img in images_to_remove:
        #check if the basename matches
        bpy.data.images.remove(img)
        #print(f"Image '{img.name}' has been removed from Blender.")
    refresh_enum(True, True)


def render_complete_alert(self, context):
    scene = bpy.context.scene
    #load the sound file
    #path to sound file
    #sound options
    render_complete_sound = "Render_Completed4.wav"
    render_anim_complete_sound = "Render_Animation_Completed4.wav"

    sfx = os.path.dirname(__file__) #path of the current script
    parent_directory = os.path.dirname(sfx)
    sound_path_render = os.path.join(parent_directory, "sfx/sounds", render_complete_sound)
    sound_path_anim_render = os.path.join(parent_directory, "sfx/sounds", render_anim_complete_sound)

    cycles_sound = aud.Sound(sound_path_render)
    cycles_anim_sound = aud.Sound(sound_path_anim_render)

    device = aud.Device()

    if scene.renderAnim == False:
        handle_cycles = device.play(cycles_sound)
    else:
        handle_anim_cycles = device.play(cycles_anim_sound)

def opengl_complete_alert(self, context):
    scene = bpy.context.scene
    #load the sound file
    #path to sound file
    #sound options
    viewport_captured_sound = "Viewport_Captured2.wav"
    viewport_Animation_captured_sound = "Viewport_Animation_Captured2.wav"

    sfx = os.path.dirname(__file__) #path of the current script
    parent_directory = os.path.dirname(sfx)
    sound_path_opengl = os.path.join(parent_directory, "sfx/sounds", viewport_captured_sound)
    sound_path_opengl_anim = os.path.join(parent_directory, "sfx/sounds", viewport_Animation_captured_sound)

    opengl_sound = aud.Sound(sound_path_opengl)
    opengl_animation_sound = aud.Sound(sound_path_opengl_anim)

    device = aud.Device()

    if scene.renderAnim == False:
        handle_gl = device.play(opengl_sound)
    else:
        hanlde_gl_anim = device.play(opengl_animation_sound)


def refresh_enum(self, context):
    #refresh the enum
    scene = bpy.context.scene
    scene.renderLockUI = False

    preview_selector.refresh_image_enum(None, bpy.context)

    #set the latest image as the displayed image on enum
    preview_selector.set_enum_to_latest_image()


#open gl call
def update_enum():
    refresh_enum(True, True)

    save_post_handler()

    bpy.app.timers.unregister(update_enum)


#set the filepath back to '/tmp\' after opengl render
def filepath_default():
    scene = bpy.context.scene
    global current_filepath
    global directory
    global directory_filename

    if directory:
            bpy.context.scene.render.filepath = os.path.join(directory, directory_filename)

    else:
        bpy.context.scene.render.filepath = '/tmp\\'

    bpy.app.timers.unregister(filepath_default)

    if scene.renderpostnotify == True:
        opengl_complete_alert(True, True)

#OPEN RENDERED WINDOW
def ShowRender(showrender):
    bpy.ops.render.view_show('INVOKE_DEFAULT')

#clear custom render settings to default
def ClearSelSets(clearselsets):
    gv()
    #storing the previous selected objects
    previous_selection = bpy.context.selected_objects

    spaceData = bpy.context.space_data
    nonMesh = [
        "show_object_viewport_armature",
        "show_object_viewport_lattice",
        "show_object_viewport_empty",
        "show_object_viewport_light",
        "show_object_viewport_light_probe",
        "show_object_viewport_camera",
        "show_object_viewport_speaker"
    ]
    ####--------------------------------------------##########
    #hide elements we don't want to select
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    hide_nonmesh(space, nonMesh)

    #invert selection selecting all mesh types
    bpy.ops.object.select_all(action = 'SELECT')

    objSel = bpy.context.selected_objects
    for x in range(len(objSel)):
        o = bpy.context.selected_objects[x]
        bpy.context.view_layer.objects.active = o
        o.select_set(state = True)

        bpy.context.object.is_shadow_catcher = False
        bpy.context.object.is_holdout = False

        bpy.context.object.visible_camera = True

        #check for particle systems in "unselected" set if any
        for obj in bpy.data.objects:
            for mod in gv.obj.modifiers:
                if mod.type == 'PARTICLE_SYSTEM':
                    mod.show_viewport = True
                    mod.show_render = True

    #Show elements we don't want to select
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    show_nonmesh(space, nonMesh)

    bpy.ops.object.select_all(action = 'DESELECT')

    #restore the previous selected objects and set one of them active
    for gv.obj in previous_selection:
        gv.obj.select_set(True)

    #set the last object in the previously selected list as the active object
    if previous_selection:
        bpy.context.view_layer.objects.active = previous_selection[-1]

#render settings
def renderperf(self, context):
    gv()
    if gv.scene.performance == True:
        gv.scene.renderSamples = False

def rendersamp(self, context):
    gv()
    if gv.scene.renderSamples == True:
        gv.scene.performance = False

def use_ao(self, context):
    gv()
    sc = gv.scene
    if sc.use_AmbOcc == True:
        sc.useBloom = False
        sc.use_screen_space_reflections = False
        sc.riuse_motion_blur = False
        sc.volumetric_lighting = False
        sc.volumetric_shadows = False
        sc.depthoffield = False
        sc.subsurfscat = False
        sc.rivolumetrics = False
        sc.ricurves = False
        sc.rishadows = False

def use_bloom(self, context):
    gv()
    sc = gv.scene
    if sc.useBloom == True:
        sc.use_AmbOcc = False
        sc.use_screen_space_reflections = False
        sc.riuse_motion_blur = False
        sc.volumetric_lighting = False
        sc.volumetric_shadows = False
        sc.depthoffield = False
        sc.subsurfscat = False
        sc.rivolumetrics = False
        sc.ricurves = False
        sc.rishadows = False

def use_ssr(self, context):
    gv()
    sc = gv.scene
    if sc.use_screen_space_reflections == True:
        sc.use_AmbOcc = False
        sc.useBloom = False
        sc.riuse_motion_blur = False
        sc.volumetric_lighting = False
        sc.volumetric_shadows = False
        sc.depthoffield = False
        sc.subsurfscat = False
        sc.rivolumetrics = False
        sc.ricurves = False
        sc.rishadows = False

def use_Moblur(self, context):
    gv()
    sc = gv.scene
    if sc.riuse_motion_blur == True:
        sc.use_AmbOcc = False
        sc.useBloom = False
        sc.use_screen_space_reflections = False
        sc.volumetric_lighting = False
        sc.volumetric_shadows = False
        sc.depthoffield = False
        sc.subsurfscat = False
        sc.rivolumetrics = False
        sc.ricurves = False
        sc.rishadows = False

def use_vol_light(self, context):
    gv()
    sc = gv.scene
    if sc.volumetric_lighting == True:
        sc.use_AmbOcc = False
        sc.useBloom = False
        sc.use_screen_space_reflections = False
        sc.riuse_motion_blur = False
        sc.volumetric_shadows = False
        sc.depthoffield = False
        sc.subsurfscat = False
        sc.rivolumetrics = False
        sc.ricurves = False
        sc.rishadows = False


def use_vol_shadows(self, context):
    gv()
    sc = gv.scene
    if sc.volumetric_shadows == True:
        sc.use_AmbOcc = False
        sc.useBloom = False
        sc.use_screen_space_reflections = False
        sc.riuse_motion_blur = False
        sc.volumetric_lighting = False
        sc.depthoffield = False
        sc.subsurfscat = False
        sc.rivolumetrics = False
        sc.ricurves = False
        sc.rishadows = False

def use_dof(self, context):
    gv()
    sc = gv.scene
    if sc.depthoffield == True:
        sc.use_AmbOcc = False
        sc.useBloom = False
        sc.use_screen_space_reflections = False
        sc.riuse_motion_blur = False
        sc.volumetric_lighting = False
        sc.volumetric_shadows = False
        sc.subsurfscat = False
        sc.rivolumetrics = False
        sc.ricurves = False
        sc.rishadows = False

def use_sss(self, context):
    gv()
    sc = gv.scene
    if sc.subsurfscat == True:
        sc.use_AmbOcc = False
        sc.useBloom = False
        sc.use_screen_space_reflections = False
        sc.riuse_motion_blur = False
        sc.volumetric_lighting = False
        sc.volumetric_shadows = False
        sc.depthoffield = False
        sc.rivolumetrics = False
        sc.ricurves = False
        sc.rishadows = False


def use_vol(self, context):
    gv()
    sc = gv.scene
    if sc.rivolumetrics == True:
        sc.use_AmbOcc = False
        sc.useBloom = False
        sc.use_screen_space_reflections = False
        sc.riuse_motion_blur = False
        sc.volumetric_lighting = False
        sc.volumetric_shadows = False
        sc.depthoffield = False
        sc.subsurfscat = False
        sc.ricurves = False
        sc.rishadows = False

def use_curves(self, context):
    gv()
    sc = gv.scene
    if sc.ricurves == True:
        sc.use_AmbOcc = False
        sc.useBloom = False
        sc.use_screen_space_reflections = False
        sc.riuse_motion_blur = False
        sc.volumetric_lighting = False
        sc.volumetric_shadows = False
        sc.depthoffield = False
        sc.subsurfscat = False
        sc.rivolumetrics = False
        sc.rishadows = False

def use_shadows(self, context):
    gv()
    sc = gv.scene
    if sc.rishadows == True:
        sc.use_AmbOcc = False
        sc.useBloom = False
        sc.use_screen_space_reflections = False
        sc.riuse_motion_blur = False
        sc.volumetric_lighting = False
        sc.volumetric_shadows = False
        sc.depthoffield = False
        sc.subsurfscat = False
        sc.rivolumetrics = False
        sc.ricurves = False

def holdout(self, context):
    gv() #load global variables

    if gv.scene.renderHoldouts == True:
        gv.scene.renderCamVisible = False

def invisible(self, context):
    gv() #load global variables

    if gv.scene.renderCamVisible == True:
        gv.scene.renderHoldouts = False

def renderTransparency(self, context):
    gv() #load global variables

    bpy.context.scene.render.film_transparent = gv.scene.fTransparent

def rendertransparentGlass(self, context):
    gv() #load global variables

    bpy.context.scene.cycles.film_transparent_glass = gv.scene.transparentGlass


def global_subSample(self, context):
    gv() #load global variables

    bpy.context.scene.cycles.diffuse_samples = gv.scene.subsampleGlobal
    bpy.context.scene.cycles.glossy_samples = gv.scene.subsampleGlobal
    bpy.context.scene.cycles.transmission_samples = gv.scene.subsampleGlobal
    bpy.context.scene.cycles.ao_samples = gv.scene.subsampleGlobal
    bpy.context.scene.cycles.mesh_light_samples = gv.scene.subsampleGlobal
    bpy.context.scene.cycles.subsurface_samples = gv.scene.subsampleGlobal
    bpy.context.scene.cycles.volume_samples = gv.scene.subsampleGlobal

#visibility functions
def viewPortRender(self, context):
    gv() #load global variables
    sel = len(bpy.context.selected_objects)
    objSel = range(sel)

    gv.scene.screenCaps = False

    for x in objSel:
        ob = bpy.context.selected_objects[x]
        bpy.context.view_layer.objects.active = ob
        ob.select_set(state = True)

        bpy.context.object.hide_render = 1-gv.scene.visRenders


def viewPortHold(self, context):
    gv() #load global variables
    sel = len(bpy.context.selected_objects)
    objSel = range(sel)

    for x in objSel:
        ob = bpy.context.selected_objects[x]
        bpy.context.view_layer.objects.active = ob
        ob.select_set(state = True)

        if gv.scene.visHold == True:
            bpy.context.object.is_holdout = True
        else:
            bpy.context.object.is_holdout = False

def visShadowCatcher(self, context):
    gv() #load global variables
    sel = len(bpy.context.selected_objects)
    objSel = range(sel)

    for x in objSel:
        ob = bpy.context.selected_objects[x]
        bpy.context.view_layer.objects.active = ob
        ob.select_set(state = True)

        if gv.scene.visShadCatch == True:
            bpy.context.object.is_shadow_catcher = True
        else:
            bpy.context.object.is_shadow_catcher = False


#ray visibility
def rayCamera(self, context):
    gv() #load global variables
    sel = len(bpy.context.selected_objects)
    objSel = range(sel)

    for x in objSel:
        ob = bpy.context.selected_objects[x]
        bpy.context.view_layer.objects.active = ob
        ob.select_set(state = True)

        if gv.scene.rVisCamera == True:
            bpy.context.object.visible_camera = True
        else:
            bpy.context.object.visible_camera = False

def rayDiffuse(self, context):
    gv() #load global variables
    sel = len(bpy.context.selected_objects)
    objSel = range(sel)

    for x in objSel:
        ob = bpy.context.selected_objects[x]
        bpy.context.view_layer.objects.active = ob
        ob.select_set(state = True)

        if gv.scene.rVisDif == True:
            bpy.context.object.visible_diffuse = True
        else:
            bpy.context.object.visible_diffuse = False


def rayGlossy(self, context):
    gv() #load global variables
    sel = len(bpy.context.selected_objects)
    objSel = range(sel)

    for x in objSel:
        ob = bpy.context.selected_objects[x]
        bpy.context.view_layer.objects.active = ob
        ob.select_set(state = True)

        if gv.scene.rVisGlos == True:
            bpy.context.object.visible_glossy = True
        else:
            gv.scene.rVisGlos = False


def rayTransmission(self, context):
    gv() #load global variables
    sel = len(bpy.context.selected_objects)
    objSel = range(sel)

    for x in objSel:
        ob = bpy.context.selected_objects[x]
        bpy.context.view_layer.objects.active = ob
        ob.select_set(state = True)

        if gv.scene.rVisTran == True:
            bpy.context.object.visible_transmission = True
        else:
            bpy.context.object.visible_transmission = False


def rayVolume(self, context):
    gv() #load global variables
    sel = len(bpy.context.selected_objects)
    objSel = range(sel)

    for x in objSel:
        ob = bpy.context.selected_objects[x]
        bpy.context.view_layer.objects.active = ob
        ob.select_set(state = True)

        if gv.scene.rVisVol == True:
            bpy.context.object.visible_volume_scatter = True
        else:
            bpy.context.object.visible_volume_scatter = False

def rayShadow(self, context):
    gv() #load global variables
    sel = len(bpy.context.selected_objects)
    objSel = range(sel)

    for x in objSel:
        ob = bpy.context.selected_objects[x]
        bpy.context.view_layer.objects.active = ob
        ob.select_set(state = True)

        if gv.scene.rVisShad == True:
            bpy.context.object.visible_shadow = True
        else:
            bpy.context.object.visible_shadow = False


def EeveePassVolumeTransmittance(self, context):
    gv() #load global variables
    bpy.context.view_layer.eevee.use_pass_volume_transmittance = gv.scene.eeveePassVolTrans

def EeveePassVolumeScatter(self, context):
    gv() #load global variables
    bpy.context.view_layer.eevee.use_pass_volume_scatter = gv.scene.eeveePassVolScat

def EeveeBloomEffect(self, context):
    gv() #load global variables
    bpy.context.view_layer.eevee.use_pass_bloom = gv.scene.bloomEffect


#passes
def passdat(self, context):
    gv() #load global variabls
    if gv.scene.passData == True:
        gv.scene.passLight = False
        gv.scene.passCryptoMatte = False

def passlit(self, context):
    gv() #load global variables
    if gv.scene.passLight == True:
        gv.scene.passData = False
        gv.scene.passCryptoMatte = False
def passcryptmat(self, context):
    gv() #load global variabls
    if gv.scene.passCryptoMatte == True:
        gv.scene.passLight = False
        gv.scene.passData = False

def ClayRenderMTL(clayrendermtl):
    gv() #load global variables
    bpy.data.materials.new(name= "Clay Render MTL")
    bpy.data.materials["Clay Render MTL"].use_nodes = True
    bpy.data.materials["Clay Render MTL"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.522522, 0.522522, 0.522522, 1)

    bpy.context.scene.view_layers["ViewLayer"].material_override = bpy.data.materials["Clay Render MTL"]

    gv.scene.mtlOverrideOn = True


def ClayOn(self, context):
    gv() #load global variables

    if gv.scene.mtlOverrideOn == True:
        gv.scene.mtlOverrideOff = False
    bpy.context.scene.view_layers["ViewLayer"].material_override = bpy.data.materials["Clay Render MTL"]

def ClayOff(self, context):
    gv() #load global variables

    if gv.scene.mtlOverrideOff == True:
        gv.scene.mtlOverrideOn = False
    bpy.context.scene.view_layers["ViewLayer"].material_override = None

def RenderLockInterface(self, context):
    gv() #load global variables
    scene = bpy.context.scene

    scene.render.use_lock_interface = gv.scene.renderLockUI

#dimension presets
def onekrenderstill(onekstill):
    gv() #load global variables
    gv.scene.render.resolution_x = 1024
    gv.scene.render.resolution_y = 1024

def twokrenderstill(twokstill):
    gv() #load global variables
    gv.scene.render.resolution_x = 2048
    gv.scene.render.resolution_y = 2048

def fourkrenderstill(fourkstill):
    gv() #load global variables
    gv.scene.render.resolution_x = 4096
    gv.scene.render.resolution_y = 4096

def standardanimrender(standardanim):
    gv() #load global variables
    gv.scene.render.resolution_x = 1920
    gv.scene.render.resolution_y = 1080

def highresanimrender(highresanim):
    gv() #load global variables
    gv.scene.render.resolution_x = 3840
    gv.scene.render.resolution_y = 2160

def userenderdenoise(self, context):
    gv() #load global variables
    obj = bpy.context.object

    bpy.context.scene.cycles.use_denoising = gv.scene.samplesRenderDenoise

def useviewportdenoise(self, context):
    gv() #load global variables
    obj = bpy.context.object

    bpy.context.scene.cycles.use_preview_denoising = gv.scene.samplesVPDenoise

def rendersampling(self, context):
    gv() #load global variables
    if gv.scene.samplesRender == True:
        gv.scene.samplesVP = False
def rendersamplingVP(self, context):
    gv() #load global variables
    if gv.scene.samplesVP == True:
        gv.scene.samplesRender = False


def register():
    check_filepath_handler()

def unregister():
    try:
        bpy.app.timers.unregister(load_post_enum)
        bpy.app.handlers.load_post.remove(check_filepath)
    except:
        pass
