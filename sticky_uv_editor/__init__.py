# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

import bpy
from bpy.props import BoolProperty, EnumProperty, PointerProperty
from bpy.types import AddonPreferences, GizmoGroup, Operator, Scene
from bpy.utils import register_class, unregister_class

from .modules.keymap_manager import (draw_key, register_keymap,
                                     unregister_keymap)
from .uv_editor_settings import UVEditorSettings

bl_info = {
    "name": "Sticky UV Editor",
    "author": "Oleg Stepanov (DotBow)",
    "description": "Quickly toggle UV Editor in 3D Viewport area",
    "blender": (2, 90, 0),
    "version": (1, 0, 0),
    "location": "3D Viewport",
    "warning": "",
    "category": "UV"
}


class AddonPreferences(AddonPreferences):
    bl_idname = __name__

    uv_editor_side: EnumProperty(
        name="UV Editor Side",
        description="3D Viewport area side where to open UV Editor",
        items={('LEFT', "Left",
                "Open UV Editor on the left side of 3D Viewport area", 0),
               ('RIGHT', "Right",
                "Open UV Editor on the right side of 3D Viewport area", 1)},
        default='LEFT')
    show_ui_button: BoolProperty(
        name="Show Overlay Button",
        description="Show overlay button on corresponding side of 3D Viewport",
        default=True)
    remember_uv_editor_settings: BoolProperty(
        name="Remember UV Editor Settings",
        description="Remember changes made in UV Editor area",
        default=True)
    uv_editor_settings: PointerProperty(type=UVEditorSettings)

    view_mode: EnumProperty(
        name="View Mode",
        description="Adjust UV Editor view when open",
        items={('DISABLE', "Disable",
                "Do not modify the view", 0),
               ('FRAME_ALL', "Frame All UVs",
                "View all UVs", 1),
               ('FRAME_SELECTED', "Frame Selected",
                "View all selected UVs", 2),
               ('FRAME_ALL_FIT', "Frame All UDIMs",
                "View all UDIMs", 3)},
        default='DISABLE')
    use_uv_select_sync: BoolProperty(
        name="UV Sync Selection",
        description="Keep UV an edit mode mesh selection in sync",
        default=False)

    def draw(self, context):
        layout = self.layout

        # Draw preferences
        box = layout.box()
        split = box.split()
        col = split.column()
        col.label(text="Add-on Settings:")
        col.separator()
        col.prop(self, "uv_editor_side")
        col.prop(self, "show_ui_button")
        col.prop(self, "remember_uv_editor_settings")

        box = layout.box()
        split = box.split()
        col = split.column()
        col.label(text="UV Editor Tool Settings:")
        col.separator()

        col.prop(self, "use_uv_select_sync")

        box = layout.box()
        split = box.split()
        col = split.column()
        col.label(text="UV Editor Overlay Settings:")
        col.separator()

        col.label(text="UV Editor")
        row = col.row()
        row.prop(self.uv_editor_settings, "show_stretch")
        row.prop(self.uv_editor_settings, "display_stretch_type", text="")
        col.separator()

        col.label(text="Geometry")
        col.prop(self.uv_editor_settings, "uv_opacity")
        col.prop(self.uv_editor_settings, "edge_display_type", text="")
        col.prop(self.uv_editor_settings, "show_modified_edges")
        col.prop(self.uv_editor_settings, "show_faces")
        col.separator()

        col.label(text="Image")
        col.prop(self.uv_editor_settings, "show_metadata")

        box = layout.box()
        split = box.split()
        col = split.column()
        col.label(text="UV Editor View Settings:")
        col.separator()

        col.prop(self, "view_mode")
        col.prop(self.uv_editor_settings, "show_region_toolbar")
        col.prop(self.uv_editor_settings, "show_region_ui")
        col.prop(self.uv_editor_settings, "show_region_tool_header")
        col.prop(self.uv_editor_settings, "show_region_hud")

        # Draw keymap
        keys = [('Window', 'wm.sticky_uv_editor', None)]
        draw_key(self.layout, keys)


