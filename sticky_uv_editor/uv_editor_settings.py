from bpy.props import (BoolProperty, EnumProperty, FloatProperty,
                       IntVectorProperty)
from bpy.types import PropertyGroup


class UVEditorSettings(PropertyGroup):
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
        name="Tile Grid Shape",
        description="How many tiles will be shown in the background",
        size=2,
        default=(0, 0))

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

        space.show_region_toolbar = self.show_region_toolbar
        space.show_region_ui = self.show_region_ui
        space.show_region_tool_header = self.show_region_tool_header
        space.show_region_hud = self.show_region_hud

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

        self.show_region_toolbar = space.show_region_toolbar
        self.show_region_ui = space.show_region_ui
        self.show_region_tool_header = space.show_region_tool_header
        self.show_region_hud = space.show_region_hud

    def save_from_property(self, property):
        self.show_stretch = property.show_stretch
        self.display_stretch_type = property.display_stretch_type
        self.uv_opacity = property.uv_opacity
        self.edge_display_type = property.edge_display_type
        self.show_modified_edges = property.show_modified_edges
        self.show_faces = property.show_faces
        self.show_metadata = property.show_metadata
        self.tile_grid_shape = property.tile_grid_shape

        self.show_region_toolbar = property.show_region_toolbar
        self.show_region_ui = property.show_region_ui
        self.show_region_tool_header = property.show_region_tool_header
        self.show_region_hud = property.show_region_hud
