# ============================================================================
# RenderNames - Preset System
# ============================================================================
# Handles saving, loading, and managing presets
# Uses bpy.utils.extension_path_user for proper extension storage

import os
import json
from typing import Dict, Any, Optional, List

import bpy


# ============================================================================
# Built-in Presets
# ============================================================================

BUILTIN_PRESETS: Dict[str, Dict[str, Any]] = {
    "simple": {
        "template": "{{scene}}_{{frame}}",
        "use_base_path": False,
        "base_path": "",
        "folder_per_scene": False,
        "folder_per_camera": False,
        "folder_per_date": False,
        "use_blend_root": False,
        "sanitize_names": True,
        "lowercase": False,
        "frame_padding": 4,
    },
    "professional": {
        "template": "{{blend_file}}/{{date}}/{{scene}}_{{camera}}/{{frame}}",
        "use_base_path": False,
        "base_path": "",
        "folder_per_scene": True,
        "folder_per_camera": True,
        "folder_per_date": True,
        "use_blend_root": True,
        "sanitize_names": True,
        "lowercase": False,
        "frame_padding": 4,
    },
    "archival": {
        "template": "{{datetime}}/{{blend_file}}_{{scene}}_{{frame}}",
        "use_base_path": False,
        "base_path": "",
        "folder_per_scene": False,
        "folder_per_camera": False,
        "folder_per_date": True,
        "use_blend_root": False,
        "sanitize_names": True,
        "lowercase": False,
        "frame_padding": 5,
    },
    "by_camera": {
        "template": "{{camera}}/{{scene}}_{{frame}}",
        "use_base_path": False,
        "base_path": "",
        "folder_per_scene": False,
        "folder_per_camera": True,
        "folder_per_date": False,
        "use_blend_root": False,
        "sanitize_names": True,
        "lowercase": False,
        "frame_padding": 4,
    },
    "minimal": {
        "template": "{{scene}}_{{frame}}",
        "use_base_path": False,
        "base_path": "",
        "folder_per_scene": False,
        "folder_per_camera": False,
        "folder_per_date": False,
        "use_blend_root": False,
        "sanitize_names": True,
        "lowercase": False,
        "frame_padding": 4,
    },
}


# ============================================================================
# Storage Path
# ============================================================================

def _get_presets_dir() -> str:
    """
    Get the directory for storing user presets.
    
    Uses Blender's extension storage which:
    - Persists across extension upgrades
    - Is removed when extension is uninstalled
    - Is user-writable on all systems
    """
    # Get extension's user directory
    ext_dir = bpy.utils.extension_path_user(__package__, path="presets", create=True)
    return ext_dir


def _get_preset_path(name: str) -> str:
    """Get the full path for a preset file."""
    safe_name = _sanitize_filename(name)
    return os.path.join(_get_presets_dir(), f"{safe_name}.json")


def _sanitize_filename(name: str) -> str:
    """Sanitize a preset name for use as a filename."""
    # Remove/replace problematic characters
    bad_chars = '<>:"/\\|?*'
    result = name
    for char in bad_chars:
        result = result.replace(char, "_")
    result = result.strip(". ")
    return result


# ============================================================================
# Preset Data Extraction/Application
# ============================================================================

def extract_preset_data(props) -> Dict[str, Any]:
    """
    Extract current properties as a preset data dict.
    
    Args:
        props: RENDERNAMES_Properties instance
        
    Returns:
        Dict containing all saveable settings
    """
    return {
        "version": 1,  # For future compatibility
        "template": props.template,
        "use_base_path": props.use_base_path,
        "base_path": props.base_path,
        "folder_per_scene": props.folder_per_scene,
        "folder_per_camera": props.folder_per_camera,
        "folder_per_date": props.folder_per_date,
        "use_blend_root": props.use_blend_root,
        "sanitize_names": props.sanitize_names,
        "lowercase": props.lowercase,
        "frame_padding": props.frame_padding,
    }


# Flag to prevent update callbacks from overwriting template during preset load
_applying_preset = False


