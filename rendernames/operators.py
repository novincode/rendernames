# ============================================================================
# RenderNames - Operators
# ============================================================================
# All Blender operators for the extension
# Handles preset management, variable insertion, and template actions

import os
import json
from typing import Set

import bpy
from bpy.types import Operator
from bpy.props import StringProperty, EnumProperty

from . import template_engine
from . import presets


# ============================================================================
# Variable Insertion
# ============================================================================

class RENDERNAMES_OT_insert_variable(Operator):
    """Insert a template variable at cursor position"""
    bl_idname = "rendernames.insert_variable"
    bl_label = "Insert Variable"
    bl_options = {"REGISTER", "UNDO"}
    
    variable: StringProperty(
        name="Variable",
        description="Variable name to insert",
    )
    
    def execute(self, context):
        props = context.scene.rendernames
        
        # Insert the variable wrapped in braces
        var_text = f"{{{{{self.variable}}}}}"
        
        # Append to template (could be smarter with cursor position)
        if props.template and not props.template.endswith("/"):
            props.template += "_"
        props.template += var_text
        
        return {"FINISHED"}


class RENDERNAMES_OT_copy_variable(Operator):
    """Copy a template variable syntax to clipboard"""
    bl_idname = "rendernames.copy_variable"
    bl_label = "Copy Variable"
    bl_options = {"REGISTER"}
    
    variable: StringProperty(
        name="Variable",
        description="Variable name to copy",
    )
    
    def execute(self, context):
        var_text = f"{{{{{self.variable}}}}}"
        context.window_manager.clipboard = var_text
        self.report({"INFO"}, f"Copied {var_text} to clipboard")
        return {"FINISHED"}


class RENDERNAMES_OT_variable_menu(Operator):
    """Show menu of available template variables"""
    bl_idname = "rendernames.variable_menu"
    bl_label = "Variables"
    bl_options = {"REGISTER"}
    
    def execute(self, context):
        return {"FINISHED"}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=500)
    
    def draw(self, context):
        layout = self.layout
        
        descriptions = template_engine.get_variable_descriptions()
        
        # Group variables by category
        categories = {
            "Scene & Project": ["scene", "blend_file"],
            "Frame": ["frame", "frame_start", "frame_end", "frame_range"],
            "Date & Time": ["date", "time", "datetime", "year", "month", "day"],
            "Camera": ["camera"],
            "Resolution": ["resolution", "width", "height", "percent"],
            "Render": ["fps", "format", "engine", "samples"],
        }
        
        for category, vars in categories.items():
            box = layout.box()
            box.label(text=category, icon="DOT")
            
            for var_name in vars:
                if var_name in descriptions:
                    row = box.row(align=True)
                    
                    # Variable button - fixed width
                    split = row.split(factor=0.35)
                    op = split.operator(
                        "rendernames.insert_variable",
                        text=f"{{{{{var_name}}}}}",
                    )
                    op.variable = var_name
                    
                    # Description - takes remaining space
                    split.label(text=descriptions[var_name])


# ============================================================================
# Template Actions
# ============================================================================

class RENDERNAMES_OT_reset_template(Operator):
    """Reset template to default"""
    bl_idname = "rendernames.reset_template"
    bl_label = "Reset Template"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        props = context.scene.rendernames
        props.template = "{{scene}}_"
        self.report({"INFO"}, "Template reset to default")
        return {"FINISHED"}


class RENDERNAMES_OT_clear_template(Operator):
    """Clear the template"""
    bl_idname = "rendernames.clear_template"
    bl_label = "Clear Template"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        props = context.scene.rendernames
        props.template = ""
        return {"FINISHED"}


class RENDERNAMES_OT_copy_preview(Operator):
    """Copy the preview path to clipboard"""
    bl_idname = "rendernames.copy_preview"
    bl_label = "Copy Preview Path"
    
    def execute(self, context):
        props = context.scene.rendernames
        context.window_manager.clipboard = props.preview
        self.report({"INFO"}, "Path copied to clipboard")
        return {"FINISHED"}


