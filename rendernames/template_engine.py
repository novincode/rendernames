# ============================================================================
# RenderNames - Template Engine
# ============================================================================
# Core logic for parsing and rendering templates
# All template variable definitions and substitution logic

import re
import os
from datetime import datetime
from typing import Dict, Callable, Optional, Any

import bpy


# ============================================================================
# Template Variable Definitions
# ============================================================================

# Each variable is a tuple of (description, resolver_function)
# Resolver receives (scene, props) and returns the string value

def _get_variables() -> Dict[str, tuple[str, Callable]]:
    """
    Get all available template variables.
    
    Returns a dict of variable_name -> (description, resolver_function)
    """
    return {
        # Scene & Project
        "scene": (
            "Current scene name",
            lambda scene, props: scene.name,
        ),
        "blend_file": (
            "Blend file name (without .blend)",
            lambda scene, props: (
                os.path.splitext(os.path.basename(bpy.data.filepath))[0]
                if bpy.data.filepath else "untitled"
            ),
        ),
        
        # Frame Information
        "frame": (
            "⚠️ Not recommended - Blender adds frames automatically",
            lambda scene, props: str(scene.frame_start).zfill(props.frame_padding),
        ),
        "frame_start": (
            "First frame of range",
            lambda scene, props: str(scene.frame_start).zfill(props.frame_padding),
        ),
        "frame_end": (
            "Last frame of range",
            lambda scene, props: str(scene.frame_end).zfill(props.frame_padding),
        ),
        "frame_range": (
            "Frame range (start-end) with padding applied",
            lambda scene, props: f"{scene.frame_start}".zfill(props.frame_padding) + "-" + f"{scene.frame_end}".zfill(props.frame_padding),
        ),
        
        # Date & Time
        "date": (
            "Current date (YYYY-MM-DD)",
            lambda scene, props: datetime.now().strftime("%Y-%m-%d"),
        ),
        "time": (
            "Current time (HH-MM-SS)",
            lambda scene, props: datetime.now().strftime("%H-%M-%S"),
        ),
        "datetime": (
            "Date and time combined",
            lambda scene, props: datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        ),
        "year": (
            "Current year",
            lambda scene, props: datetime.now().strftime("%Y"),
        ),
        "month": (
            "Current month",
            lambda scene, props: datetime.now().strftime("%m"),
        ),
        "day": (
            "Current day",
            lambda scene, props: datetime.now().strftime("%d"),
        ),
        
        # Camera
        "camera": (
            "Active camera name",
            lambda scene, props: scene.camera.name if scene.camera else "no_camera",
        ),
        
        # Resolution
        "resolution": (
            "Resolution (WxH)",
            lambda scene, props: f"{scene.render.resolution_x}x{scene.render.resolution_y}",
        ),
        "width": (
            "Resolution width",
            lambda scene, props: str(scene.render.resolution_x),
        ),
        "height": (
            "Resolution height",
            lambda scene, props: str(scene.render.resolution_y),
        ),
        "percent": (
            "Resolution percentage",
            lambda scene, props: str(scene.render.resolution_percentage),
        ),
        
        # Render Settings
        "fps": (
            "Frames per second",
            lambda scene, props: str(scene.render.fps),
        ),
        "format": (
            "Output format (PNG, JPEG, etc.)",
            lambda scene, props: scene.render.image_settings.file_format.lower(),
        ),
        "engine": (
            "Render engine (cycles, eevee, etc.)",
            lambda scene, props: scene.render.engine.lower().replace("blender_", ""),
        ),
        "samples": (
            "Render samples (Cycles only)",
            lambda scene, props: _get_samples(scene),
        ),
    }


