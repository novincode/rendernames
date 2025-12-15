# ============================================================================
# RenderNames - Panels
# ============================================================================
# UI Panel definitions - appears in Output Properties
# Clean, Blender-native look with progressive disclosure

import os

import bpy
from bpy.types import Panel

from . import template_engine


# ============================================================================
# Main Panel
# ============================================================================

class RENDERNAMES_PT_main(Panel):
    """Main RenderNames panel in Output Properties"""
    bl_idname = "RENDERNAMES_PT_main"
    bl_label = "RenderNames"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "output"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        props = context.scene.rendernames
        self.layout.prop(props, "enabled", text="")
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.rendernames
        
        # Disable UI if not enabled
        layout.active = props.enabled
        
        # Template Input
        col = layout.column(align=True)
        col.label(text="Template:", icon="TEXT")
        
        row = col.row(align=True)
        row.prop(props, "template", text="")
        row.menu("RENDERNAMES_MT_variable_menu", text="", icon="ADD")
        row.operator("rendernames.reset_template", text="", icon="LOOP_BACK")
        
        # Base Path Section
        col.separator()
        
        box = col.box()
        row = box.row()
        row.prop(props, "use_base_path", text="Custom Base Path")
        
        if props.use_base_path:
            sub = box.row()
            sub.prop(props, "base_path", text="")
        else:
            sub = box.row()
            sub.enabled = False
            sub.scale_y = 0.8
            sub.label(text="Using Blender's output path", icon="INFO")
        
        # Live Preview
        col.separator()
        
        box = col.box()
        box.scale_y = 1.0
        
        # Calculate preview
        if props.template:
            # Get base path for preview
            if props.use_base_path and props.base_path:
                base = props.base_path
            else:
                existing = scene.render.filepath
                if existing:
                    base = os.path.dirname(existing) or "//"
                else:
                    base = "//"
            
            rendered = template_engine.render_template(
                props.template,
                scene,
                props,
            )
            
            # Combine for full preview
            if base.endswith("/"):
                preview = base + rendered
            else:
                preview = base + "/" + rendered
        else:
            preview = "(empty template)"
        
        # Show full preview with expandable row
        row = box.row(align=True)
        row.label(text="", icon="FORWARD")
        row.label(text=preview)  # Full path without truncation
        row.operator("rendernames.copy_preview", text="", icon="COPYDOWN")


# ============================================================================
# Options Sub-Panel
# ============================================================================

class RENDERNAMES_PT_options(Panel):
    """Options panel for folder organization and naming"""
    bl_idname = "RENDERNAMES_PT_options"
    bl_label = "Options"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "output"
    bl_parent_id = "RENDERNAMES_PT_main"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.rendernames
        
        layout.active = props.enabled
        
        # Folder Organization
        col = layout.column()
        col.label(text="Folder Structure:", icon="FILE_FOLDER")
        
        flow = col.column_flow(columns=2, align=True)
        flow.prop(props, "use_blend_root", text="Blend File Root")
        flow.prop(props, "folder_per_scene", text="Per Scene")
        flow.prop(props, "folder_per_camera", text="Per Camera")
        flow.prop(props, "folder_per_date", text="Per Date")
        
        layout.separator()
        
        # Naming Options
        col = layout.column()
        col.label(text="Naming:", icon="SORTALPHA")
        
        flow = col.column_flow(columns=2, align=True)
        flow.prop(props, "sanitize_names", text="Sanitize Names")
        flow.prop(props, "lowercase", text="Lowercase")
        
        row = col.row(align=True)
        row.prop(props, "frame_padding", text="Frame Padding")


# ============================================================================
# Presets Sub-Panel
# ============================================================================

class RENDERNAMES_PT_presets(Panel):
    """Presets panel for saving and loading configurations"""
    bl_idname = "RENDERNAMES_PT_presets"
    bl_label = "Presets"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "output"
    bl_parent_id = "RENDERNAMES_PT_main"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.rendernames
        
        layout.active = props.enabled
        
        # Quick access row
        row = layout.row(align=True)
        row.menu("RENDERNAMES_MT_presets", text="Load Preset", icon="PRESET")
        
        layout.separator()
        
        # Save new preset
        col = layout.column(align=True)
        col.label(text="Save Current Settings:", icon="ADD")
        
        row = col.row(align=True)
        row.prop(props, "preset_name", text="")
        row.operator("rendernames.save_preset", text="Save")
        
        layout.separator()
        
        # Import/Export
        row = layout.row(align=True)
        row.operator("rendernames.import_preset", text="Import", icon="IMPORT")
        row.operator("rendernames.export_preset", text="Export", icon="EXPORT")


# ============================================================================
# Variables Reference Sub-Panel
# ============================================================================

class RENDERNAMES_PT_variables(Panel):
    """Quick reference for available template variables"""
    bl_idname = "RENDERNAMES_PT_variables"
    bl_label = "Variables Reference"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "output"
    bl_parent_id = "RENDERNAMES_PT_main"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.rendernames
        
        layout.active = props.enabled
        
        # Compact variable reference
        descriptions = template_engine.get_variable_descriptions()
        
        # Group by category for cleaner display
        categories = {
            "Scene": ["scene", "blend_file"],
            "Frame": ["frame", "frame_start", "frame_end", "frame_range"],
            "Time": ["date", "time", "datetime"],
            "Camera": ["camera"],
            "Resolution": ["resolution"],
            "Render": ["fps", "format", "engine", "samples"],
        }
        
        for category, var_names in categories.items():
            box = layout.box()
            box.scale_y = 0.7
            
            col = box.column(align=True)
            col.label(text=f"{category}:", icon="DOT")
            
            for name in var_names:
                if name in descriptions:
                    # Use split to properly align variable and description
                    split = col.split(factor=0.4, align=True)
                    
                    # Variable syntax (clickable - copies to clipboard)
                    op = split.operator(
                        "rendernames.copy_variable",
                        text=f"{{{{{name}}}}}",
                        emboss=False,
                    )
                    op.variable = name
                    
                    # Description - takes remaining space
                    split.label(text=descriptions[name])


# ============================================================================
# Render Output Integration Notice
# ============================================================================

class RENDERNAMES_PT_render_output_notice(Panel):
    """Small notice panel in the standard Output section"""
    bl_idname = "RENDERNAMES_PT_render_output_notice"
    bl_label = ""
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "output"
    bl_options = {"HIDE_HEADER"}
    bl_order = 0  # Try to appear near the top
    
    @classmethod
    def poll(cls, context):
        # Only show if RenderNames is enabled
        return hasattr(context.scene, "rendernames") and context.scene.rendernames.enabled
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.rendernames
        
        if props.enabled:
            box = layout.box()
            box.scale_y = 0.7
            
            row = box.row()
            row.alert = False
            row.label(
                text="Output path managed by RenderNames",
                icon="INFO",
            )
            
            sub = row.row()
            sub.alignment = "RIGHT"
            sub.operator(
                "rendernames.apply_to_render",
                text="Apply",
                icon="CHECKMARK",
            )


# ============================================================================
# Registration
# ============================================================================

_classes = (
    RENDERNAMES_PT_main,
    RENDERNAMES_PT_options,
    RENDERNAMES_PT_presets,
    RENDERNAMES_PT_variables,
    RENDERNAMES_PT_render_output_notice,
)


def register():
    """Register panel classes."""
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister panel classes."""
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
