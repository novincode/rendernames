# ============================================================================
# RenderNames - Handlers
# ============================================================================
# Blender event handlers for render path management
# Strategy: Set path before render, restore after render completes

import os

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
    
    Apply the template to render.filepath, but store the original
    so we can restore it after rendering completes.
    """
    if not hasattr(scene, "rendernames"):
        return
    
    props = scene.rendernames
    
    if not props.enabled:
        return
    
    if not props.template:
        return
    
    try:
        # Store original path ONLY on first render_init call
        if "_rendernames_original_filepath" not in scene:
            scene["_rendernames_original_filepath"] = scene.render.filepath
        
        # Get base path
        if props.use_base_path and props.base_path:
            base_path = props.base_path
        else:
            base_path = "//"
        
        # Render the template
        rendered = template_engine.render_template(
            props.template,
            scene,
            props,
        )
        
        # Build full path
        if base_path.endswith("/"):
            full_path = base_path + rendered
        else:
            full_path = base_path + "/" + rendered
        
        # Create directories
        abs_path = bpy.path.abspath(full_path)
        dir_path = os.path.dirname(abs_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        
        # Apply to render
        scene.render.filepath = full_path
        print(f"RenderNames: Set render path to: {full_path}")
        
    except Exception as e:
        print(f"RenderNames: Error in render_init: {e}")


@persistent
def on_render_complete(scene):
    """
    Called after rendering completes.
    
    Restore the original filepath that user had set.
    """
    if not hasattr(scene, "rendernames"):
        return
    
    props = scene.rendernames
    
    if not props.enabled:
        return
    
    try:
        # Restore original path
        if "_rendernames_original_filepath" in scene:
            original = scene["_rendernames_original_filepath"]
            scene.render.filepath = original
            print(f"RenderNames: Restored original path: {original}")
            # Clear the stored original
            del scene["_rendernames_original_filepath"]
    
    except Exception as e:
        print(f"RenderNames: Error in render_complete: {e}")


@persistent
def on_render_cancel(scene):
    """
    Called when rendering is cancelled.
    
    Restore the original filepath.
    """
    if not hasattr(scene, "rendernames"):
        return
    
    try:
        # Restore original path
        if "_rendernames_original_filepath" in scene:
            original = scene["_rendernames_original_filepath"]
            scene.render.filepath = original
            print(f"RenderNames: Render cancelled - restored path: {original}")
            # Clear the stored original
            del scene["_rendernames_original_filepath"]
    
    except Exception as e:
        print(f"RenderNames: Error in render_cancel: {e}")


@persistent
def on_load_post(dummy):
    """
    Called after a .blend file is loaded.
    
    Clean up any stored paths and refresh presets.
    """
    for scene in bpy.data.scenes:
        if "_rendernames_original_filepath" in scene:
            del scene["_rendernames_original_filepath"]
        
        if hasattr(scene, "rendernames"):
            from . import presets
            presets.refresh_preset_list(scene.rendernames)


# ============================================================================
# Timer for Preview Updates
# ============================================================================

def _preview_timer():
    """
    Timer function for periodic preview updates.
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
                )
                
                if props.preview != preview:
                    props["preview"] = preview
    except Exception:
        pass
    
    return 5.0


_timer_registered = False


# ============================================================================
# Registration
# ============================================================================

def register():
    """Register handlers."""
    global _timer_registered
    
    if on_render_init not in bpy.app.handlers.render_init:
        bpy.app.handlers.render_init.append(on_render_init)
    
    if on_render_complete not in bpy.app.handlers.render_complete:
        bpy.app.handlers.render_complete.append(on_render_complete)
    
    if on_render_cancel not in bpy.app.handlers.render_cancel:
        bpy.app.handlers.render_cancel.append(on_render_cancel)
    
    if on_load_post not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(on_load_post)
    
    if not _timer_registered:
        bpy.app.timers.register(_preview_timer, first_interval=1.0)
        _timer_registered = True


def unregister():
    """Unregister handlers."""
    global _timer_registered
    
    if on_render_init in bpy.app.handlers.render_init:
        bpy.app.handlers.render_init.remove(on_render_init)
    
    if on_render_complete in bpy.app.handlers.render_complete:
        bpy.app.handlers.render_complete.remove(on_render_complete)
    
    if on_render_cancel in bpy.app.handlers.render_cancel:
        bpy.app.handlers.render_cancel.remove(on_render_cancel)
    
    if on_load_post in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(on_load_post)
    
    if _timer_registered:
        if bpy.app.timers.is_registered(_preview_timer):
            bpy.app.timers.unregister(_preview_timer)
        _timer_registered = False
