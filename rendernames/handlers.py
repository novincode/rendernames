# ============================================================================
# RenderNames - Handlers
# ============================================================================
# Blender event handlers for automatic render path updates
# Hooks into render pipeline to apply templates dynamically

import os
from typing import Set

import bpy
from bpy.app.handlers import persistent

from . import template_engine


# ============================================================================
# Handler Functions
# ============================================================================

@persistent
def on_render_init(scene):
    """
    Called before rendering starts.
    
    Applies the template to the render output path.
    This is where the magic happens - we intercept the render
    and set the correct output path based on the template.
    """
    if not hasattr(scene, "rendernames"):
        return
    
    props = scene.rendernames
    
    if not props.enabled:
        return
    
    if not props.template:
        return
    
    try:
        # Render the template
        rendered = template_engine.render_template(
            props.template,
            scene,
            props,
        )
        
        # Get base path
        if props.use_base_path and props.base_path:
            # Use custom base path
            base_path = props.base_path
        else:
            # Use Blender's existing output path directory
            existing_path = scene.render.filepath
            if existing_path:
                # Extract directory from existing path
                base_path = os.path.dirname(existing_path)
                if not base_path:
                    base_path = "//renders/"
            else:
                base_path = "//renders/"
        
        # Combine and set the render path
        full_path = os.path.join(base_path, rendered)
        
        # Store original path for potential restoration
        if not hasattr(scene, "_rendernames_original_path"):
            scene["_rendernames_original_path"] = scene.render.filepath
        
        # Set the new path
        scene.render.filepath = full_path
        
        # Ensure the directory exists
        abs_path = bpy.path.abspath(full_path)
        dir_path = os.path.dirname(abs_path)
        
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print(f"RenderNames: Created directory: {dir_path}")
        
        print(f"RenderNames: Output path set to: {full_path}")
        
    except Exception as e:
        print(f"RenderNames: Error applying template: {e}")


@persistent
def on_render_complete(scene):
    """
    Called after rendering completes.
    
    Could be used for logging or cleanup.
    """
    if not hasattr(scene, "rendernames"):
        return
    
    props = scene.rendernames
    
    if not props.enabled:
        return
    
    # Log success (optional)
    print(f"RenderNames: Render complete - {scene.render.filepath}")


@persistent
def on_render_cancel(scene):
    """
    Called when rendering is cancelled.
    """
    pass  # Nothing special needed


@persistent
def on_load_post(dummy):
    """
    Called after a .blend file is loaded.
    
    Refreshes the preset list and updates preview.
    """
    # Refresh presets for all scenes
    for scene in bpy.data.scenes:
        if hasattr(scene, "rendernames"):
            from . import presets
            presets.refresh_preset_list(scene.rendernames)


@persistent
def on_scene_update(scene, depsgraph):
    """
    Called when scene updates (used for live preview updates).
    
    Note: This can be called very frequently, so we keep it minimal.
    The preview is primarily updated via property update callbacks.
    """
    pass  # Preview updates handled by property callbacks


# ============================================================================
# Timer for Preview Updates (Optional)
# ============================================================================

def _preview_timer():
    """
    Timer function for periodic preview updates.
    
    This ensures the preview stays current even when
    external factors change (like system time).
    
    Returns None to stop, or float for next interval.
    """
    try:
        context = bpy.context
        if context and context.scene and hasattr(context.scene, "rendernames"):
            props = context.scene.rendernames
            
            if props.enabled and props.template:
                preview = template_engine.render_template(
                    props.template,
                    context.scene,
                    props,
                    sample=True,
                )
                
                # Only update if changed (avoid unnecessary redraws)
                if props.preview != preview:
                    props["preview"] = preview
    except Exception:
        pass  # Silently fail - timer shouldn't crash Blender
    
    return 5.0  # Update every 5 seconds


# Track if timer is registered
_timer_registered = False


# ============================================================================
# Registration
# ============================================================================

def register():
    """Register handlers."""
    global _timer_registered
    
    # Render handlers
    if on_render_init not in bpy.app.handlers.render_init:
        bpy.app.handlers.render_init.append(on_render_init)
    
    if on_render_complete not in bpy.app.handlers.render_complete:
        bpy.app.handlers.render_complete.append(on_render_complete)
    
    if on_render_cancel not in bpy.app.handlers.render_cancel:
        bpy.app.handlers.render_cancel.append(on_render_cancel)
    
    # File load handler
    if on_load_post not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(on_load_post)
    
    # Register preview timer
    if not _timer_registered:
        bpy.app.timers.register(_preview_timer, first_interval=1.0)
        _timer_registered = True


def unregister():
    """Unregister handlers."""
    global _timer_registered
    
    # Render handlers
    if on_render_init in bpy.app.handlers.render_init:
        bpy.app.handlers.render_init.remove(on_render_init)
    
    if on_render_complete in bpy.app.handlers.render_complete:
        bpy.app.handlers.render_complete.remove(on_render_complete)
    
    if on_render_cancel in bpy.app.handlers.render_cancel:
        bpy.app.handlers.render_cancel.remove(on_render_cancel)
    
    # File load handler
    if on_load_post in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(on_load_post)
    
    # Unregister timer
    if _timer_registered:
        if bpy.app.timers.is_registered(_preview_timer):
            bpy.app.timers.unregister(_preview_timer)
        _timer_registered = False
