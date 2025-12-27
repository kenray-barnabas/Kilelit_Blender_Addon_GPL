import bpy
import os
import webbrowser
import time

from bpy.types import *
from bpy.props import *
import bpy.utils.previews
from bpy.app.handlers import persistent


#import Kilelit
from Kilelit import icons, ops, utils, thumb
from Kilelit.icons import icons_load
from Kilelit.ops import operators
from Kilelit.utils import kilelit_functions, preview_selector, openwebpages
from Kilelit.thumb import renderhistory


def gv():
    gv.scene = bpy.context.scene
    #path to save image
    script_path = os.path.dirname(__file__) #path of the current script
    parent_directory = os.path.dirname(script_path)
    gv.folder_path = os.path.join(parent_directory, "thumb\images")

#rendering
def holdout(self, context):
    kilelit_functions.holdout(self, context)
def invisible(self, context):
    kilelit_functions.invisible(self, context)

def renderTransparency(self, context):
    kilelit_functions.renderTransparency(self, context)
def rendertransparentGlass(self, context):
    kilelit_functions.rendertransparentGlass(self, context)
def renderviewport(self, context):
    kilelit_functions.renderviewport(self, context)
def renderselonly(self, context):
    kilelit_functions.renderselonly(self, context)

#rendersettings
def renderperf(self, context):
    kilelit_functions.renderperf(self, context)
def rendersamp(self, context):
    kilelit_functions.rendersamp(self, context)

#visibility
def viewPortHold(self, context):
    kilelit_functions.viewPortHold(self, context)
def viewPortRender(self, context):
    kilelit_functions.viewPortRender(self, context)
def visShadowCatcher(self, context):
    kilelit_functions.visShadowCatcher(self, context)

#ray visibility
def rayCamera(self, context):
    kilelit_functions.rayCamera(self, context)
def rayDiffuse(self, context):
    kilelit_functions.rayDiffuse(self, context)
def rayGlossy(self, context):
    kilelit_functions.rayGlossy(self, context)
def rayTransmission(self, context):
    kilelit_functions.rayTransmission(self, context)
def rayVolume(self, context):
    kilelit_functions.rayVolume(self, context)
def rayShadow(self, context):
    kilelit_functions.rayShadow(self, context)

#rendersettings
def useviewportdenoise(self, context):
    kilelit_functions.useviewportdenoise(self, context)
def userenderdenoise(self, context):
    kilelit_functions.userenderdenoise(self, context)

#passes
def passdat(self, context):
    kilelit_functions.passdat(self, context)
def passlit(self, context):
    kilelit_functions.passlit(self, context)
def passcryptmat(self, context):
    kilelit_functions.passcryptmat(self, context)

#color management
def global_subSample(self, context):
    kilelit_functions.global_subSample(self, context)
def EeveePassVolumeTransmittance(self, context):
    kilelit_functions.EeveePassVolumeTransmittance(self, context)
def EeveePassVolumeScatter(self, context):
    kilelit_functions.EeveePassVolumeScatter(self, context)
def EeveeBloomEffect(self, context):
    kilelit_functions.EeveeBloomEffect(self, context)
def ClayOn(self, context):
    kilelit_functions.ClayOn(self, context)
def ClayOff(self, context):
    kilelit_functions.ClayOff(self, context)
def RenderLockInterface(self, context):
    kilelit_functions.RenderLockInterface(self, context)

#light linking
def rilightgroup(self, context):
    kilelit_functions.rilightgroup(self, context)
def rilightlinks(self, context):
    kilelit_functions.rilightlinks(self, context)
def rishadowlinks(self, context):
    kilelit_functions.rishadowlinks(self, context)

#sampling buttons
def rendersampling(self, context):
    kilelit_functions.rendersampling(self, context)
def rendersamplingVP(self, context):
    kilelit_functions.rendersamplingVP(self, context)

#image preview update and selector
def get_images(self, context):
    preview_selector.get_images(self, context)

def isshadowcatcher(self, context):
    kilelit_functions.isshadowcatcher(self, context)

def historypathset(self, context):
    kilelit_functions.historypathset(self, context)

#Eevee toggle switch functions
def use_ao(self, context):
    kilelit_functions.use_ao(self, context)

def use_bloom(self, context):
    kilelit_functions.use_bloom(self, context)

def use_ssr(self, context):
    kilelit_functions.use_ssr(self, context)

def use_Moblur(self, context):
    kilelit_functions.use_Moblur(self, context)

def use_vol_light(self, context):
    kilelit_functions.use_vol_light(self, context)

def use_vol_shadows(self, context):
    kilelit_functions.use_vol_shadows(self, context)

def use_dof(self, context):
    kilelit_functions.use_dof(self, context)

def use_sss(self, context):
    kilelit_functions.use_sss(self, context)

def use_vol(self, context):
    kilelit_functions.use_vol(self, context)

def use_curves(self, context):
    kilelit_functions.use_curves(self, context)

def use_shadows(self, context):
    kilelit_functions.use_shadows(self, context)