class StickyUVEditor(Operator):
    """\
Show/Hide UV Editor on the right side of the 3D Viewport.
Hold 'Alt' to open UV Editor in a separate window."""
    bl_idname = "wm.sticky_uv_editor"
    bl_label = "Sticky UV Editor"
    bl_options = {'INTERNAL'}

    ui_button: BoolProperty(default=False)

    @classmethod
    def poll(self, context):
        if context.area.ui_type not in ['UV', 'VIEW_3D']:
            return False

        return True

    def invoke(self, context, event):
        scene = context.scene
        active_area = context.area

        if not event.alt:
            if context.window.screen.show_fullscreen is True:
                self.report({'WARNING'},
                            "Sticky UV Editor: Fullscreen mode is not supported!")
                return {'FINISHED'}

            areas = context.screen.areas
            active_area_x = active_area.x
            active_area_y = active_area.y
            active_area_width = active_area.width

            # Close existing UV Editor
            if active_area.ui_type == 'UV':
                for area in areas:
                    if area.ui_type == 'VIEW_3D':
                        area_x = area.x
                        area_y = area.y
                        area_width = area.width

                        # Areas in one horizontal space
                        if area_y == active_area_y:
                            # UV Editor on left
                            if (active_area_x + active_area_width + 1) == area_x:
                                # Save UV Editor area settings
                                scene.uv_editor_settings.save_from_area(
                                    active_area)

                                # Close UV Editor area
                                bpy.ops.screen.area_join(
                                    cursor=(area_x, area_y + 10))

                                # Force update layout
                                space = area.spaces[0]
                                space.show_region_toolbar = \
                                    space.show_region_toolbar

                                return {'FINISHED'}

                            # UV Editor on right
                            if (area_x + area_width + 1) == active_area_x:
                                # Save UV Editor area settings
                                scene.uv_editor_settings.save_from_area(
                                    active_area)

                                # Close UV Editor area
                                bpy.ops.screen.area_swap(
                                    cursor=(active_area_x, active_area_y + 10))
                                bpy.ops.screen.area_join(
                                    cursor=(active_area_x, active_area_y + 10))

                                # Force update layout
                                space = active_area.spaces[0]
                                space.show_region_toolbar = \
                                    space.show_region_toolbar

                                return {'FINISHED'}

                self.report({'WARNING'},
                            "Sticky UV Editor: Failed to figure out current layout!")
                return {'FINISHED'}
            elif active_area.ui_type == 'VIEW_3D':
                for area in areas:
                    if area.ui_type == 'UV':
                        area_x = area.x
                        area_y = area.y
                        area_width = area.width

                        # Areas in one horizontal space
                        if area_y == active_area_y:
                            # 3D View on left
                            if (active_area_x + active_area_width + 1) == area_x:
                                # Save UV Editor area settings
                                scene.uv_editor_settings.save_from_area(area)

                                # Close UV Editor area
                                bpy.ops.screen.area_swap(
                                    cursor=(area_x, area_y + 10))
                                bpy.ops.screen.area_join(
                                    cursor=(area_x, area_y + 10))

                                # Force update layout
                                space = area.spaces[0]
                                space.show_region_toolbar = \
                                    space.show_region_toolbar

                                return {'FINISHED'}

                            # 3D View on right
                            if (area_x + area_width + 1) == active_area_x:
                                # Save UV Editor area settings
                                scene.uv_editor_settings.save_from_area(area)

                                # Close UV Editor area
                                bpy.ops.screen.area_join(
                                    cursor=(active_area_x, active_area_y + 10))

                                # Force update layout
                                space = active_area.spaces[0]
                                space.show_region_toolbar = \
                                    space.show_region_toolbar

                                return {'FINISHED'}

            # Split active 3D View area
            bpy.ops.screen.area_split(
                direction='VERTICAL', factor=0.5)

        # Open UV Editor
        addon_prefs = context.preferences.addons[__name__].preferences

        if addon_prefs.uv_editor_side == 'LEFT':
            for area in reversed(context.screen.areas):
                if area.ui_type == 'VIEW_3D':
                    uv_area = area
                    break

            if self.ui_button is True:
                context.window.cursor_warp(
                    event.mouse_x + context.area.width * 0.5, event.mouse_y)
        else:
            uv_area = active_area

            if self.ui_button is True:
                context.window.cursor_warp(
                    event.mouse_x - context.area.width * 0.5, event.mouse_y)

        ui_type = active_area.ui_type
        uv_area.ui_type = 'UV'

        # Set UV Editor area settings
        uv_editor_settings = scene.uv_editor_settings

        if (uv_editor_settings.initialized is False) or \
                (addon_prefs.remember_uv_editor_settings is False):
            uv_editor_settings.save_from_property(
                addon_prefs.uv_editor_settings)
            uv_editor_settings.initialized = True
            scene.tool_settings.use_uv_select_sync = \
                addon_prefs.use_uv_select_sync

        uv_editor_settings.set(uv_area)

        # Set view mode
        view_mode = addon_prefs.view_mode

        if (view_mode != 'DISABLE') and (context.mode == 'EDIT_MESH'):
            override = {'window': context.window,
                        'screen': context.window.screen, 'area': area}

            if view_mode == 'FRAME_ALL':
                bpy.ops.image.view_all(override)
            elif view_mode == 'FRAME_SELECTED':
                bpy.ops.image.view_selected(override)
            elif view_mode == 'FRAME_ALL_FIT':
                bpy.ops.image.view_all(override, fit_view=True)

        # Open UV Editor in new window
        if event.alt:
            bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
            active_area.ui_type = ui_type

        return {'FINISHED'}


