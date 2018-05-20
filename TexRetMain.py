bl_info = {
    "name": "Texture Retriever",
    "author": "Quaddy9779",
    "version": (1, 0),
    "blender": (2, 77, 0),
    "location": "View3D > Tool Shelf > TexRet",
    "description": "Copies all your textures and paste it to a targeted Directory",
    "warning": "",
    "wiki_url": "",
    "category": "Copy Texture",
    }

import bpy
from bpy.props import (StringProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )
import bpy_extras
import os
import shutil
import os.path


def main(context):
    #body
    os.system("cls")
    print("Copying files.... \n")
    for ob in bpy.data.objects:
        for mat_slot in ob.material_slots:
            for mtex_slot in mat_slot.material.texture_slots:
                if mtex_slot:
                    if hasattr(mtex_slot.texture , 'image'):
                        CurImage = mtex_slot.texture.image.filepath
                        if os.path.isfile(CurImage):
                            print(CurImage)
                            shutil.copy(CurImage, targetdir)
                        else:
                            if os.path.isfile(CurImage.replace("//..", mainpath)):
                                print(CurImage.replace("//..", mainpath))
                                shutil.copy(CurImage.replace("//..", mainpath), targetdir)
                                
    list = os.listdir(targetdir)
    total_files = len(list)
    print("\nTotal files that is copied: " + str(total_files - 1) + ". Note: Ignore duplicate ones")

class SelectFile(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "demo.select_file" 
    bl_label = "Select a file"

    filename_ext = ".txt"
    filter_glob = bpy.props.StringProperty(default='*.txt', options={'HIDDEN'}, maxlen=255)

    def execute(self, context):
        print(self.filepath)
        return {'FINISHED'}

class MainTexRet(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "myops.get_textures"
    bl_label = "Get Texture"


    def execute(self, context):
        SelectFile(bpy.types.Operator, bpy_extras.io_utils.ExportHelper)
        main(context)
        return {'FINISHED'}

class TexRetPanel(bpy.types.Panel):
    """Creates a Panel in the Tool Shelf"""
    bl_label = "TexRet Panel"
    bl_idname = "OBJECT_PT_texret"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "TexRet"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("myops.get_textures")

def register():
    bpy.utils.register_class(MainTexRet)
    bpy.utils.register_class(TexRetPanel)

def unregister():
    bpy.utils.unregister_class(MainTexRet)
    bpy.utils.unregister_class(TexRetPanel)

if __name__ == "__main__":
    register()

    # test call
    # bpy.ops.myops.get_textures()--