def apply_preset_data(props, data: Dict[str, Any]) -> None:
    """
    Apply preset data to properties.
    
    Args:
        props: RENDERNAMES_Properties instance
        data: Preset data dict
    """
    global _applying_preset
    
    # Save the template to reapply it if needed
    template_to_apply = data.get("template", "")
    
    # Set flag to prevent update callbacks from overwriting template
    _applying_preset = True
    
    try:
        # Handle version upgrades if needed
        # version = data.get("version", 1)
        
        # Apply folder structure options FIRST (these have update callbacks)
        # but the flag prevents them from overwriting the template
        if "folder_per_scene" in data:
            props.folder_per_scene = data["folder_per_scene"]
        
        if "folder_per_camera" in data:
            props.folder_per_camera = data["folder_per_camera"]
        
        if "folder_per_date" in data:
            props.folder_per_date = data["folder_per_date"]
        
        if "use_blend_root" in data:
            props.use_blend_root = data["use_blend_root"]
        
        # Apply other options
        if "use_base_path" in data:
            props.use_base_path = data["use_base_path"]
        
        if "base_path" in data:
            props.base_path = data["base_path"]
        
        if "sanitize_names" in data:
            props.sanitize_names = data["sanitize_names"]
        
        if "lowercase" in data:
            props.lowercase = data["lowercase"]
        
        if "frame_padding" in data:
            props.frame_padding = data["frame_padding"]
        
        # Apply template LAST to ensure it's not overwritten
        # Use direct assignment to bypass any intermediate updates
        if template_to_apply:
            props.template = template_to_apply
            # Verify it stuck - if folder options changed it, reapply
            if props.template != template_to_apply:
                props.template = template_to_apply
    
    finally:
        # Reset the flag AFTER everything is applied
        _applying_preset = False


def is_applying_preset() -> bool:
    """Check if we're currently applying a preset (for update callbacks)."""
    return _applying_preset


# ============================================================================
# Preset CRUD Operations
# ============================================================================

def list_presets() -> List[str]:
    """
    List all user presets.
    
    Returns:
        List of preset names (without .json extension)
    """
    presets_dir = _get_presets_dir()
    
    if not os.path.exists(presets_dir):
        return []
    
    presets = []
    for filename in os.listdir(presets_dir):
        if filename.endswith(".json"):
            name = os.path.splitext(filename)[0]
            presets.append(name)
    
    return sorted(presets)


def save_preset(name: str, data: Dict[str, Any]) -> bool:
    """
    Save a preset to disk.
    
    Args:
        name: Preset name
        data: Preset data dict
        
    Returns:
        True if successful
    """
    try:
        filepath = _get_preset_path(name)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        return True
        
    except Exception as e:
        print(f"RenderNames: Failed to save preset '{name}': {e}")
        return False


def load_preset(name: str) -> Optional[Dict[str, Any]]:
    """
    Load a preset from disk.
    
    Args:
        name: Preset name (or __builtin__<name> for built-ins)
        
    Returns:
        Preset data dict, or None if not found
    """
    # Handle built-in presets
    if name.startswith("__builtin__"):
        builtin_name = name.replace("__builtin__", "")
        return BUILTIN_PRESETS.get(builtin_name)
    
    try:
        filepath = _get_preset_path(name)
        
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
            
    except Exception as e:
        print(f"RenderNames: Failed to load preset '{name}': {e}")
        return None


def delete_preset(name: str) -> bool:
    """
    Delete a preset from disk.
    
    Args:
        name: Preset name
        
    Returns:
        True if successful
    """
    try:
        filepath = _get_preset_path(name)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        
        return False
        
    except Exception as e:
        print(f"RenderNames: Failed to delete preset '{name}': {e}")
        return False


def refresh_preset_list(props) -> None:
    """
    Refresh the presets collection property from disk.
    
    Args:
        props: RENDERNAMES_Properties instance
    """
    # Clear existing
    props.presets.clear()
    
    # Add user presets
    for name in list_presets():
        item = props.presets.add()
        item.name = name


# ============================================================================
# Initialization
# ============================================================================

def ensure_defaults() -> None:
    """
    Ensure default presets exist in the user directory.
    
    Called on extension registration.
    """
    # We don't copy built-ins to disk - they're loaded directly
    # This keeps the preset directory clean
    pass
