
import bpy
from bpy.props import (BoolProperty, EnumProperty, FloatProperty, IntProperty,
                       IntVectorProperty)
from bpy.types import PropertyGroup


class UVEditorSettings(PropertyGroup):
    app_version = bpy.app.version
    initialized: BoolProperty(
        default=False)

    show_stretch: BoolProperty(
        name="Display Stretch",
        description="Display faces colored according to the difference in shape between UVs and their 3D coordinates (blue for low distortion, red for high distortion)",
        default=False)
    display_stretch_type: EnumProperty(
        name="Display Stretch Type",
        description="Type of stretch to draw",
        items={('ANGLE', "Angle",
                "Angle distortion between UV and 3D angles", 0),
               ('AREA', "Area",
                "Area distortion between UV and 3D faces", 1)},
        default='ANGLE')
    uv_opacity: FloatProperty(
        name="UV Opacity",
        description="Opacity of UV overlays",
        default=1.0,
        min=0.0, max=1.0)
    edge_display_type: EnumProperty(
        name="Display style for UV edges",
        description="Type of stretch to draw",
        items={('OUTLINE', "Outline",
                "Display white edges with black outline", 0),
               ('DASH', "Dash",
                "Display dashed black-white edges", 1),
               ('BLACK', "Black",
                "Display black edges", 2),
               ('WHITE', "White",
                "Display white edges", 3)},
        default='OUTLINE')
    show_modified_edges: BoolProperty(
        name="Modified Edges",
        description="Display edges after modifiers are applied",
        default=False)
    show_faces: BoolProperty(
        name="Faces",
        description="Display faces over the image",
        default=True)
    show_metadata: BoolProperty(
        name="Show Metadata",
        description="Display metadata properties of the image",
        default=True)

    tile_grid_shape: IntVectorProperty(
        name="UDIM Grid Shape",
        description="How many tiles will be shown in the background",
        size=2,
        default=(0, 0),
        min=0, max=100)
    use_custom_grid: BoolProperty(
        name="Custom Grid",
        description="Use a grid with a user-defined number of steps",
        default=True)
    custom_grid_subdivisions: IntProperty(
        name="Dynamic Grid Size",
        description="Number of Grid units in UV space that make one UV Unit",
        default=10,
        min=1, max=100)

    show_region_toolbar: BoolProperty(
        name="Show Toolbar",
        description="",
        default=False)
    show_region_ui: BoolProperty(
        name="Show Sidebar",
        description="",
        default=False)
    show_region_tool_header: BoolProperty(
        name="Show Tool Settings",
        description="",
        default=False)
    show_region_hud: BoolProperty(
        name="Show Adjust Last Operation",
        description="",
        default=False)

    pixel_snap_mode: EnumProperty(
        name="Snap to Pixels",
        description="",
        items={('DISABLED', "Disabled",
                "Don't snap to pixels", 0),
               ('CORNER', "Corner",
                "Snap to pixel corners", 1),
               ('CENTER', "Center",
                "Snap to pixel centers", 2)},
        default='DISABLED')
    lock_bounds: BoolProperty(
        name="Constrain to Image Bounds",
        description="Constraint to stay within the image bounds while editing",
        default=False)
    use_live_unwrap: BoolProperty(
        name="Live Unwrap",
        description="Continuously unwrap the selected island while transforming pinned vertices",
        default=False)

    def set(self, area):
        space = area.spaces[0]
        uv_editor = space.uv_editor

        uv_editor.show_stretch = self.show_stretch
        uv_editor.display_stretch_type = self.display_stretch_type
        uv_editor.uv_opacity = self.uv_opacity
        uv_editor.edge_display_type = self.edge_display_type
        uv_editor.show_modified_edges = self.show_modified_edges
        uv_editor.show_faces = self.show_faces
        uv_editor.show_metadata = self.show_metadata
        uv_editor.tile_grid_shape = self.tile_grid_shape

        if self.app_version >= (3, 0, 0):
            uv_editor.use_custom_grid = self.use_custom_grid
            uv_editor.custom_grid_subdivisions = self.custom_grid_subdivisions

        space.show_region_toolbar = self.show_region_toolbar
        space.show_region_ui = self.show_region_ui
        space.show_region_tool_header = self.show_region_tool_header
        space.show_region_hud = self.show_region_hud

        uv_editor.pixel_snap_mode = self.pixel_snap_mode
        uv_editor.lock_bounds = self.lock_bounds
        uv_editor.use_live_unwrap = self.use_live_unwrap

    def save_from_area(self, area):
        space = area.spaces[0]
        uv_editor = space.uv_editor

        self.show_stretch = uv_editor.show_stretch
        self.display_stretch_type = uv_editor.display_stretch_type
        self.uv_opacity = uv_editor.uv_opacity
        self.edge_display_type = uv_editor.edge_display_type
        self.show_modified_edges = uv_editor.show_modified_edges
        self.show_faces = uv_editor.show_faces
        self.show_metadata = uv_editor.show_metadata
        self.tile_grid_shape = uv_editor.tile_grid_shape

        if self.app_version >= (3, 0, 0):
            self.use_custom_grid = uv_editor.use_custom_grid
            self.custom_grid_subdivisions = uv_editor.custom_grid_subdivisions

        self.show_region_toolbar = space.show_region_toolbar
        self.show_region_ui = space.show_region_ui
        self.show_region_tool_header = space.show_region_tool_header
        self.show_region_hud = space.show_region_hud

        self.pixel_snap_mode = uv_editor.pixel_snap_mode
        self.lock_bounds = uv_editor.lock_bounds
        self.use_live_unwrap = uv_editor.use_live_unwrap

    def save_from_property(self, property):
        self.show_stretch = property.show_stretch
        self.display_stretch_type = property.display_stretch_type
        self.uv_opacity = property.uv_opacity
        self.edge_display_type = property.edge_display_type
        self.show_modified_edges = property.show_modified_edges
        self.show_faces = property.show_faces
        self.show_metadata = property.show_metadata
        self.tile_grid_shape = property.tile_grid_shape

        if self.app_version >= (3, 0, 0):
            self.use_custom_grid = property.use_custom_grid
            self.custom_grid_subdivisions = property.custom_grid_subdivisions

        self.show_region_toolbar = property.show_region_toolbar
        self.show_region_ui = property.show_region_ui
        self.show_region_tool_header = property.show_region_tool_header
        self.show_region_hud = property.show_region_hud

        self.pixel_snap_mode = property.pixel_snap_mode
        self.lock_bounds = property.lock_bounds
        self.use_live_unwrap = property.use_live_unwrap