class RENDERNAMES_OT_apply_to_render(Operator):
    """Apply the template to Blender's render output path"""
    bl_idname = "rendernames.apply_to_render"
    bl_label = "Apply to Render Settings"
    bl_options = {"REGISTER", "UNDO"}
    
    def execute(self, context):
        scene = context.scene
        props = scene.rendernames
        
        if not props.enabled:
            self.report({"WARNING"}, "RenderNames is disabled")
            return {"CANCELLED"}
        
        # Get the rendered path
        rendered = template_engine.render_template(
            props.template,
            scene,
            props,
        )
        
        # Apply to render settings
        scene.render.filepath = f"//renders/{rendered}"
        
        self.report({"INFO"}, f"Render path set to: {rendered}")
        return {"FINISHED"}


# ============================================================================
# Preset Management
# ============================================================================

class RENDERNAMES_OT_save_preset(Operator):
    """Save current settings as a preset"""
    bl_idname = "rendernames.save_preset"
    bl_label = "Save Preset"
    bl_options = {"REGISTER"}
    
    preset_name: StringProperty(
        name="Preset Name",
        description="Name for this preset",
        default="",
    )
    
    def execute(self, context):
        props = context.scene.rendernames
        
        name = self.preset_name or props.preset_name
        if not name:
            self.report({"ERROR"}, "Please enter a preset name")
            return {"CANCELLED"}
        
        # Save the preset
        preset_data = presets.extract_preset_data(props)
        presets.save_preset(name, preset_data)
        
        # Update the presets list
        presets.refresh_preset_list(props)
        
        # Clear the name field
        props.preset_name = ""
        
        self.report({"INFO"}, f"Preset '{name}' saved")
        return {"FINISHED"}
    
    def invoke(self, context, event):
        props = context.scene.rendernames
        self.preset_name = props.preset_name
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "preset_name", text="Name")


class RENDERNAMES_OT_load_preset(Operator):
    """Load a preset"""
    bl_idname = "rendernames.load_preset"
    bl_label = "Load Preset"
    bl_options = {"REGISTER", "UNDO"}
    
    preset_name: StringProperty(
        name="Preset Name",
        description="Name of preset to load",
    )
    
    def execute(self, context):
        props = context.scene.rendernames
        
        if not self.preset_name:
            self.report({"ERROR"}, "No preset selected")
            return {"CANCELLED"}
        
        # Load the preset
        preset_data = presets.load_preset(self.preset_name)
        if preset_data is None:
            self.report({"ERROR"}, f"Preset '{self.preset_name}' not found")
            return {"CANCELLED"}
        
        # Apply to current properties
        presets.apply_preset_data(props, preset_data)
        
        self.report({"INFO"}, f"Preset '{self.preset_name}' loaded")
        return {"FINISHED"}


class RENDERNAMES_OT_delete_preset(Operator):
    """Delete a preset"""
    bl_idname = "rendernames.delete_preset"
    bl_label = "Delete Preset"
    bl_options = {"REGISTER"}
    
    preset_name: StringProperty(
        name="Preset Name",
        description="Name of preset to delete",
    )
    
    def execute(self, context):
        props = context.scene.rendernames
        
        if not self.preset_name:
            self.report({"ERROR"}, "No preset selected")
            return {"CANCELLED"}
        
        # Delete the preset
        success = presets.delete_preset(self.preset_name)
        if not success:
            self.report({"ERROR"}, f"Could not delete preset '{self.preset_name}'")
            return {"CANCELLED"}
        
        # Refresh the list
        presets.refresh_preset_list(props)
        
        self.report({"INFO"}, f"Preset '{self.preset_name}' deleted")
        return {"FINISHED"}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class RENDERNAMES_OT_refresh_presets(Operator):
    """Refresh the presets list"""
    bl_idname = "rendernames.refresh_presets"
    bl_label = "Refresh Presets"
    
    def execute(self, context):
        props = context.scene.rendernames
        presets.refresh_preset_list(props)
        return {"FINISHED"}


