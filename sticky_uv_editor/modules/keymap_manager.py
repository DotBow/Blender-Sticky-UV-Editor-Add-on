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
import rna_keymap_ui

from .keymap import keymap

addon_keymap = []


def get_hotkey_entry_item(km, kmi_name, kmi_value):
    for i, km_item in enumerate(km.keymap_items):
        if km.keymap_items.keys()[i] == kmi_name:
            if kmi_value is None:
                return km_item
            elif km.keymap_items[i].properties.name == kmi_value:
                return km_item

    return None


def register_keymap():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        addon_keymap.extend(keymap())


def unregister_keymap():
    for km, kmi in addon_keymap:
        km.keymap_items.remove(kmi)

    addon_keymap.clear()


def draw_key(layout, dict):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.user
    box = layout.box()
    split = box.split()
    col = split.column()
    col.label(text='Keymap:')

    dict.sort()
    km_name = None

    for item in dict:
        km = kc.keymaps[item[0]]
        kmi = get_hotkey_entry_item(km, item[1], item[2])

        if km_name != km.name:
            col.context_pointer_set("keymap", km)
            km_name = km.name
            col.separator()
            row = col.row(align=True)
            row.label(text=km_name)

            if km.is_user_modified:
                subrow = row.row()
                subrow.alignment = 'RIGHT'
                subrow.operator("preferences.keymap_restore", text="Restore")

        col.separator()

        if kmi:
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
        else:
            row = col.row(align=True)
            row.separator(factor=2.0)
            row.label(text="Keymap item for '" +
                      item[1] + "' in '" + item[0] + "' not found",
                      icon='ERROR')