def _get_samples(scene) -> str:
    """Get sample count for the current render engine."""
    engine = scene.render.engine
    if engine == "CYCLES":
        return str(scene.cycles.samples)
    elif engine == "BLENDER_EEVEE_NEXT":
        # Blender 4.2+ uses EEVEE Next
        if hasattr(scene.eevee, "taa_render_samples"):
            return str(scene.eevee.taa_render_samples)
        return "64"  # Default
    elif engine == "BLENDER_EEVEE":
        # Legacy EEVEE (pre-4.2)
        if hasattr(scene.eevee, "taa_render_samples"):
            return str(scene.eevee.taa_render_samples)
        return "64"
    return "n/a"


# ============================================================================
# Template Rendering
# ============================================================================

# Regex pattern to match {{variable}} syntax
_TEMPLATE_PATTERN = re.compile(r"\{\{(\w+)\}\}")


def get_variable_names() -> list[str]:
    """Get list of all available variable names."""
    return list(_get_variables().keys())


def get_variable_descriptions() -> Dict[str, str]:
    """Get dict of variable names to descriptions."""
    return {name: info[0] for name, info in _get_variables().items()}


def render_template(
    template: str,
    scene: bpy.types.Scene,
    props: Any,
    sample: bool = False,
) -> str:
    """
    Render a template string by substituting all variables.
    
    Args:
        template: The template string with {{variable}} placeholders
        scene: The Blender scene context
        props: RenderNames properties
        sample: Not used (kept for compatibility)
        
    Returns:
        The rendered string with all variables substituted
    """
    variables = _get_variables()
    
    def replace_var(match):
        var_name = match.group(1)
        
        if var_name in variables:
            _, resolver = variables[var_name]
            
            try:
                value = resolver(scene, props)
            except Exception:
                value = f"[{var_name}]"
        else:
            # Unknown variable - keep it as-is for debugging
            return f"{{{{{var_name}}}}}"
        
        # Apply sanitization if enabled
        if props.sanitize_names:
            value = sanitize_string(value)
        
        # Apply lowercase if enabled
        if props.lowercase:
            value = value.lower()
        
        return value
    
    result = _TEMPLATE_PATTERN.sub(replace_var, template)
    return result


def sanitize_string(value: str) -> str:
    """
    Sanitize a string for use in file paths.
    
    Replaces spaces with underscores and removes problematic characters.
    """
    # Characters that are problematic in file paths across platforms
    bad_chars = '<>:"/\\|?*'
    
    result = value
    
    # Replace spaces with underscores
    result = result.replace(" ", "_")
    
    # Remove bad characters
    for char in bad_chars:
        result = result.replace(char, "")
    
    # Remove leading/trailing dots and spaces
    result = result.strip(". ")
    
    # Collapse multiple underscores
    while "__" in result:
        result = result.replace("__", "_")
    
    return result


def get_full_render_path(
    scene: bpy.types.Scene,
    props: Any,
    base_path: Optional[str] = None,
) -> str:
    """
    Get the full render output path including the rendered template.
    
    Args:
        scene: The Blender scene
        props: RenderNames properties
        base_path: Optional base path (defaults to //renders/)
        
    Returns:
        Absolute path for render output
    """
    if base_path is None:
        # Use relative path from .blend file location
        base_path = "//renders/"
    
    # Render the template
    rendered = render_template(props.template, scene, props)
    
    # Combine paths
    full_path = os.path.join(base_path, rendered)
    
    # Make absolute
    full_path = bpy.path.abspath(full_path)
    
    return full_path


# ============================================================================
# Validation
# ============================================================================

def validate_template(template: str) -> tuple[bool, str]:
    """
    Validate a template string.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not template:
        return False, "Template cannot be empty"
    
    # Check for unmatched braces
    open_count = template.count("{{")
    close_count = template.count("}}")
    
    if open_count != close_count:
        return False, "Unmatched braces in template"
    
    # Check for unknown variables
    variables = _get_variables()
    matches = _TEMPLATE_PATTERN.findall(template)
    
    unknown = [m for m in matches if m not in variables]
    if unknown:
        return False, f"Unknown variables: {', '.join(unknown)}"
    
    return True, ""