def has_geometry_visibility(ob):
    ob = bpy.context.object
    return ob and ((ob.type in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META', 'LIGHT', 'EMPTY', 'CAMERA', 'ARMATURE'}) or
                   (ob.instance_type == 'COLLECTION' and ob.instance_collection))


class View3DPanel():
    bl_category = "Kilelit"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "KB Tools"
    bl_options = {'DEFAULT_CLOSED'}

class kbkilelit(View3DPanel, bpy.types.Panel):
    bl_idname = "KB_PT_Render_panel"
    bl_label = "Render"

    def draw(self, context):
        layout = self.layout

        obj = bpy.context.object
        sel = len(bpy.context.selected_objects)
        scene = bpy.context.scene


        rd = context.scene.render
        image_settings = rd.image_settings
        scene = context.scene
        cscene = scene.cycles
        props = scene.eevee
        aa = cscene.samples
        rEngine = bpy.context.scene.render.engine
        prefs = context.preferences
        view = prefs.view


        #custom icons
        kbicons = icons_load.kilelit_icons
        #Render Engines
        col = layout.box()
        if rd.has_multiple_engines:
            col.prop(rd, "engine", text="Render Engine")

        col.prop(cscene, "feature_set")
        col.prop(cscene, "device")

        col = layout.column()
        col.label(text = "-------------------------------------------------------------------------------------------------------------------------")
        # Progress Bar
        #layout.template_running_jobs()

        box = layout.box()
        col0 = box.column()
        col0.scale_y = 2
        col0.operator("myct.renderbutton", text = "RENDER", icon_value = kbicons["kicam"].icon_id)

        col0 = layout.column()
        col0.prop(scene, "renderpostnotify", text = "Sound on render complete")
        # Messages
        col0 = layout.column()
        col0.scale_y = 1
        col0.template_reports_banner()

        col0 = layout.column()
        col0.prop(view, "render_display_type", text="Render In")

        if (scene.generate_previews == False):
            box = layout.box()
            col1 = box.column()
            col1.scale_y = 1.25
            col1.prop(scene, "generate_previews", text = "Enable Render History", toggle = True, icon_value=kbicons["kisavefile"].icon_id)
        elif (scene.generate_previews == True):
            box = layout.box()
            row = box.row()
            col1 = row.column(align=True)
            col1.alignment = 'LEFT'
            col1.scale_y = 1.25
            col1.scale_x = 1.75
            col1.prop(scene, "generate_previews", text = "Disable Render History", toggle=True, icon_value = kbicons["kisavefile"].icon_id)
            if (scene.generate_previews == True):
                col1 = row.column(align=True)
                col1.alignment = 'RIGHT'
                col1.scale_y = 1.25
                col1.alert = True
                col1.operator("myct.clearrenderhistory", text = "Empty", icon_value = kbicons["kitrashcan"].icon_id)
                row = box.row()
                col = row.column(align=True)
                col.scale_x = 1
                col.alignment = 'LEFT'

                if (scene.lock_renderhistory_path == False):
                    col.prop(scene, "lock_renderhistory_path", text="", icon_value=kbicons["kiunlocked"].icon_id)
                elif(scene.lock_renderhistory_path == True):
                    col.prop(scene, "lock_renderhistory_path", text="", icon_value=kbicons["kilocked"].icon_id)

                if (scene.lock_renderhistory_path == False):
                    col = row.column(align=True)
                    col.scale_x = 1
                    col.alignment = 'RIGHT'
                    col.prop(scene, "render_history_path", text="")
                elif (scene.lock_renderhistory_path == True):
                    col = row.column(align=True)
                    col.scale_x = 1
                    col.alignment = 'RIGHT'
                    col.label(text = str(scene.render_history_path))

                if (scene.render_history_path != ""):
                    #render preview history
                    try:
                        render_history_prev = "render_history_previews"
                        render_images = scene.render_history_previews

                        row = box.row()
                        row.template_icon_view(scene, render_history_prev, show_labels=True, scale=6)

                        if "_rendersomething" in scene.render_history_path:
                            scene.render_history_previews = "_rendersomething"

                        col = box.column()
                        col.scale_y = 1.25
                        col.operator("myct.open_exploerer", text = "Open History Location", icon_value=kbicons["kifolder"].icon_id)

                    except:
                        pass
        #RENDER SPECIALS
        box = layout.box()
        uigivp = box.column_flow(columns=3, align = True)
        uigivp.scale_y = 1.25

        if (scene.renderLockUI == True):
            uigivp.prop(scene, "renderLockUI", text = "UI Locked In Render", toggle=True, icon_value=kbicons["kilocked"].icon_id)
        elif (scene.renderLockUI == False):
            uigivp.prop(scene, "renderLockUI", text = "UI Unlocked In Render", toggle=True, icon_value=kbicons["kiunlocked"].icon_id)

        #use fase global illumination
        uigivp.prop(cscene, "use_fast_gi", text = "Fast GI Approximation", toggle =True, icon_value = kbicons["kigi"].icon_id)

        uigivp.operator("myct.showmyrender", text = "View Render", icon_value = kbicons["kiviewrender"].icon_id)

        colRS = box.column_flow(columns = 2, align = True)
        colRS.scale_y = 1.25
        colRS.prop(scene, "renderAnim", text = "Animation", toggle = True, icon_value = kbicons["kianim"].icon_id)

        colRS.prop(scene, "renderselected", text = "Selected Only", toggle = True, icon_value = kbicons["kiselonly"].icon_id)

        colRS.prop(scene, "fTransparent", text = "Transparent", toggle = True, icon_value = kbicons["kitransparent"].icon_id)

        colRS.prop(scene, "screenCaps", text = "ViewPort Render", toggle = True, icon_value = kbicons["kivprender"].icon_id)
        colTG = layout.column_flow(columns = 1, align = True)

        if rEngine == 'CYCLES':
            if (scene.fTransparent == True):
                colTG.prop(scene, "transparentGlass", text = "Transparent Glass")
                #glass roughness
                if (scene.transparentGlass == True):
                    colTG.prop(cscene, "film_transparent_roughness", text="Roughness Threshold")

        if (scene.renderselected == True):
            #box = layout.box()
            #DISABLED operator button
            #col = box.column()
            #col.scale_y = 1.25
            #col.operator("myct.clearcustrendersettings", text = "Clear Selected Only Settings", icon_value = kbicons["kiclearselonly"].icon_id)


            col = layout.box()
            if obj is not None:
                col.label(text = "Selected Only Object: " + obj.name)
            else:
                col.label(text = "Nothing is selected")

            box = layout.box()
            col1 = box.column()
            col1.scale_y = 1.25
            col1.label(text = "Uses Methods:")
            if rEngine == 'CYCLES':
                col1.prop(scene, "rendershadowcatcher", text = "Render Shadow Catcher", icon_value = kbicons["kishadowcatch"].icon_id)

            col1 = box.column()
            col1.label(text = "METHODS:")

            col1.prop(scene, "renderHoldouts", text = "Holdout unselected")
            if rEngine == 'CYCLES':
                col1.prop(scene, "renderCamVisible", text = "Invisible unselected")
            col1.separator()

class kbrenderperformance(View3DPanel, bpy.types.Panel):
    bl_idname = "KB_PT_kbrenderperformance_panel"
    bl_label = "Render Settings"

    def draw(self, context):
        import _cycles

        layout = self.layout
        obj = bpy.context.object
        scene = bpy.context.scene
        props = scene.eevee
        rd = context.scene.render
        cscene = scene.cycles
        view_layer = context.view_layer
        cycles_view_layer = view_layer.cycles
        rEngine = bpy.context.scene.render.engine

        kbicons = icons_load.kilelit_icons

        colmain = layout.column_flow(columns = 2, align = True)
        colmain.scale_y = 1.25

        #sampling
        layout.use_property_split = False
        colmain.prop(scene, "renderSamples", text = "Sampling", toggle = True, icon_value = kbicons["kisamples"].icon_id)

        if (scene.renderSamples == True):
            if rEngine == 'CYCLES':
                box = layout.box()
                colsubmain = box.column_flow(columns=2, align=True)

                #rendering sampling
                box.use_property_split = False
                colsubmain.prop(scene, "samplesRender", text = "Render Sampling", toggle=True)

                #render sampling
                if (scene.samplesRender == True):
                    box.use_property_split = True
                    box.use_property_decorate = False

                    heading = box.column(align=True, heading="Noise Threshold")
                    row = heading.row(align=True)
                    row.prop(cscene, "use_adaptive_sampling", text="")
                    sub = row.row()
                    sub.active = cscene.use_adaptive_sampling
                    sub.prop(cscene, "adaptive_threshold", text="")

                    col = box.column(align=True)
                    if cscene.use_adaptive_sampling:
                        col.prop(cscene, "samples", text=" Max Samples")
                        col.prop(cscene, "adaptive_min_samples", text="Min Samples")
                    else:
                        col.prop(cscene, "samples", text="Samples")
                    col.prop(cscene, "time_limit")

                    box.use_property_split = False
                    col = box.column(align = True)

                    col.prop(scene, "samplesRenderDenoise", text=" Render Denoise")
                    if (scene.samplesRenderDenoise == True):

                        #Render denoising
                        col.label(text = "Render Denoising")
                        col.active = cscene.use_denoising
                        col.prop(cscene, "denoiser", text="Denoiser")
                        col.prop(cscene, "denoising_input_passes", text="Passes")
                        if cscene.denoiser == 'OPENIMAGEDENOISE':
                            col.prop(cscene, "denoising_prefilter", text="Prefilter")
                            col.prop(cscene, "denoising_quality", text ="Quality")
                            col.prop(cscene, "denoising_use_gpu", toggle = True, text = "Use GPU")

                colsubmain.prop(scene, "samplesVP", text = "Viewport Sampling", toggle=True)

                #viewport sampling
                if (scene.samplesVP == True):
                    box.use_property_split = True
                    box.use_property_decorate = False

                    heading = box.column(align=True, heading="Noise Threshold")
                    row = heading.row(align=True)
                    row.prop(cscene, "use_preview_adaptive_sampling", text="")
                    sub = row.row()
                    sub.active = cscene.use_preview_adaptive_sampling
                    sub.prop(cscene, "preview_adaptive_threshold", text="")

                    if cscene.use_preview_adaptive_sampling:
                        col = box.column(align=True)
                        col.prop(cscene, "preview_samples", text=" Max Samples")
                        col.prop(cscene, "preview_adaptive_min_samples", text="Min Samples")
                    else:
                        layout.prop(cscene, "preview_samples", text="Samples")

                    #viewport denoising
                    layout.use_property_split = False
                    col = box.column(align = True)
                    col.prop(scene, "samplesVPDenoise", text="Viewport Denoise")
                    if (scene.samplesVPDenoise == True):
                        col.prop(cscene, "preview_denoiser", text="Denoiser")
                        col.prop(cscene, "preview_denoising_input_passes", text="Passes")

                        if bpy.context.scene.cycles.preview_denoiser == 'OPENIMAGEDENOISE':
                            col.prop(cscene, "preview_denoising_prefilter", text="Prefilter")

                        col.prop(cscene, "preview_denoising_start_sample", text="Start Sample")

                #advanced
                box = layout.box()
                col = box.column()
                col.prop(scene, "advanced", text = "Advanced", toggle = True, icon_value = kbicons["kiadvanced"].icon_id)
                if (scene.advanced == True):
                    row = box.row(align=True)
                    row.prop(cscene, "seed")
                    row.prop(cscene, "use_animated_seed", text="", icon='TIME')
                    col = box.column()
                    col.prop(cscene, "sample_offset")

                    col.separator()

                    heading = box.column(align=True, heading="Scrambling Distance")
                    heading.active = (cscene.sampling_pattern == 'TABULATED_SOBOL' or not CyclesDebugButtonsPanel.poll(context))
                    heading.prop(cscene, "auto_scrambling_distance", text="Automatic")
                    sub = heading.row()
                    sub.active = not cscene.use_preview_adaptive_sampling
                    sub.prop(cscene, "preview_scrambling_distance", text="Viewport")
                    heading.prop(cscene, "scrambling_distance", text="Multiplier")

                    col = box.column(align=True)
                    col.prop(cscene, "min_light_bounces")
                    col.prop(cscene, "min_transparent_bounces")

                    for view_layer in scene.view_layers:
                        if view_layer.samples > 0:
                            box.separator()
                            box.row().prop(cscene, "use_layer_samples")
                            break

                    col.separator()

                    col = box.column(align=True)
                    col.active = not (cscene.use_adaptive_sampling and cscene.use_preview_adaptive_sampling)
                    col.prop(cscene, "sampling_pattern", text="Pattern")

                    col.separator()

                #lights
                col = box.column()
                col.prop(scene, "lights", text = "Lights", toggle = True, icon_value=kbicons["kilights"].icon_id)
                if (scene.lights == True):
                    col.prop(cscene, "use_light_tree")
                    if (cscene.use_light_tree == True):
                        col.label(text = "Light Threshold: " + str(round(cscene.light_sampling_threshold, 3)))
                    else:
                        col.prop(cscene, "light_sampling_threshold", text="Light Threshold")

                    col.separator()

                col = box.column()
                col.prop(scene, "lightpaths", text = "Light Paths", toggle = True, icon_value=kbicons["kilightpaths"].icon_id)
                if (scene.lightpaths == True):
                    col.separator()
                    col.label(text = "Max Bounces")
                    col.prop(cscene, "max_bounces", text = "Total")
                    col = box.column()
                    col.prop(cscene, "diffuse_bounces", text = "Diffuse")
                    col.prop(cscene, "glossy_bounces", text = "Glossy")
                    col.prop(cscene, "transmission_bounces", text = "Transmission")
                    col.prop(cscene, "volume_bounces", text = "Volume")
                    col.separator()
                    col.prop(cscene, "transparent_max_bounces", text = "Transparent")
                    col.separator()
                    col.label(text = "Clampling")
                    col.prop(cscene, "sample_clamp_direct", text = "Direct Light")
                    col.prop(cscene, "sample_clamp_indirect", text = "Indirect Light")
                    col.separator()
                    col.label(text = "Caustics")
                    col.prop(cscene, "blur_glossy")
                    col.prop(cscene, "caustics_reflective", text = "Reflective")
                    col.prop(cscene, "caustics_refractive", text = "Refractive")
                    col.separator()

                col = box.column()
                col.prop(cscene, "use_fast_gi", text = "Fast GI Approximation", toggle =True, icon_value = kbicons["kigi"].icon_id)
                if (cscene.use_fast_gi == True):
                    col.prop(cscene, "fast_gi_method", text = "Method")
                    world = scene.world
                    if world:
                        light = world.light_settings
                        col.prop(light, "ao_factor", text = "AO Factor")
                        col.prop(light, "distance", text = "AO Distance")

                    if cscene.fast_gi_method == 'REPLACE':
                        col.prop(cscene, "ao_bounces", text = "Viewport Bounces")
                        col.prop(cscene, "ao_bounces_render", text = "Render Bounces")

            elif rEngine == 'BLENDER_EEVEE':
                box = layout.box()
                col = box.column()
                col.prop(props, "taa_render_samples", text = "Render")
                col.prop(props, "taa_samples", text = "Viewport")
                col.prop(props, "use_taa_reprojection")

                col0 = box.column_flow(columns=9, align=True)
                col0.prop(scene, "use_AmbOcc", text = "AO", toggle = True)
                if (scene.use_AmbOcc == True):
                    col1 = box.column()
                    col1.prop(props, "use_gtao", text = "Use Ambient Occlusion")
                    col2 = box.column()
                    col2.active = props.use_gtao
                    col2.prop(props, "gtao_distance", text = "Distance:" )
                    col2.prop(props, "gtao_factor", text = "Factor:")
                    col2.prop(props, "gtao_quality", text = "Trace Precision:")
                    col2.prop(props, "use_gtao_bent_normals", text = "Bent Normals")
                    col2.prop(props, "use_gtao_bounce", text = "Bounces Approximation")

                col0.prop(scene, "useBloom", text = "Bloom", toggle = True)
                if (scene.useBloom == True):
                    col1 = box.column()
                    col1.prop(props, "use_bloom", text = "Use Bloom")
                    col2 = box.column()
                    col2.active = props.use_bloom
                    col2.prop(props, "bloom_threshold", text = "Threshold:")
                    col2.prop(props, "bloom_knee", text = "Knee:")
                    col2.prop(props, "bloom_radius", text = "Radius:")
                    col2.prop(props, "bloom_color", text = "Color:")
                    col2.prop(props, "bloom_intensity", text = "Intensity:")
                    col2.prop(props, "bloom_clamp", text = "Clamp:")

                col0.prop(scene, "depthoffield", text = "DOF", toggle = True)
                if (scene.depthoffield == True):
                    col1 = box.column()
                    col1.prop(props, "bokeh_max_size", text = "Max Size:")
                    col1.prop(props, "bokeh_threshold", text = "Sprite Threshold:")
                    col1.prop(props, "bokeh_neighbor_max", text = "Neighbor Rejection:")
                    col1.prop(props, "bokeh_denoise_fac", text = "Denoise Amount:")
                    col1.prop(props, "use_bokeh_high_quality_slight_defocus", text = "High Quality Slight Defocus")
                    col1.prop(props, "use_bokeh_jittered", text = "Jitter Camera")
                    if (props.use_bokeh_jittered == True):
                        col1.prop(props, "bokeh_overblur", text = "Over-blur")

                col0.prop(scene, "subsurfscat", text = "SSS", toggle=True)
                if (scene.subsurfscat == True):
                    col1 = box.column()
                    col1.prop(props, "sss_samples", text = "Samples:")
                    col1.prop(props, "sss_jitter_threshold", text = "Jitter Threshold:")

                col0.prop(scene, "use_screen_space_reflections", text = "Screen Space Reflections", toggle=True)
                if (scene.use_screen_space_reflections == True):
                    col1 = box.column()
                    col1.prop(props, "use_ssr", text="Use Screen Space Reflections")
                    col2 = box.column()
                    col2.active = props.use_ssr
                    col2.prop(props, "use_ssr_refraction", text="Refraction")
                    col2.prop(props, "use_ssr_halfres", text = "Half Res Trace")
                    col2.prop(props, "ssr_quality", text = "Trace Precision:")
                    col2.prop(props, "ssr_max_roughness", text = "Max Roughness:")
                    col2.prop(props, "ssr_thickness", text = "Thickness:")
                    col2.prop(props, "ssr_border_fade", text = "Edge Fading:")
                    col2.prop(props, "ssr_firefly_fac", text = "Clamp:")

                col0.prop(scene, "riuse_motion_blur", text = "Motion Blur", toggle = True)
                if (scene.riuse_motion_blur == True):
                    col1 = box.column()
                    col1.prop(props, "use_motion_blur", text="Use Motion Blur")
                    col2 = box.column()
                    col2.active = props.use_motion_blur
                    col2.prop(props, "motion_blur_position", text="Position")
                    col2.prop(props, "motion_blur_shutter", text = "Shutter:")
                    col2.separator()
                    col2.prop(props, "motion_blur_depth_scale", text = "Background Separation:")
                    col2.prop(props, "motion_blur_max", text = "Max Blur:")
                    col2.prop(props, "motion_blur_steps", text="Steps:")

                col0.prop(scene, "rivolumetrics", text = "Volumetrics", toggle = True)
                if (scene.rivolumetrics == True):
                    col1 = box.column()
                    col1.prop(props, "volumetric_start", text = "Start:")
                    col1.prop(props, "volumetric_end", text = "End:")
                    col1.prop(props, "volumetric_tile_size", text = "Tile Size")
                    col1.prop(props, "volumetric_samples", text = "Samples:")
                    col1.prop(props, "volumetric_sample_distribution", text="Distribution")

                    col1.prop(scene, "volumetric_lighting", text = "Volumetric Lighting", toggle = True)
                    if (scene.volumetric_lighting == True):

                        col1.prop(props, "volumetric_light_clamp", text="Light Clamping")

                    col1.prop(scene, "volumetric_shadows", text = "Volumetric Shadows", toggle = True)
                    if (scene.volumetric_shadows == True):
                        col1.prop(props, "volumetric_shadow_samples", text="Samples")

                col0.prop(scene, "ricurves", text = "Curves", toggle=True)
                if (scene.ricurves == True):
                    col1 = box.column()
                    col1.prop(rd, "hair_type", text="Shape", expand=True)
                    col1.prop(rd, "hair_subdiv")

                col0.prop(scene, "rishadows", text = "Shadows", toggle=True)
                if (scene.rishadows == True):
                    col1 = box.column()
                    col1.prop(props, "shadow_cube_size", text="Cube Size")
                    col1.prop(props, "shadow_cascade_size", text="Cascade Size")
                    col1.prop(props, "use_shadow_high_bitdepth", text = "High Bit Depth")
                    col1.prop(props, "use_soft_shadows", text = "Soft Shadows")
                    col1.prop(props, "light_threshold", text = "Light Threshold:")


        #performance
        colmain.prop(scene, "performance", text = "Performance", toggle = True, icon_value = kbicons["kiperformance"].icon_id)
        if (scene.performance == True):
            if rEngine == 'CYCLES':
                #threads
                box = layout.box()
                col = box.column(align=True)
                col.prop(scene, "myThreads", text = "Threads")
                if (scene.myThreads == True):
                    col.label(text = "THREADS")
                    col.prop(rd, "threads_mode")
                    sub = box.column(align=True)
                    sub.enabled = rd.threads_mode == 'FIXED'
                    sub.prop(rd, "threads")
                #memory
                col.prop(scene, "myMemory", text = "Memory")
                if (scene.myMemory == True):
                    layout.use_property_split = True
                    col = box.column()
                    col.prop(cscene, "use_auto_tile")
                    sub = box.column()
                    sub.active = cscene.use_auto_tile
                    sub.prop(cscene, "tile_size")
                    layout.use_property_split = False

                #acceleration structure
                col = box.column()
                col.prop(scene, "AccelStruct", text = "Acceleration Structure")
                if (scene.AccelStruct == True):
                    layout.use_property_split = True
                    col = box.column()
                    use_embree = _cycles.with_embree
                    if bpy.context.scene.cycles.device == 'CPU':
                        if not use_embree:
                            sub = box.column(align=True)
                            sub.label(text="Cycles built without Embree support")
                            sub.label(text="CPU raytracing performance will be poor")

                    col.prop(cscene, "debug_use_spatial_splits")
                    if bpy.context.scene.cycles.device == 'GPU':
                        col = box.column()
                        col.prop(cscene, "debug_use_hair_bvh")
                        col.prop(cscene, "debug_bvh_time_steps")
                    layout.use_property_split = False

                #final render
                col = box.column()
                col.prop(scene, "myFinalRender", text = "Final Render")
                if (scene.myFinalRender == True):
                    layout.use_property_split = True
                    col = box.column()
                    col.prop(rd, "use_persistent_data", text="Persistent Data")
                    layout.use_property_split = False

                #viewport
                col = box.column()
                col.prop(scene, "myViewPort", text = "Viewport")
                if (scene.myViewPort == True):
                    layout.use_property_split = True
                    col = box.column()
                    col.prop(rd, "preview_pixel_size", text="Pixel Size")
                    layout.use_property_split = False
            elif rEngine == 'BLENDER_EEVEE':
                box = layout.box()
                col = box.column()
                col.prop(rd, "use_high_quality_normals", toggle = True)


class kbviewlayers(View3DPanel, bpy.types.Panel):
    bl_idname = "KB_PT_kbviewlayers_panel"
    bl_label = "Render Passes"

    def draw(self, context):
        layout = self.layout
        obj = bpy.context.object
        scene = bpy.context.scene
        view_layer = context.view_layer
        view_layer_eevee = view_layer.eevee
        rd = context.scene.render
        cycles_view_layer = view_layer.cycles

        kbicons = icons_load.kilelit_icons

        if has_geometry_visibility(obj):
            colPass = layout.column_flow(columns=3, align = True)
            colPass.scale_y = 1.25
            colPass.prop(scene, "passData", text = "Data", toggle = True, icon_value = kbicons["kidata"].icon_id)
            colPass.prop(scene, "passLight", text = "Light", toggle = True, icon_value=kbicons["kilight"].icon_id)
            if scene.render.engine == 'CYCLES':
                colPass.prop(scene, "passCryptoMatte", text = "Cryptomatte", toggle = True, icon_value=kbicons["kicryptomatte"].icon_id)

            elif scene.render.engine == "BLENDER_EEVEE":
                colPass.prop(scene, "passCryptoMatte", text = "Effects", toggle = True)

            #Data Passes
            if (scene.passData == True):
                box = layout.box()
                coldat = box.column_flow(align=True)
                coldat.label(text = "Included")
                col = box.column_flow(columns=2, align=True)
                col.prop(view_layer, "use_pass_combined", toggle = True)
                col.prop(view_layer, "use_pass_z", toggle = True)
                col.prop(view_layer, "use_pass_mist", toggle = True)
                col.prop(view_layer, "use_pass_normal", toggle = True)
                if scene.render.engine == "CYCLES":
                    col.active = not rd.use_motion_blur
                    col.prop(view_layer, "use_pass_vector", toggle = True)
                    col.prop(view_layer, "use_pass_uv", toggle = True)

                    col.prop(cycles_view_layer, "denoising_store_passes", text="Denoising Data", toggle = True)
                if scene.render.engine == 'CYCLES':
                    coldat = box.column_flow(align=True)
                    coldat.label(text = "Indexes")
                    col = box.column_flow(columns=2, align=True)
                    col.prop(view_layer, "use_pass_object_index", toggle = True)
                    col.prop(view_layer, "use_pass_material_index", toggle = True)

                    coldat = box.column_flow(align=True)
                    coldat.label(text = "Debug")
                    col = box.column_flow(columns=1, align=True)
                    col.prop(cycles_view_layer, "pass_debug_sample_count", text="Sample Count", toggle = False)

                    box.prop(view_layer, "pass_alpha_threshold")

            #Light Passes
            if (scene.passLight == True):
                box = layout.box()
                collit = box.column_flow(align=True)
                collit.label(text = "Diffuse")

                col = box.column_flow(columns=3, align=True)
                col.prop(view_layer, "use_pass_diffuse_direct", text="Direct", toggle = True)
                if scene.render.engine == "CYCLES":
                    col.prop(view_layer, "use_pass_diffuse_indirect", text="Indirect", toggle = True)
                col.prop(view_layer, "use_pass_diffuse_color", text="Color", toggle = True)

                collit = box.column_flow(align=True)
                if scene.render.engine == "CYCLES":
                    collit.label(text = "Glossy")
                if scene.render.engine == "BLENDER_EEVEE":
                    collit.label(text = "Specular")

                col = box.column_flow(columns=3, align=True)
                col.prop(view_layer, "use_pass_glossy_direct", text="Direct", toggle = True)
                if scene.render.engine == "CYCLES":
                    col.prop(view_layer, "use_pass_glossy_indirect", text="Indirect", toggle = True)
                col.prop(view_layer, "use_pass_glossy_color", text="Color", toggle = True)

                if scene.render.engine == "CYCLES":
                    collit = box.column_flow(align=True)
                    collit.label(text = "Transmission")
                    col = box.column_flow(columns=3, align=True)
                    col.prop(view_layer, "use_pass_transmission_direct", text="Direct", toggle = True)
                    col.prop(view_layer, "use_pass_transmission_indirect", text="Indirect", toggle = True)
                    col.prop(view_layer, "use_pass_transmission_color", text="Color", toggle = True)


                collit = box.column_flow(align=True)
                collit.label(text = "Volume")
                col = box.column_flow(columns=2, align=True)
                if scene.render.engine == "CYCLES":
                    col.prop(cycles_view_layer, "use_pass_volume_direct", text="Direct", toggle = True)
                    col.prop(cycles_view_layer, "use_pass_volume_indirect", text="Indirect", toggle = True)
                elif scene.render.engine == "BLENDER_EEVEE":
                    col.prop(scene, "eeveePassVolTrans", text = "Transmittance", toggle = True)
                    col.prop(scene, "eeveePassVolScat", text = "Scatter", toggle=True)

                collit = box.column_flow(align=True)
                collit.label(text = "Other")

                col = box.column_flow(columns=2, align=True)
                col.prop(view_layer, "use_pass_emit", text="Emission", toggle = True)
                col.prop(view_layer, "use_pass_environment", toggle = True)
                col.prop(view_layer, "use_pass_shadow", toggle = True)
                col.prop(view_layer, "use_pass_ambient_occlusion", text="Ambient Occlusion", toggle = True)

            #Cryptomatte passes
            if (scene.passCryptoMatte == True):
                box = layout.box()
                col = box.column()
                col.label(text = "Cryptomatte")
                col.prop(view_layer, "use_pass_cryptomatte_object", text="Object", toggle = True)
                col.prop(view_layer, "use_pass_cryptomatte_material", text="Material", toggle = True)
                col.prop(view_layer, "use_pass_cryptomatte_asset", text="Asset", toggle = True)
                col = box.column()
                col.active = any((view_layer.use_pass_cryptomatte_object,
                                  view_layer.use_pass_cryptomatte_material,
                                  view_layer.use_pass_cryptomatte_asset))
                col.prop(view_layer, "pass_cryptomatte_depth", text="Levels")
                col.prop(view_layer, "use_pass_cryptomatte_accurate",
                         text="Accurate Mode", toggle = True)

                if scene.render.engine == "BLENDER_EEVEE":
                    col = box.column_flow(align=True)
                    col.label(text = "Eevee Bloom Effect:")
                    col.prop(scene, "bloomEffect", text = "Bloom", toggle = True)
                    col.prop(view_layer_eevee, "use_pass_transparent", text = "Transparent", toggle = True)

                    col.separator()

class kbmtloverride(View3DPanel, bpy.types.Panel):
    bl_idname = "KB_PT_kbmtloverride_panel"
    bl_label = "Material Override"

    def draw(self, context):
        layout = self.layout
        obj = bpy.context.object
        scene = bpy.context.scene
        view_layer = context.view_layer
        mat = bpy.data.materials

        kbicons = icons_load.kilelit_icons
        #material override
        if has_geometry_visibility(obj):
            if scene.render.engine == 'CYCLES':
                colMTL = layout.column_flow(columns=1, align=True)
                colMTL.scale_y = 1.25
                colMTL.prop(scene, "mtlOverride", text = "Material Override", toggle = True, icon_value = kbicons["kimtloverride"].icon_id)

                if (scene.mtlOverride == True):
                    claymtl = "Clay Render MTL" not in bpy.data.materials
                    box = layout.box()
                    col = box.column_flow(columns=2, align=True)
                    if claymtl == False:
                        col.prop(scene, "mtlOverrideOn", text = "", toggle = True, icon_value=kbicons["kiclayon"].icon_id)
                        col.prop(scene, "mtlOverrideOff", text = "", toggle = True, icon_value=kbicons["kiclayoff"].icon_id)

                        col = layout.column_flow(columns=1, align=True)

                    elif claymtl:
                        col = box.column_flow(columns=1, align=True)
                        col.alert = True
                        col.operator("myct.createclayrendermat", text = "Create Clay Render MTL")
                    col = box.column()
                    col.prop(view_layer, "material_override")
                    col.prop(view_layer, "samples")
                    col.separator()
            else:
                msg = layout.column()
                msg.label(text = ">CYCLES ONLY<")

class kbvisibility(View3DPanel, bpy.types.Panel):
    bl_idname = "KB_PT_kbvisibility_panel"
    bl_label = "Render Visibility"

    def draw(self, context):
        layout = self.layout
        obj = bpy.context.object
        scene = bpy.context.scene
        rEngine = scene.render.engine
        #visibility
        if has_geometry_visibility(obj):
            cob = obj.cycles
            sel = len(bpy.context.selected_objects)
            objSel = range(sel)

            if sel > 0:
                box = layout.box()
                colVis = box.column_flow(columns = 1, align = True)
                colVis.label(text = "Selected object: " + obj.name)
                colVis.prop(scene, "visRenders", text = "Show in Renders", toggle = True)

                if rEngine == 'CYCLES':
                    if sel > 1:
                        colVis.prop(scene, "visShadCatch", text = "Shadow Catcher", toggle = True)
                    elif sel < 2:
                        colVis.prop(obj, "is_shadow_catcher", text = "Shadow Catcher", toggle = True)

                if rEngine == 'CYCLES' or rEngine == 'BLENDER_EEVEE':
                    if sel > 1:
                        colVis.prop(scene, "visHold", text = "Holdout", toggle = True)
                    elif sel < 2:
                        colVis.prop(obj, "is_holdout", text = "Holdout", toggle = True)

                colRVis = box.column_flow(columns = 1, align = True)
                if rEngine != 'CYCLES':
                    colRVis.prop(scene, "rayVisibility", text = "Cycles Visibility", toggle = True)
                    if scene.rayVisibility == True:
                        colRVis.label(text = "> CYCLES ONLY <")

                #Ray Visibility
                elif rEngine == 'CYCLES':
                    colRay = box.column_flow(columns = 2, align = True)
                    if sel > 1:
                        colRay.prop(scene, "rVisCamera", text = "Camera", toggle = True)
                    elif sel < 2:
                        colRay.prop(obj, "visible_camera", text = "Camera", toggle = True)
                    if sel > 1:
                        colRay.prop(scene, "rVisGlos", text = "Glossy",toggle = True)
                    elif sel < 2:
                        colRay.prop(obj, "visible_glossy", text = "Glossy",toggle = True)
                    if sel > 1:
                        colRay.prop(scene, "rVisVol", text = "Volume Scatter", toggle = True)
                    elif sel < 2:
                        colRay.prop(obj, "visible_volume_scatter", text = "Volume Scatter", toggle = True)

                    if sel > 1:
                        colRay.prop(scene, "rVisDif", text = "Diffuse", toggle = True)
                    elif sel < 2:
                        colRay.prop(obj, "visible_diffuse", text = "Diffuse", toggle = True)

                    if sel > 1:
                        colRay.prop(scene, "rVisTran", text = "Transmission",toggle = True)
                    elif sel < 2:
                        colRay.prop(obj, "visible_transmission", text = "Transmission",toggle = True)

                    if obj.type != 'LIGHT':
                        if sel > 1:
                            colRay.prop(scene, "rVisShad", text = "Shadow", toggle = True)
                        elif sel < 2:
                            colRay.prop(obj, "visible_shadow", text = "Shadow", toggle = True)

                    if obj.type != 'LIGHT':
                        msg = box.column()
                        msg.label(text = "Culling")
                        btn = box.column_flow(columns=2, align=True)
                        btn.prop(cob, "use_camera_cull", toggle = True)
                        btn.prop(cob, "use_distance_cull", toggle = True)
                else:
                    box = layout.box()
                    col = box.column()
                    col.label(text = "No object selected")

class kbrenderoutput(View3DPanel, bpy.types.Panel):
    bl_idname = "KB_PT_kbrenderoutput_panel"
    bl_label = "Render Output"

    def draw(self, context):
        layout = self.layout
        obj = bpy.context.object
        scene = bpy.context.scene
        rd = context.scene.render
        image_settings = rd.image_settings
        ffmpeg = rd.ffmpeg

        layout.use_property_split = False

        row = layout.row()
        row.alignment = 'CENTER'
        row.scale_y = 0.5
        if (scene.renderAnim == False):
            row.label(text = "Rendering Still")
        else:
            row.label(text = "Rendering Animation")
        title = layout.column()
        title.label(text = "Resolution:")
        col = layout.column_flow(columns=1, align = True)
        col.prop(scene, "dimpresets", text = "Dimension Presets", toggle = True)
        if (scene.dimpresets == True):
            box = layout.box()
            head = box.column()
            head.label(text = "Still:")
            pre = box.column_flow(columns=3, align = True)
            pre.operator("myct.onekrenderimg", text = "1024")
            pre.operator("myct.twokrenderimg", text = "2048")
            pre.operator("myct.fourkrenderimg", text = "4096")
            title = box.column()
            title.label(text = "Animation")
            pre = box.column_flow(columns = 2, align = True)
            pre.operator("myct.standardanimvid", text = "1920x1080")
            pre.operator("myct.highresanimvid", text = "3840x2160")


        col4 = layout.column_flow(columns = 1, align = True)
        col4.prop(rd, "resolution_x", text = "Res X")
        col4.prop(rd, "resolution_y", text = "Res Y")
        col4.prop(rd, "resolution_percentage", text="Res %")
        col4.separator()
        if (scene.renderAnim == True):
            col4.label(text = "Animation frames:")
            col4.prop(scene, "frame_start", text = "Start")
            col4.prop(scene, "frame_end", text = "End")
            col4.prop(scene, "frame_step", text = "Step")
            col4.separator()
        col4.separator()
        box = layout.box()
        col4 = box.column()
        col4.prop(rd, "filepath", text = "File Path")
        col4.template_image_settings(image_settings, color_management=False)
        vid = ['FFMPEG','AVI_RAW','AVI_JPEG']
        sf = scene.render.image_settings.file_format
        if sf == vid[0] or sf == vid[1] or sf == vid[2]:
            col4.label(text = "Encoding")
            col4.prop(rd.ffmpeg, "format")
            col4.prop(ffmpeg, "use_autosplit")
            col4.label(text = "Video")

            needs_codec = ffmpeg.format in {'AVI', 'QUICKTIME', 'MKV', 'OGG', 'MPEG4', 'WEBM'}
            if needs_codec:
                col4.prop(ffmpeg, "codec")

            if needs_codec and ffmpeg.codec == 'NONE':
                return

            if ffmpeg.codec == 'DNXHD':
                col4.prop(ffmpeg, "use_lossless_output")

            # Output quality
            use_crf = needs_codec and ffmpeg.codec in {'H264', 'MPEG4', 'WEBM'}
            if use_crf:
                col4.prop(ffmpeg, "constant_rate_factor")

            # Encoding speed
            col4.prop(ffmpeg, "ffmpeg_preset")



        col4.prop(rd, "use_overwrite")
        col4.prop(rd, "use_placeholder")
        col4.prop(rd, "use_file_extension")
        col4.prop(rd, "use_render_cache")
        self.layout.separator()
        colCC = box.column_flow(columns = 1)
        if (scene.colorManage == True):
            colCC.prop(scene, "colorManage", toggle = True, text = "Close Color Management")
        else:
            colCC.prop(scene, "colorManage", toggle = True, text = "Open Color Management")
        col5 = box.column_flow(columns = 2, align = True)
        scene = context.scene
        view = scene.view_settings
        if (scene.colorManage == True):
            col5.prop(scene.display_settings, "display_device")

            col5.separator()

            col5.prop(view, "view_transform")
            col5.prop(view, "look")

            col5.prop(view, "exposure")
            col5.prop(view, "gamma")

            col5.separator()

            col5.prop(scene.sequencer_colorspace_settings, "name", text="Sequencer")
            col6 = box.column_flow(columns = 1, align = True)
            col6.prop(view, "use_curve_mapping", toggle = True, text="Use Curves")
            if (view.use_curve_mapping == True):
                col6.use_property_split = False
                col6.use_property_decorate = False  # No animation.

                col6.template_curve_mapping(view, "curve_mapping", type='COLOR', levels=True)

class kbkilelitinfo(View3DPanel, bpy.types.Panel):
    bl_idname = "KB_PT_kbkilelitinfo_panel"
    bl_label = "Kilelit Info"

    def draw(self, context):
        layout = self.layout
        scene = bpy.context.scene
        object = bpy.context.object

        kbicons = icons_load.kilelit_icons
        box = layout.box()
        row = box.row(align=True)
        row.alignment = 'CENTER'
        row.scale_y = 0.5
        row.label(text = "Addon: Kilelit")
        row = box.row(align=True)
        row.alignment = 'CENTER'
        row.scale_y = 0.5
        row.label(text = "Author: Kenray Barnabas")
        row = box.row(align=True)
        row.alignment = 'CENTER'
        row.scale_y = 0.5
        row.label(text = "Version: 1.5")

        col = box.column()
        col.separator()
        col = box.column_flow(columns=2, align=True)
        col.scale_y = 1.25
        col.operator("myct.kbspaceportals", text = "KB Space Portals", icon_value=kbicons["kikbspacelogo"].icon_id)
        col.operator("myct.kbportfolio", text = "3D Portfolio", icon_value=kbicons["kikblogo"].icon_id)

classes = [kbkilelit, kbrenderperformance, kbviewlayers, kbmtloverride, kbvisibility, kbrenderoutput, kbkilelitinfo]

def renderhistoryprev():
    try:
        bpy.types.Scene.render_history_previews = bpy.props.EnumProperty(items = renderhistory.init_images(True, True), name="Render History", description="Kilelit previews", default= "_rendersomething", update = get_images)

        bpy.app.timers.unregister(renderhistoryprev)
    except:
        pass


def register():
    #class register
    for c in classes:
        bpy.utils.register_class(c)

    #import icons
    icons_load.Kilelit_Icons()

    pt = bpy.types.Scene
    #dimension presets
    pt.dimpresets = BoolProperty(default = False)

    pt.renderpostnotify = BoolProperty(default = False, description="Notify after render is complete.")
    #Rendering
    pt.renderHoldouts = BoolProperty(description = "Render selected. Unselected objects will be masked out.", default = False, update = holdout)
    pt.renderCamVisible = BoolProperty(description = "Render selected. Unselected objects will be invisible to camera.", default = True, update = invisible)
    pt.renderAnim = BoolProperty(description = "Render animation frames/selection only animation frames.", default = False)
    pt.renderselected = BoolProperty(description = "Render selected object only.", default = False, update = renderselonly)
    pt.rendershadowcatcher = BoolProperty(default = False, update = isshadowcatcher)


    #string
    pt.selectonlyobjname = StringProperty(name= "Selected Only Object")

    pt.screenCaps = BoolProperty(description = "capture viewport.", default = False, update = renderviewport)
    pt.fTransparent = BoolProperty(description = "Render with transparent background.", default = False, update = renderTransparency)
    pt.transparentGlass = BoolProperty(description = "Render transmissive surfaces as transparent for comping glass over another background.", default = False, update = rendertransparentGlass)
    pt.objProps = BoolProperty(description = "Render visibility", default = False)


    #visibility
    pt.visHold = BoolProperty(default = False, update = viewPortHold)
    pt.visRenders = BoolProperty(default = True, update = viewPortRender)
    pt.visShadCatch = BoolProperty(default = False, update = visShadowCatcher)


    #Ray visibility
    pt.rayVisibility = BoolProperty(default = True)
    pt.rVisCamera = BoolProperty(default = True, update = rayCamera)
    pt.rVisDif = BoolProperty(default = True, update = rayDiffuse)
    pt.rVisGlos = BoolProperty(default = True, update = rayGlossy)
    pt.rVisTran = BoolProperty(default = True, update = rayTransmission)
    pt.rVisVol = BoolProperty(default = True, update = rayVolume)
    pt.rVisShad = BoolProperty(default = True, update = rayShadow)

    #rendersettings
    pt.performance = BoolProperty(default = False, update = renderperf)
    pt.renderSamples = BoolProperty(default = False, update = rendersamp)

    pt.samplesVP = BoolProperty(default = False, update = rendersamplingVP)
    pt.samplesVPDenoise = BoolProperty(default = True, update = useviewportdenoise)
    pt.samplesRender = BoolProperty(default = True, update = rendersampling)
    pt.samplesRenderDenoise = BoolProperty(default = False, update = userenderdenoise)

    #eevee render settings
    pt.use_AmbOcc = BoolProperty(default = False, description = "Use Ambient Occlusion.", update = use_ao)
    pt.useBloom = BoolProperty(default = False, description = "Use Bloom.", update = use_bloom)
    pt.use_screen_space_reflections = BoolProperty(default = False, description="Use Screen Space Reflections.", update = use_ssr)
    pt.riuse_motion_blur = BoolProperty(default = False, description = "Use motion blur.", update = use_Moblur)
    pt.volumetric_lighting = BoolProperty(default = False, description = "Enable scene light interactions with volumetrics.", update = use_vol_light)
    pt.volumetric_shadows = BoolProperty(default = False, description = "Generate shadows from volumetric materials(Very expensive).", update = use_vol_shadows)
    pt.depthoffield = BoolProperty(default = False, description = "Define depth of field properties.", update = use_dof)
    pt.subsurfscat = BoolProperty(default = False, description = "Define subsurface scattering properties.", update = use_sss)
    pt.rivolumetrics = BoolProperty(default = False, description = "Volumetric settings.", update = use_vol)
    pt.ricurves = BoolProperty(default = False, description = "Hair curve object display properties.", update = use_curves)
    pt.rishadows = BoolProperty(default = False, description = "Eevee shadow parameters.", update = use_shadows)


    #performance
    pt.myThreads = BoolProperty(default = True)
    pt.myMemory = BoolProperty(default = True)
    pt.AccelStruct = BoolProperty(default = True)
    pt.myFinalRender = BoolProperty(default = True)
    pt.myViewPort = BoolProperty(default = True)
    pt.lightpaths = BoolProperty(default = False)
    pt.lights = BoolProperty(default = False)
    #renderoutput
    pt.renderOutput = BoolProperty(default = False)

    #color management
    pt.colorManage = BoolProperty(default = False)

    #Bool
    pt.subsampleGlobal = IntProperty(default = 8, min = 1, description = "Globally update sub samples.",update = global_subSample)
    pt.RenderDenoise = BoolProperty(default = False)
    pt.advanced = BoolProperty(default = False)
    pt.denoiserPasses = BoolProperty(default = False)
    pt.mtlOverride = BoolProperty(default = False)
    pt.eeveePassVolTrans = BoolProperty(default = False, update = EeveePassVolumeTransmittance)
    pt.eeveePassVolScat = BoolProperty(default = False, update = EeveePassVolumeScatter)
    pt.bloomEffect = BoolProperty(default = False, update = EeveeBloomEffect)

    pt.mtlOverrideOn = BoolProperty(default = True, update = ClayOn)
    pt.mtlOverrideOff = BoolProperty(default = False, update = ClayOff)

    pt.renderLockUI = BoolProperty(default = False, update = RenderLockInterface)

    pt.postProcess = BoolProperty(default = False)
    pt.aoSettings = BoolProperty(default= False)
    pt.bloomSettings = BoolProperty(default= False)
    pt.ssrSettings = BoolProperty(default= False)
    pt.motionblurSettings = BoolProperty(default= False)

    #RenderPasses
    pt.renderPasses = BoolProperty(default = False)
    pt.passData = BoolProperty(default = False, update = passdat)
    pt.passLight = BoolProperty(default = False, update = passlit)
    pt.passCryptoMatte = BoolProperty(default = False, update = passcryptmat)

    #renders previews
    pt.generate_previews = BoolProperty(default = False, description = "Generate render history previews.")
    pt.lock_renderhistory_path = BoolProperty(default = False, description = "Use alternate path.")
    pt.render_history_path = StringProperty(name = "Path", description = "Kilelit History alternate path.", subtype = "DIR_PATH", update = historypathset)

    #load thumbnails
    renderhistory.init_images(True, True)

    bpy.app.timers.register(renderhistoryprev, first_interval=0.0001)


def unregister():
    pt = bpy.types.Scene
    #class unregister
    for c in classes:
        bpy.utils.unregister_class(c)
    try:
        del pt.renderpostnotify

        del pt.dimpresets

        del pt.renderHoldouts
        del pt.renderCamVisible
        del pt.renderAnim
        del pt.renderselected
        del pt.rendershadowcatcher

        del pt.screenCaps

        del pt.objProps


        #visibilityd
        del pt.visHold
        del pt.visRenders
        del pt.visShadCatch

        #Ray Visibility
        del pt.rayVisibility
        del pt.rVisCamera
        del pt.rVisDif
        del pt.rVisGlos
        del pt.rVisTran
        del pt.rVisVol
        del pt.rVisShad

        #rendersettings
        del pt.performance
        del pt.renderSamples
        del pt.samplesVP
        del pt.samplesVPDenoise
        del pt.samplesRenderDenoise
        del pt.samplesDenoise

        #eevee render settings
        del pt.use_AmbOcc
        del pt.useBloom
        del pt.use_screen_space_reflections
        del pt.riuse_motion_blur
        del pt.volumetric_lighting
        del pt.volumetric_shadows
        del pt.depthoffield
        del pt.subsurfscat
        del pt.rivolumetrics
        del pt.ricurves
        del pt.rishadows



        #performance
        del pt.myThreads
        del pt.myMemory
        del pt.AccelStruct
        del pt.myFinalRender
        del pt.myViewPort
        del pt.lightpaths
        del pt.lights
        #render output
        del pt.renderOutput

        #color management
        del pt.colorManage
        #Bool
        del pt.subsampleGlobal
        del pt.advancedDenoise
        del pt.denoiserPasses
        del pt.mtlOverride
        del pt.mtlOverrideOn
        del pt.mtlOverrideOff

        del pt.postProcess
        del pt.aoSettings
        del pt.bloomSettings
        del pt.ssrSettings
        del pt.motionblurSettings


        #render passes
        del pt.eeveePassVolTrans
        del pt.renderPasses
        del pt.passData
        del pt.passLight
        del pt.passCryptoMatte

        #render previews
        del pt.generate_previews
        del pt.render_history_previews

        del pt.render_history_path
        del pt.use_alt_path
    except:
        pass


if __name__ == "__main__":
    register()
