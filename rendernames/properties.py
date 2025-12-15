# ============================================================================
# RenderNames - Properties
# ============================================================================
# All property definitions for the extension
# Properties are stored per-scene and automatically saved with .blend files

import bpy
from bpy.props import (
    StringProperty,
    BoolProperty,
    IntProperty,
    EnumProperty,
    CollectionProperty,
)
from bpy.types import PropertyGroup


# ============================================================================
# Property Definitions
# ============================================================================

class RENDERNAMES_PresetItem(PropertyGroup):
    """Individual preset entry for the presets list."""
    name: StringProperty(
        name="Preset Name",
        default="",
    )


class RENDERNAMES_Properties(PropertyGroup):
    """Main property group for RenderNames settings."""
    
    # -------------------------------------------------------------------------
    # Master Toggle
    # -------------------------------------------------------------------------
    enabled: BoolProperty(
        name="Enable RenderNames",
        description="Enable smart render naming (disabling uses Blender's default path)",
        default=True,
    )
    
    # -------------------------------------------------------------------------
    # Template System
    # -------------------------------------------------------------------------
    template: StringProperty(
        name="Template",
        description="Template for render output naming. Use {{variable}} syntax",
        default="{{scene}}_{{frame}}",
        update=lambda self, ctx: _update_preview(self, ctx),
    )
    
    base_path: StringProperty(
        name="Base Path",
        description="Base directory for renders (leave empty to use Blender's output path)",
        default="",
        subtype="DIR_PATH",
    )
    
    use_base_path: BoolProperty(
        name="Use Custom Base Path",
        description="Use custom base path instead of Blender's output path",
        default=False,
    )
    
    # -------------------------------------------------------------------------
    # Organization Options (Folder Creation)
    # -------------------------------------------------------------------------
    folder_per_scene: BoolProperty(
        name="Folder per Scene",
        description="Create a subfolder for each scene",
        default=False,
        # REMOVED: update callback that was auto-modifying template
    )
    
    folder_per_camera: BoolProperty(
        name="Folder per Camera",
        description="Create a subfolder for each camera",
        default=False,
        # REMOVED: update callback that was auto-modifying template
    )
    
    folder_per_date: BoolProperty(
        name="Folder per Date",
        description="Create a subfolder for each render date",
        default=False,
        # REMOVED: update callback that was auto-modifying template
    )
    
    use_blend_root: BoolProperty(
        name="Use Blend File as Root",
        description="Use the .blend filename as the root folder",
        default=True,
        # REMOVED: update callback that was auto-modifying template
    )
    
    # -------------------------------------------------------------------------
    # Naming Options
    # -------------------------------------------------------------------------
    sanitize_names: BoolProperty(
        name="Sanitize Names",
        description="Replace special characters and spaces with underscores",
        default=True,
    )
    
    lowercase: BoolProperty(
        name="Lowercase",
        description="Convert all text to lowercase",
        default=False,
    )
    
    frame_padding: IntProperty(
        name="Frame Padding",
        description="Number of digits for frame numbers (e.g., 4 = 0001)",
        default=4,
        min=1,
        max=8,
    )
    
    # -------------------------------------------------------------------------
    # File Format Override
    # -------------------------------------------------------------------------
    include_extension: BoolProperty(
        name="Include Extension",
        description="Automatically append file extension based on output format",
        default=True,
    )
    
    # -------------------------------------------------------------------------
    # Live Preview (Read-only, computed)
    # -------------------------------------------------------------------------
    preview: StringProperty(
        name="Preview",
        description="Live preview of the render output path",
        default="",
    )
    
    # -------------------------------------------------------------------------
    # UI State
    # -------------------------------------------------------------------------
    show_options: BoolProperty(
        name="Show Options",
        description="Expand/collapse the options panel",
        default=True,
    )
    
    show_variables: BoolProperty(
        name="Show Variables",
        description="Expand/collapse the variables reference",
        default=False,
    )
    
    # -------------------------------------------------------------------------
    # Preset Management
    # -------------------------------------------------------------------------
    preset_name: StringProperty(
        name="Preset Name",
        description="Name for saving the current settings as a preset",
        default="",
    )
    
    presets: CollectionProperty(
        type=RENDERNAMES_PresetItem,
        name="Presets",
    )
    
    active_preset_index: IntProperty(
        name="Active Preset",
        default=0,
    )


# ============================================================================
# Update Callbacks
# ============================================================================

def _update_preview(props, context):
    """Update the live preview when template changes."""
    # Import here to avoid circular imports
    from . import template_engine
    
    if context.scene:
        preview_path = template_engine.render_template(
            props.template,
            context.scene,
            props,
        )
        props["preview"] = preview_path


# ============================================================================
# Registration
# ============================================================================

_classes = (
    RENDERNAMES_PresetItem,
    RENDERNAMES_Properties,
)


def register():
    """Register property classes."""
    for cls in _classes:
        bpy.utils.register_class(cls)
    
    # Attach to Scene type - settings persist with .blend file
    bpy.types.Scene.rendernames = bpy.props.PointerProperty(
        type=RENDERNAMES_Properties,
    )


def unregister():
    """Unregister property classes."""
    # Remove from Scene type
    if hasattr(bpy.types.Scene, "rendernames"):
        del bpy.types.Scene.rendernames
    
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
