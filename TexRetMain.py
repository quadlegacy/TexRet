bl_info = {
    "name": "Texture Retriever",
    "author": "Quaddy9779",
    "version": (1, 0),
    "blender": (2, 77, 0),
    "location": "View3D > Tool Shelf > TexRet",
    "description": "Copies all your textures and paste it to a target Directory",
    "warning": "",
    "wiki_url": "",
    "category": "Copy Texture",
    }

import bpy_extras
import os
import shutil
import os.path
import bpy
from bpy.props import (StringProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )

#-----------
#	DEF
#-----------

def main(context):
    #body
    scn = context.scene
    filepath = bpy.data.filepath
    directory = filepath
    targetdir = scn.my_tool.path
    
    a = -1
    os.system("cls")    
    if not os.path.isdir(targetdir):
        b = targetdir.split("..")
        if ".." in targetdir:
            for x in b:
                a += 1
                directory = os.path.dirname(directory)
            targetdir = targetdir.replace("//..", "")
            targetdir = targetdir.replace("\..", "")
                                    
        elif "//" in targetdir:
            directory = os.path.dirname(directory)
            targetdir = targetdir.replace("//", "\\")
    
    print("Copying files.... \n")
    for ob in bpy.data.objects:
        for mat_slot in ob.material_slots:
            for mtex_slot in mat_slot.material.texture_slots:
                if mtex_slot:
                    if hasattr(mtex_slot.texture , 'image'):
                        if(mtex_slot.texture is not None):
                            CurImage = mtex_slot.texture.image.filepath
                            directory = filepath
                            a = -1
                            b = CurImage.split("..")
                            if ".." in CurImage:
                                for x in b:
                                    a += 1
                                    directory = os.path.dirname(directory)
                                CurImage = CurImage.replace("//..", "")
                                CurImage = CurImage.replace("\..", "")
                                
                            elif "//" in CurImage:
                                directory = os.path.dirname(directory)
                                CurImage = CurImage.replace("//", "\\")
                                
                            if os.path.isfile(directory + CurImage):
                                print(directory + CurImage)
                                shutil.copy(directory + CurImage, targetdir)
                                
                            elif os.path.isfile(CurImage):
                                print(CurImage)
                                shutil.copy(CurImage, targetdir)
                                
    list = os.listdir(targetdir)
    total_files = len(list)
    print("\nTotal files that is in the folder: " + str(total_files - 1) + ". Note: Ignore duplicate ones in the log")
    
    #print(directory + targetdir)
    #print("total is:" + str(a))

# ------------------------------------------------------------------------
#    ui
# ------------------------------------------------------------------------

class MySettings(PropertyGroup):

    path = StringProperty(
        name="",
        description="Path to Directory",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')
    bb = ""

class MainTexRet(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "myops.get_textures"
    bl_label = "Get Texture"


    def execute(self, context):
        bb = self
        scn = context.scene
        targetdir = scn.my_tool.path
        if(targetdir == ""):
            self.report({'ERROR'}, "Please fill up the target directory properly")
            return {'FINISHED'}
        else:
            main(context)
            return {'FINISHED'}
		
class OBJECT_PT_my_panel(Panel):
    bl_idname = "OBJECT_PT_texret"
    bl_label = "TexRet Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "TexRet"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        col = layout.column(align=True)
        col.prop(scn.my_tool, "path", text="Target Location")
        
        row = layout.row()
        row.operator("myops.get_textures")

        # print the path to the console
        #print (scn.my_tool.path)
        #filepath = bpy.data.filepath
        #directory = os.path.dirname(os.path.dirname(filepath))
        #print(directory)

# ------------------------------------------------------------------------
#    register and unregister functions
# ------------------------------------------------------------------------

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.my_tool = PointerProperty(type=MySettings)

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()