class StickyUVEditor_UI_Button(GizmoGroup):
    bl_idname = "StickyUVEditor_UI_Button"
    bl_label = "Sticky UV Editor UI Button"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'PERSISTENT', 'SCALE'}

    @classmethod
    def poll(cls, context):
        addon_prefs = context.preferences.addons[__name__].preferences
        return (addon_prefs.show_ui_button) and \
            (not context.window.screen.show_fullscreen)

    def draw_prepare(self, context):
        addon_prefs = context.preferences.addons[__name__].preferences
        ui_scale = context.preferences.view.ui_scale

        width = 0
        padding = 20 * ui_scale

        if addon_prefs.uv_editor_side == 'LEFT':
            for region in bpy.context.area.regions:
                if region.type == "TOOLS":
                    width = region.width
                    break

            self.foo_gizmo.matrix_basis[0][3] = width + padding
        else:
            for region in bpy.context.area.regions:
                if region.type == "UI":
                    width = region.width
                    break

            self.foo_gizmo.matrix_basis[0][3] = \
                context.region.width - padding - width

        self.foo_gizmo.matrix_basis[1][3] = context.region.height * 0.5

    def setup(self, context):
        mpr = self.gizmos.new("GIZMO_GT_button_2d")
        mpr.show_drag = False
        mpr.icon = 'UV'
        mpr.draw_options = {'BACKDROP', 'OUTLINE'}

        mpr.color = 0.0, 0.0, 0.0
        mpr.alpha = 0.5
        mpr.color_highlight = 0.8, 0.8, 0.8
        mpr.alpha_highlight = 0.2

        mpr.scale_basis = (80 * 0.35) / 2  # Same as buttons defined in C
        op = mpr.target_set_operator("wm.sticky_uv_editor")
        op.ui_button = True
        self.foo_gizmo = mpr


classes = (
    UVEditorSettings,
    AddonPreferences,
    StickyUVEditor,
    StickyUVEditor_UI_Button
)


def sticky_uv_editor_button(self, context):
    layout = self.layout
    layout.operator("wm.sticky_uv_editor", text="", icon='UV')


def register():
    for cls in classes:
        register_class(cls)

    Scene.uv_editor_settings = PointerProperty(type=UVEditorSettings)
    register_keymap()


def unregister():
    for cls in classes:
        unregister_class(cls)

    unregister_keymap()


if __name__ == "__main__":
    register()