class RENDERNAMES_OT_import_preset(Operator):
    """Import a preset from file"""
    bl_idname = "rendernames.import_preset"
    bl_label = "Import Preset"
    bl_options = {"REGISTER"}
    
    filepath: StringProperty(
        subtype="FILE_PATH",
    )
    
    filter_glob: StringProperty(
        default="*.json",
        options={"HIDDEN"},
    )
    
    def execute(self, context):
        props = context.scene.rendernames
        
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                preset_data = json.load(f)
            
            # Get name from file
            name = os.path.splitext(os.path.basename(self.filepath))[0]
            
            # Save to presets folder
            presets.save_preset(name, preset_data)
            presets.refresh_preset_list(props)
            
            self.report({"INFO"}, f"Imported preset '{name}'")
            return {"FINISHED"}
            
        except Exception as e:
            self.report({"ERROR"}, f"Failed to import: {e}")
            return {"CANCELLED"}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


class RENDERNAMES_OT_export_preset(Operator):
    """Export current settings to a file"""
    bl_idname = "rendernames.export_preset"
    bl_label = "Export Preset"
    bl_options = {"REGISTER"}
    
    filepath: StringProperty(
        subtype="FILE_PATH",
    )
    
    filter_glob: StringProperty(
        default="*.json",
        options={"HIDDEN"},
    )
    
    def execute(self, context):
        props = context.scene.rendernames
        
        try:
            # Ensure .json extension
            filepath = self.filepath
            if not filepath.endswith(".json"):
                filepath += ".json"
            
            preset_data = presets.extract_preset_data(props)
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(preset_data, f, indent=2)
            
            self.report({"INFO"}, f"Exported to {filepath}")
            return {"FINISHED"}
            
        except Exception as e:
            self.report({"ERROR"}, f"Failed to export: {e}")
            return {"CANCELLED"}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


# ============================================================================
# Preset Menu
# ============================================================================

class RENDERNAMES_MT_presets(bpy.types.Menu):
    """Presets menu"""
    bl_idname = "RENDERNAMES_MT_presets"
    bl_label = "Presets"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.rendernames
        
        # Built-in presets
        layout.label(text="Built-in Presets", icon="PRESET")
        
        for name in presets.BUILTIN_PRESETS:
            op = layout.operator(
                "rendernames.load_preset",
                text=name.replace("_", " ").title(),
            )
            op.preset_name = f"__builtin__{name}"
        
        layout.separator()
        
        # User presets
        user_presets = presets.list_presets()
        if user_presets:
            layout.label(text="User Presets", icon="USER")
            for name in user_presets:
                row = layout.row()
                op = row.operator("rendernames.load_preset", text=name)
                op.preset_name = name
        else:
            layout.label(text="No user presets", icon="INFO")
        
        layout.separator()
        
        # Management options
        layout.operator("rendernames.save_preset", icon="ADD")
        layout.operator("rendernames.import_preset", icon="IMPORT")
        layout.operator("rendernames.export_preset", icon="EXPORT")


# ============================================================================
# Registration
# ============================================================================

_classes = (
    RENDERNAMES_OT_insert_variable,
    RENDERNAMES_OT_copy_variable,
    RENDERNAMES_OT_variable_menu,
    RENDERNAMES_OT_reset_template,
    RENDERNAMES_OT_clear_template,
    RENDERNAMES_OT_copy_preview,
    RENDERNAMES_OT_apply_to_render,
    RENDERNAMES_OT_save_preset,
    RENDERNAMES_OT_load_preset,
    RENDERNAMES_OT_delete_preset,
    RENDERNAMES_OT_refresh_presets,
    RENDERNAMES_OT_import_preset,
    RENDERNAMES_OT_export_preset,
    RENDERNAMES_MT_presets,
)


def register():
    """Register operator classes."""
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister operator classes."""
    for cls in reversed(_classes):
        bpy.utils.unregister_class(cls)
