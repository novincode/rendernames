# RenderNames - Vision

## The Problem

Blender's built-in render output naming is... primitive. You get:
- A single text field for the path
- No variables, no templates
- Manual folder creation
- Constant renaming to avoid overwrites
- No organization system

Every professional studio ends up with either:
1. A mess of randomly named renders
2. Complex Python scripts
3. Third-party pipeline tools

## The Solution

**RenderNames** is a native Blender extension that brings modern file naming to renders.

**One template**: `{{blend_file}}/{{date}}/{{scene}}_{{camera}}_{{frame}}`

**Outputs**: `my_project/2025-01-15/Scene_Camera_0001.png`

That's it. Simple concept, powerful results.

## Design Principles

### 1. Blender-First
- Looks and feels like native Blender
- No custom UI frameworks
- Follows all extension guidelines
- Ready for Blender Extensions platform

### 2. Progressive Disclosure
- Basic use: Template + Preview (visible by default)
- Intermediate: Organization checkboxes (one click away)
- Advanced: Variable reference, presets (collapsed)

Users shouldn't see complexity they don't need.

### 3. Non-Destructive
- Enable/disable with a checkbox
- Settings persist with .blend file
- Blender's default behavior still works
- No permanent changes

### 4. Predictable
- Live preview shows EXACTLY what you'll get
- No surprises at render time
- Variables resolve the same way every time
- Error handling for edge cases

### 5. Shareable
- Presets export as JSON
- Team members can share configurations
- Built-in presets for common workflows

## Target Users

### Freelancers
- Need organization without overhead
- Different settings per project
- Quick to set up, reliable results

### Studios
- Consistent naming across team
- Preset distribution
- Integration with existing pipelines

### Hobbyists
- Simple defaults that "just work"
- No learning curve for basic use
- Grows with their needs

## Success Criteria

1. **Zero-config start**: Enable and render - default template works
2. **30-second mastery**: Basic customization under a minute
3. **No data loss**: Never overwrite unless explicitly configured
4. **Invisible when unused**: Disabled = vanilla Blender behavior
5. **Marketplace ready**: Passes all Blender extension guidelines

## Non-Goals

- Not a full render manager
- Not a batch rendering system
- Not a file browser/organizer
- Not a versioning system (though variables help)
- Not render farm integration

## Future Possibilities

If this core succeeds, potential additions:
- Render layer/pass variables
- Collection-based naming
- Post-render actions (move, copy, notify)
- Thumbnail generation
- Render log/history

But the core must be solid first.

## Philosophy

> Make the simple things simple, and the complex things possible.

Most users just want sensible file names. Give them that.
Power users want full control. Give them that too.
Nobody wants bloat. Keep it lean.
