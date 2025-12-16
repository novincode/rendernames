# ============================================================================
# RenderNames - Properties
# ============================================================================
# All property definitions for the extension
# Properties can be stored per-scene or globally (shared across all scenes)

import bpy
from bpy.props import (
    StringProperty,
    BoolProperty,
    IntProperty,
    EnumProperty,
    CollectionProperty,
    PointerProperty,
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


class RENDERNAMES_GlobalSettings(PropertyGroup):
    """Global settings stored on WindowManager - single source of truth for global mode."""
    
    # Copy of all synced properties
    enabled: BoolProperty(default=True)
    template: StringProperty(default="{{scene}}_")
    base_path: StringProperty(default="")
    use_base_path: BoolProperty(default=False)
    folder_per_scene: BoolProperty(default=False)
    folder_per_camera: BoolProperty(default=False)
    folder_per_date: BoolProperty(default=False)
    use_blend_root: BoolProperty(default=False)
    sanitize_names: BoolProperty(default=True)
    lowercase: BoolProperty(default=False)
    frame_padding: IntProperty(default=4, min=1, max=8)
    include_extension: BoolProperty(default=True)


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
    # Storage Mode (Global vs Per-Scene)
    # -------------------------------------------------------------------------
    use_global_settings: BoolProperty(
        name="Use Global Settings",
        description="Share settings across all scenes. When off, each scene has its own settings",
        default=True,
        update=lambda self, ctx: _on_storage_mode_changed(self, ctx),
    )
    
    # -------------------------------------------------------------------------
    # Template System
    # -------------------------------------------------------------------------
    template: StringProperty(
        name="Template",
        description="Template for render output naming. Use {{variable}} syntax",
        default="{{scene}}_",
        update=lambda self, ctx: _update_preview(self, ctx),
    )
    
    base_path: StringProperty(
        name="Base Path",
        description="Base directory for renders (leave empty to use Blender's output path)",
        default="",
        subtype="DIR_PATH",
        update=lambda self, ctx: _on_setting_changed(self, ctx),
    )
    
    use_base_path: BoolProperty(
        name="Use Custom Base Path",
        description="Use custom base path instead of Blender's output path",
        default=False,
        update=lambda self, ctx: _on_setting_changed(self, ctx),
    )
    
    # -------------------------------------------------------------------------
    # Organization Options (Folder Creation)
    # -------------------------------------------------------------------------
    folder_per_scene: BoolProperty(
        name="Folder per Scene",
        description="Create a subfolder for each scene",
        default=False,
        update=lambda self, ctx: _sync_template_from_options(self, ctx),
    )
    
    folder_per_camera: BoolProperty(
        name="Folder per Camera",
        description="Create a subfolder for each camera",
        default=False,
        update=lambda self, ctx: _sync_template_from_options(self, ctx),
    )
    
    folder_per_date: BoolProperty(
        name="Folder per Date",
        description="Create a subfolder for each render date",
        default=False,
        update=lambda self, ctx: _sync_template_from_options(self, ctx),
    )
    
    use_blend_root: BoolProperty(
        name="Use Blend File as Root",
        description="Use the .blend filename as the root folder",
        default=False,
        update=lambda self, ctx: _sync_template_from_options(self, ctx),
    )
    
    # -------------------------------------------------------------------------
    # Naming Options
    # -------------------------------------------------------------------------
    sanitize_names: BoolProperty(
        name="Sanitize Names",
        description="Replace special characters and spaces with underscores",
        default=True,
        update=lambda self, ctx: _on_setting_changed(self, ctx),
    )
    
    lowercase: BoolProperty(
        name="Lowercase",
        description="Convert all text to lowercase",
        default=False,
        update=lambda self, ctx: _on_setting_changed(self, ctx),
    )
    
    frame_padding: IntProperty(
        name="Frame Padding",
        description="Number of digits for frame numbers (e.g., 4 = 0001)",
        default=4,
        min=1,
        max=8,
        update=lambda self, ctx: _on_setting_changed(self, ctx),
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

def _on_setting_changed(props, context):
    """Called when any synced setting changes. Syncs to global and other scenes if in global mode."""
    from . import presets
    
    # Don't sync while applying a preset
    if presets.is_applying_preset():
        return
    
    if not props.use_global_settings:
        return
    
    if context is None or context.scene is None:
        return
    
    # Update the global storage on WindowManager
    _save_to_global_settings(context)
    
    # IMMEDIATELY sync to all other scenes in global mode
    _sync_global_to_all_scenes(context)


def _update_preview(props, context):
    """Update the live preview when template changes."""
    # Import here to avoid circular imports
    from . import template_engine
    from . import presets
    
    if context.scene:
        preview_path = template_engine.render_template(
            props.template,
            context.scene,
            props,
        )
        props["preview"] = preview_path
        
        # If using global settings and not applying a preset, sync to global and other scenes
        if props.use_global_settings and not presets.is_applying_preset():
            _save_to_global_settings(context)
            _sync_global_to_all_scenes(context)


def _sync_template_from_options(props, context):
    """Build template path from folder structure checkboxes."""
    # Don't overwrite template while applying a preset - return EARLY and SKIP EVERYTHING
    from . import presets
    if presets.is_applying_preset():
        return  # Exit completely, don't modify anything
    
    parts = []
    
    # Root folder
    if props.use_blend_root:
        parts.append("{{blend_file}}")
    
    # Subfolders
    if props.folder_per_scene:
        parts.append("{{scene}}")
    if props.folder_per_camera:
        parts.append("{{camera}}")
    if props.folder_per_date:
        parts.append("{{date}}")
    
    # Filename base
    if not props.folder_per_scene:
        # If scene isn't a folder, include it in filename
        parts.append("{{scene}}_")
    else:
        # Scene is already a folder, just add underscore for frame
        parts.append("")
    
    # Build path
    new_template = "/".join(parts)
    
    # Only update if actually changed
    if props.template != new_template:
        props.template = new_template
        # Update preview ONLY if template actually changed
        _update_preview(props, context)


def _on_storage_mode_changed(props, context):
    """Called when use_global_settings toggle changes."""
    if props.use_global_settings:
        # Switching to global mode - copy current scene settings to global
        _save_to_global_settings(context)
    else:
        # Switching to local mode - settings stay as-is for this scene
        pass


# ============================================================================
# Global Settings Helpers
# ============================================================================

# Properties to sync between global and local settings
_SYNC_PROPERTIES = [
    "enabled",
    "template",
    "base_path",
    "use_base_path",
    "folder_per_scene",
    "folder_per_camera",
    "folder_per_date",
    "use_blend_root",
    "sanitize_names",
    "lowercase",
    "frame_padding",
    "include_extension",
]


def _get_global_settings(context):
    """Get the global settings property group from WindowManager."""
    try:
        wm = context.window_manager
        if not hasattr(wm, "rendernames_global"):
            wm.rendernames_global = bpy.props.PointerProperty(type=RENDERNAMES_GlobalSettings)
        return wm.rendernames_global
    except Exception:
        return None


def _save_to_global_settings(context):
    """Save current scene's settings to the global storage on WindowManager."""
    if not context.scene or not hasattr(context.scene, "rendernames"):
        return
    
    scene_props = context.scene.rendernames
    global_props = _get_global_settings(context)
    
    if global_props is None:
        return
    
    # Copy all synced properties from scene to global
    for prop_name in _SYNC_PROPERTIES:
        if hasattr(scene_props, prop_name):
            value = getattr(scene_props, prop_name)
            if hasattr(global_props, prop_name):
                setattr(global_props, prop_name, value)


def _load_from_global_settings(context, target_props):
    """Load settings from global storage to a scene's properties."""
    if not context.scene:
        return
    
    global_props = _get_global_settings(context)
    if global_props is None:
        return
    
    # Use the preset flag to prevent update callbacks
    from . import presets
    original_flag = presets._applying_preset
    presets._applying_preset = True
    
    try:
        for prop_name in _SYNC_PROPERTIES:
            if hasattr(global_props, prop_name) and hasattr(target_props, prop_name):
                value = getattr(global_props, prop_name)
                setattr(target_props, prop_name, value)
    finally:
        presets._applying_preset = original_flag


def _sync_global_to_all_scenes(context):
    """IMMEDIATELY sync global settings to all scenes that use global mode."""
    global_props = _get_global_settings(context)
    if global_props is None:
        return
    
    from . import presets
    
    for scene in bpy.data.scenes:
        if not hasattr(scene, "rendernames"):
            continue
        
        scene_props = scene.rendernames
        
        # Skip scenes not in global mode
        if not scene_props.use_global_settings:
            continue
        
        # Skip the current scene (already updated)
        if scene == context.scene:
            continue
        
        # Temporarily set the flag
        original_flag = presets._applying_preset
        presets._applying_preset = True
        
        try:
            # Copy all synced properties from global to this scene
            for prop_name in _SYNC_PROPERTIES:
                if hasattr(global_props, prop_name) and hasattr(scene_props, prop_name):
                    value = getattr(global_props, prop_name)
                    setattr(scene_props, prop_name, value)
        finally:
            presets._applying_preset = original_flag


def get_effective_props(scene):
    """Get the effective properties for a scene."""
    return scene.rendernames


# ============================================================================
# Registration
# ============================================================================

_classes = (
    RENDERNAMES_PresetItem,
    RENDERNAMES_GlobalSettings,
    RENDERNAMES_Properties,
)


def register():
    """Register property classes."""
    for cls in _classes:
        bpy.utils.register_class(cls)
    
    # Attach global settings to WindowManager - session-persistent
    bpy.types.WindowManager.rendernames_global = bpy.props.PointerProperty(
        type=RENDERNAMES_GlobalSettings,
    )
    
    # Attach per-scene settings to Scene
    bpy.types.Scene.rendernames = bpy.props.PointerProperty(
        type=RENDERNAMES_Properties,
    )


def unregister():
    """Unregister property classes."""
    # Remove from WindowManager
    if hasattr(bpy.types.WindowManager, "rendernames_global"):
        del bpy.types.WindowManager.rendernames_global
    
    # Remove from Scene
    if hasattr(bpy.types.Scene, "rendernames"):
        del bpy.types.Scene.rendernames
    
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
