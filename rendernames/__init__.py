# ============================================================================
# RenderNames - Smart Render Naming for Blender
# ============================================================================
# Entry point for the extension
# Handles registration of all modules and handlers

"""
RenderNames - Template-based render naming system for Blender.

This extension provides:
- Template variables ({{scene}}, {{camera}}, {{date}}, etc.)
- Automatic folder organization
- Preset system for saving/loading configurations
- Live preview of render output paths
- Full sync with Blender's native render settings
"""

from . import properties
from . import operators
from . import panels
from . import handlers


# ============================================================================
# Registration
# ============================================================================

def register():
    """Register all extension components."""
    properties.register()
    operators.register()
    panels.register()
    handlers.register()


def unregister():
    """Unregister all extension components."""
    handlers.unregister()
    panels.unregister()
    operators.unregister()
    properties.unregister()
