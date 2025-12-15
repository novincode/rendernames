# RenderNames Development

## Quick Start

### Installation for Development

1. Clone this repo
2. Symlink the `rendernames` folder to Blender's addons directory:

**macOS:**
```bash
ln -s /path/to/rendernames/rendernames ~/Library/Application\ Support/Blender/4.2/extensions/user_default/rendernames
```

**Linux:**
```bash
ln -s /path/to/rendernames/rendernames ~/.config/blender/4.2/extensions/user_default/rendernames
```

**Windows (PowerShell as Admin):**
```powershell
New-Item -ItemType SymbolicLink -Path "$env:APPDATA\Blender Foundation\Blender\4.2\extensions\user_default\rendernames" -Target "C:\path\to\rendernames\rendernames"
```

3. Enable in Blender: Edit → Preferences → Add-ons → Search "RenderNames"

### Building for Distribution

```bash
./scripts/build.sh
```

This creates `dist/rendernames-X.X.X.zip` ready for installation.

### Testing in Blender

```bash
# Open Blender with extension enabled
blender --python-expr "import bpy; bpy.ops.preferences.addon_enable(module='rendernames')"
```

## Project Structure

```
rendernames/
├── rendernames/           # Extension source (distributable)
│   ├── blender_manifest.toml
│   ├── __init__.py
│   ├── properties.py
│   ├── operators.py
│   ├── panels.py
│   ├── handlers.py
│   ├── template_engine.py
│   └── presets.py
├── docs/                  # Documentation
│   ├── architecture.md
│   ├── variables.md
│   └── vision.md
├── scripts/               # Development scripts
│   └── build.sh
├── README.md
├── DEVELOPMENT.md         # This file
├── LICENSE
└── .gitignore
```

## Code Style

- **PEP 8** for Python
- **Type hints** where helpful (not required)
- **Docstrings** for public functions
- **Comments** for non-obvious logic

## Testing Checklist

Before release:

- [ ] Enable/disable extension
- [ ] Test default template
- [ ] Test each template variable
- [ ] Test checkbox options
- [ ] Test sanitization
- [ ] Test lowercase option
- [ ] Test frame padding
- [ ] Save/load user preset
- [ ] Load built-in presets
- [ ] Import/export preset
- [ ] Delete preset
- [ ] Render still image
- [ ] Render animation
- [ ] Test with unsaved blend file
- [ ] Test folder creation
- [ ] Test overwrite scenario
- [ ] Verify settings persist after restart
- [ ] Test on Blender 4.2
- [ ] Test on Blender 5.0+

## Release Process

1. Update version in `rendernames/blender_manifest.toml`
2. Update changelog in `README.md`
3. Run `./scripts/build.sh`
4. Test the built zip in fresh Blender
5. Create GitHub release with zip attached
6. Submit to Blender Extensions platform (optional)

## Architecture Notes

### Why single-level modules?

We chose flat module structure over nested folders because:
- Total codebase is ~600 LOC
- Easier to navigate
- Fewer import issues
- Simpler for contributors

### Why Scene properties vs Addon preferences?

Scene properties:
- Persist with .blend file
- Different per-project settings
- Travel with the file

Addon preferences:
- Global to Blender installation
- Same across all projects

We chose Scene because render naming should be project-specific.

### Why not use bl_info?

Blender 4.2+ introduced the extension system with `blender_manifest.toml`.
This is the modern way and required for the Extensions platform.

## Common Issues

### "No module named 'rendernames'"
- Make sure the folder structure is correct
- The `blender_manifest.toml` must be inside `rendernames/`

### Properties not saving
- Check if the .blend file is saved
- Scene properties only persist with saved files

### Preview not updating
- Check console for errors
- Timer might have crashed - try disabling/enabling

## Contributing

1. Fork the repo
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit PR

Keep PRs focused and small when possible.
