bl_info = {
    "name": "Whizibility",
    "author": "Kursad Karatas",
    "version": (0, 2),
    "blender": (3, 0, 0),
    "location": "View3d",
    "description": "Visibility Controls",
    "warning": "",
    "doc_url": "",
    "category": "",
}

from rna_prop_ui import PropertyPanel
from bpy.types import Panel, Menu
from mathutils import Vector
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from bpy.props import FloatVectorProperty
from bpy.types import Operator
import bpy


def has_geometry_visibility(ob):
    return ob and ((ob.type in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'META', 'LIGHT'}) or
                   (ob.instance_type == 'COLLECTION' and ob.instance_collection))


class ObjectButtonsPanel:
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"


class WHIZIBILITY_OT_WhizibilityStuff(Operator):
    """Visibility master panel"""
    bl_idname = "wm.whizibility_stuff"
    bl_label = "whizibility"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        return {'FINISHED'}


class WhizCyclesButtonsPanel:

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    COMPAT_ENGINES = {'CYCLES'}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES


class WHIZIBILITY_PT_Render(Panel):

    bl_idname = "WHIZIBILITY_PT_render"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Render"
    bl_category = "WhizTools"

    @classmethod
    def poll(cls, context):
        return context.object

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        ob = context.object

        layout.prop(ob, "hide_select", text="Selectable",
                    invert_checkbox=True, toggle=False)

        col = layout.column(heading="Show In")
        col.prop(ob, "hide_viewport", text="Viewports",
                 invert_checkbox=True, toggle=False)
        col.prop(ob, "hide_render", text="Renders",
                 invert_checkbox=True, toggle=False)

        if has_geometry_visibility(ob):
            cob = ob.cycles
            col = layout.column(heading="Mask")


class WHIZIBILITY_PT_RenderCycles(WhizCyclesButtonsPanel, Panel):

    bl_idname = "WHIZIBILITY_PT_rendercycles"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Render Cycles"
    bl_category = "WhizTools"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        ob = context.object
        cob = ob.cycles

        col = layout.column()
        col.prop(ob, "visible_camera", text="Camera")
        col.prop(ob, "visible_diffuse", text="Diffuse")
        col.prop(ob, "visible_glossy", text="Glossy")
        col.prop(ob, "visible_transmission", text="Transmission")
        col.prop(ob, "visible_volume_scatter", text="Volume Scatter")

        if ob.type != 'LIGHT':
            sub = col.column()
            sub.prop(ob, "visible_shadow", text="Shadow")


class WHIZIBILITY_PT_Viewport(Panel):
    bl_label = "Visibvility Object"

    bl_order = 10
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Viewport"
    bl_category = "WhizTools"

    @classmethod
    def poll(cls, context):
        return context.object

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        obj = context.object
        obj_type = obj.type
        is_geometry = (obj_type in {
                       'MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'VOLUME', 'HAIR', 'POINTCLOUD'})
        is_wire = (obj_type in {'CAMERA', 'EMPTY'})
        is_empty_image = (
            obj_type == 'EMPTY' and obj.empty_display_type == 'IMAGE')
        is_dupli = (obj.instance_type != 'NONE')
        is_gpencil = (obj_type == 'GPENCIL')

        col = layout.column(heading="Show")
        col.prop(obj, "show_name", text="Name")
        col.prop(obj, "show_axis", text="Axis")

        if is_geometry or is_dupli:
            col.prop(obj, "show_wire", text="Wireframe")
        if obj_type == 'MESH' or is_dupli:
            col.prop(obj, "show_all_edges", text="All Edges")
        if is_geometry:
            col.prop(obj, "show_texture_space", text="Texture Space")
            col.prop(obj.display, "show_shadows", text="Shadow")
        col.prop(obj, "show_in_front", text="In Front")

        sub = layout.column()
        if is_wire:

            sub.active = is_dupli
        sub.prop(obj, "display_type", text="Display As")

        if is_geometry or is_dupli or is_empty_image or is_gpencil:

            col.prop(obj, "color")

        col = layout.column(align=False, heading="Bounds")
        col.use_property_decorate = False
        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(obj, "show_bounds", text="")
        sub = sub.row(align=True)
        sub.active = obj.show_bounds or (obj.display_type == 'BOUNDS')
        sub.prop(obj, "display_bounds_type", text="")
        row.prop_decorator(obj, "display_bounds_type")


class WHIZIBILITY_PT_WhizibilityPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_idname = "WHIZIBILITY_PT_whizibilitylibpanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Whizibility Stuff"
    bl_category = "WhizTools"

    def draw(self, context):
        wm = context.window_manager
        scene = context.scene

        layout = self.layout


class WHIZIBILITY_PT_WhizibilityUtils(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_idname = "WHIZIBILITY_PT_whizibilityutilitypanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Utilities"
    bl_category = "WhizTools"

    def draw(self, context):
        wm = context.window_manager
        scene = context.scene

        layout = self.layout


def register():

    bpy.utils.register_class(WHIZIBILITY_PT_Viewport)
    bpy.utils.register_class(WHIZIBILITY_PT_Render)
    bpy.utils.register_class(WHIZIBILITY_PT_RenderCycles)
    bpy.utils.register_class(WHIZIBILITY_PT_WhizibilityUtils)


def unregister():

    bpy.utils.unregister_class(WHIZIBILITY_PT_Viewport)
    bpy.utils.unregister_class(WHIZIBILITY_PT_Render)
    bpy.utils.unregister_class(WHIZIBILITY_PT_RenderCycles)
    bpy.utils.unregister_class(WHIZIBILITY_PT_WhizibilityUtils)


if __name__ == "__main__":
    register()
