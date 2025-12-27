import bpy
import os
import subprocess


from bpy.types import *
from Kilelit import utils
from Kilelit.utils import kilelit_functions, openwebpages

def gv():
    gv.rf = kilelit_functions
    gv.web = openwebpages

def MyRender(self, myrender):
    gv()
    gv.rf.MyRender(self, myrender)

def openNetWorkHost(self, nethost):
    gv()
    gv.rf.openNetWorkHost(self, nethost)

def ShowRender(showrender):
    gv()
    gv.rf.ShowRender(showrender)

def ClearSelSets(clearselsets):
    gv()
    gv.rf.ClearSelSets(clearselsets)

def ClayRenderMTL(clayrendermtl):
    gv()
    gv.rf.ClayRenderMTL(clayrendermtl)

def onekrenderstill(onekstill):
    gv()
    gv.rf.onekrenderstill(onekstill)

def twokrenderstill(twokstill):
    gv()
    gv.rf.twokrenderstill(twokstill)

def fourkrenderstill(fourkstill):
    gv()
    gv.rf.fourkrenderstill(fourkstill)

def standardanimrender(standardanim):
    gv()
    gv.rf.standardanimrender(standardanim)

def highresanimrender(highresanim):
    gv()
    gv.rf.highresanimrender(highresanim)

def clear_render_history(clearrenderhistory):
    gv()
    gv.rf.clear_render_history(clearrenderhistory)

def openkbspaceportals():
    gv()
    gv.web.openkbspaceportals()

def openkbportfolio():
    gv()
    gv.web.openkbportfolio()

def openyoutube():
    gv()
    gv.web.openyoutube()



class renderbutton(bpy.types.Operator):
    bl_idname = "myct.renderbutton"
    bl_label = "Render image or animation"
    bl_description = "Render image or animation"

    @classmethod
    def poll(cls, context):
        return(context.object is not None)

    def execute(self, myrender):
        MyRender(self, myrender)
        return{'FINISHED'}


class viewmyrender(bpy.types.Operator):
    bl_idname = "myct.showmyrender"
    bl_label = "View Render"
    bl_description = "Show last render."

    @classmethod
    def poll(cls, context):
        return(context.object is not None)

    def execute(self, showrender):
        ShowRender(showrender)
        return{'FINISHED'}

class clearcustrendersettings(bpy.types.Operator):
    bl_idname = "myct.clearcustrendersettings"
    bl_label = "Clear Custom Settings"
    bl_description = "Clear custom selected only render settings"

    @classmethod
    def poll(cls, context):
        return(context.object is not None)

    def execute(self, clearselsets):
        ClearSelSets(clearselsets)
        return{"FINISHED"}

class createclayrendermat(bpy.types.Operator):
    bl_idname = "myct.createclayrendermat"
    bl_label = "Create Grey Material"
    bl_description = "Create material for override clay render"

    @classmethod
    def poll(cls, context):
        return(context.object is not None)

    def execute(self, clayrendermtl):
        ClayRenderMTL(clayrendermtl)
        return{"FINISHED"}

class onekrenderimg(bpy.types.Operator):
    bl_idname = "myct.onekrenderimg"
    bl_label = "1024"
    bl_description = "set dimensions to 1024x1024"

    @classmethod
    def poll(cls, context):
        return(context.object is not None)

    def execute(self, onekstill):
        onekrenderstill(onekstill)
        return{"FINISHED"}

class twokrenderimg(bpy.types.Operator):
    bl_idname = "myct.twokrenderimg"
    bl_label = "2048"
    bl_description = "set dimensions to 2048x2048"

    @classmethod
    def poll(cls, context):
        return(context.object is not None)

    def execute(self, twokstill):
        twokrenderstill(twokstill)
        return{"FINISHED"}

class fourkrenderimg(bpy.types.Operator):
    bl_idname = "myct.fourkrenderimg"
    bl_label = "4096"
    bl_description = "set dimensions to 4096x4096"

    @classmethod
    def poll(cls, context):
        return(context.object is not None)

    def execute(self, fourkstill):
        fourkrenderstill(fourkstill)
        return{"FINISHED"}

class standardanimvid(bpy.types.Operator):
    bl_idname = "myct.standardanimvid"
    bl_label = "1920x1080"
    bl_description = "set dimensions to 1920x1080"

    @classmethod
    def poll(cls, context):
        return(context.object is not None)

    def execute(self, standardanim):
        standardanimrender(standardanim)
        return{"FINISHED"}

class highresanimvid(bpy.types.Operator):
    bl_idname = "myct.highresanimvid"
    bl_label = "3840x2160"
    bl_description = "set dimensions to 3840x2160"

    @classmethod
    def poll(cls, context):
        return(context.object is not None)

    def execute(self, highresanim):
        highresanimrender(highresanim)
        return{"FINISHED"}


class renderhistoryclear(bpy.types.Operator):
    bl_idname = "myct.clearrenderhistory"
    bl_label = "Clear Render History"
    bl_description = "clear the render history"

    @classmethod
    def poll(cls, context):
        return(context.object is not None)

    def execute(self, clearrenderhistory):
        clear_render_history(clearrenderhistory)
        return{"FINISHED"}
    def invoke(self, context, event):
        #confirmation dialog before executing
        return context.window_manager.invoke_props_dialog(self, width=200)

    def draw(self, context):
        self.layout.label(text = "All renders will be deleted. Continue?")

class OpenExplorerOperator(bpy.types.Operator):
    bl_idname = "myct.open_exploerer"
    bl_label = "Open File Explorer"
    bl_description = "Open OS explorer"


    def execute(self, context):
        try:
            scene = bpy.context.scene
            folder_path = bpy.path.abspath(os.path.join(scene.render_history_path))

            #check if the folder path exists
            if not os.path.exists(folder_path):
                self.report({'WARNING'}, f"Folder path does not exist: {folder_path}")
                return {'CANCELLED'}

            #Open the folder path with windows explorer
            subprocess.Popen(["explorer", '/open,', folder_path])

        except Exception as e:
            self.report({'ERROR'}, str(e))
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class kbspaceportals(bpy.types.Operator):
    bl_idname = "myct.kbspaceportals"
    bl_label = "KB Space Portals"
    bl_description = "KB Space Portals"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        openkbspaceportals()
        return{'FINISHED'}

class kbportfolio(bpy.types.Operator):
    bl_idname = "myct.kbportfolio"
    bl_label = "KB 3D Portfolio"
    bl_description = "KB 3D Portfolio"


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        openkbportfolio()
        return{'FINISHED'}



classes = [renderbutton, viewmyrender, clearcustrendersettings, createclayrendermat, onekrenderimg, twokrenderimg, fourkrenderimg, standardanimvid, highresanimvid, renderhistoryclear, OpenExplorerOperator, kbspaceportals, kbportfolio]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
