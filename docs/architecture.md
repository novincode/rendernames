# RenderNames - Architecture

## Overview

RenderNames is a Blender extension that provides template-based render output naming. It's designed to be:

- **Simple**: Clean UI, progressive disclosure
- **Powerful**: Full template system with many variables
- **Blender-native**: Follows all extension guidelines
- **Scalable**: Modular architecture for future features

## Project Structure

```
repo_root/
├── README.md                    # User documentation
├── .gitignore                   # Git ignore patterns
├── docs/
│   ├── architecture.md          # This file
│   └── variables.md             # Template variable reference
└── rendernames/                 # The actual extension (distributable)
    ├── blender_manifest.toml    # Extension manifest (replaces bl_info)
    ├── __init__.py              # Entry point, registration
    ├── properties.py            # All PropertyGroups
    ├── operators.py             # All Operators and Menus
    ├── panels.py                # All UI Panels
    ├── handlers.py              # Blender event handlers
    ├── template_engine.py       # Core template logic
    └── presets.py               # Preset management
```

## Module Responsibilities

### `__init__.py`
- Extension entry point
- Registers/unregisters all modules in correct order
- No logic - just orchestration

### `properties.py`
- Defines `RENDERNAMES_Properties` PropertyGroup
- Attached to `bpy.types.Scene` (persists with .blend file)
- All settings stored here
- Update callbacks for live preview

### `operators.py`
- All user-triggerable actions
- Insert variable, save/load/delete presets
- Import/export functionality
- Menu definitions

### `panels.py`
- UI layout in Output Properties
- Main panel with template editor
- Sub-panels for options, presets, variable reference
- Notice panel showing RenderNames is active

### `handlers.py`
- `render_init`: Applies template before render
- `render_complete`: Optional logging
- `load_post`: Refreshes preset list
- Timer for periodic preview updates

### `template_engine.py`
- Variable definitions (name → resolver function)
- Template parsing with regex
- String sanitization
- Path validation

### `presets.py`
- Built-in preset definitions
- JSON save/load to user directory
- Uses `bpy.utils.extension_path_user()` for storage
- CRUD operations for user presets

## Data Flow

```
User Input (Template)
        ↓
   properties.py (stores template string)
        ↓
   template_engine.py (parses {{variables}})
        ↓
   Preview shown in panels.py
        ↓
   User clicks Render
        ↓
   handlers.py (render_init intercepts)
        ↓
   template_engine.py (renders final path)
        ↓
   Sets scene.render.filepath
        ↓
   Creates directories if needed
        ↓
   Blender renders to new path
```

## Settings Persistence

### Per-Project (in .blend file)
All properties in `RENDERNAMES_Properties` are stored with the scene:
- Template string
- Organization checkboxes
- Naming options
- Enabled state

This means:
- Settings survive Blender restarts
- Different projects can have different settings
- Settings travel with the .blend file

### Global (in user directory)
User presets are stored in:
```
{extension_path_user}/presets/*.json
```

This path is determined by `bpy.utils.extension_path_user(__package__)`, which:
- Persists across extension upgrades
- Is removed when extension is uninstalled
- Is user-writable on all systems

## Version Compatibility

### Blender 4.2+
- Full support via extension system
- Uses `blender_manifest.toml`
- Modern handler API

### Blender 5.0+
- Same as 4.2
- No known breaking changes yet

### Future Compatibility
- Version checks in `template_engine.py` for API differences
- Graceful fallbacks for missing features

## Extension Guidelines Compliance

✅ Uses `__package__` for all identifiers
✅ Relative imports only
✅ No external dependencies (pure Python)
✅ Uses `extension_path_user()` for storage
✅ Requests `files` permission for folder creation
✅ Proper `register()` / `unregister()` cleanup
✅ No modifications to other addons
✅ GPL-3.0-or-later license

## UI Philosophy

### Progressive Disclosure
- Main panel shows template + preview (most common use)
- Options collapsed by default
- Variables reference collapsed
- Advanced features in menus/subpanels

### Blender-Native Look
- Standard panel layouts
- Uses built-in icons
- Follows Blender's UI patterns
- No custom drawing (no `draw_handler`)

### Non-Destructive
- Enable/disable without losing settings
- Original render path can be restored
- Presets don't overwrite each other

## Future Extensibility

### Easy to add new variables
Just add to `_get_variables()` in `template_engine.py`:
```python
"new_var": (
    "Description",
    lambda scene, props: "value",
),
```

### Easy to add new presets
Add to `BUILTIN_PRESETS` dict in `presets.py`

### Easy to add new options
Add property to `RENDERNAMES_Properties` in `properties.py`

## Testing

Manual testing checklist:
1. [ ] Enable/disable extension
2. [ ] Edit template, verify preview updates
3. [ ] Test each variable
4. [ ] Save/load/delete preset
5. [ ] Import/export preset
6. [ ] Render still image
7. [ ] Render animation
8. [ ] Test with unsaved blend file
9. [ ] Test folder creation
10. [ ] Verify settings persist after Blender restart
