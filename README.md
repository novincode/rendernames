# RenderNames

**Smart render output naming for Blender that actually makes sense.**

Stop manually renaming files. Stop creating folders. Stop losing track of which render is which.

RenderNames gives you **template-based file naming** with live preview, automatic folder organization, and preset management—built right into Blender's Output Properties panel.

---

## Why This Exists

Blender's render output? It's just a text field. No variables, no organization, no help.

You end up with:
- `untitled.png`, `untitled0001.png`, `final_final_ACTUAL.png`
- Manual folder creation for every project
- No consistency across scenes or cameras
- Constant fear of overwriting your best render

**RenderNames fixes this.** One template, infinite possibilities.

```
{{blend_file}}/{{date}}/{{scene}}_{{camera}}_
→ my_project/2025-01-15/Scene_Camera_0001.png
```

That's it. You set it once, render forever.

---

## Features

### 🎯 Template System
Use variables like `{{scene}}`, `{{camera}}`, `{{date}}`, `{{resolution}}` and more. Mix and match however you want.

### 👁️ Live Preview
See your output path **as you type**. No surprises at render time.

### 📁 Auto Organization
Enable folder options and RenderNames creates the structure for you—per scene, per camera, per date, whatever you need.

### 💾 Preset System
Save your favorite setups. Load them instantly. Export and share with your team or across projects.

### 🔧 Blender Native
Lives in Output Properties where it belongs. Works with **Blender 4.2+** and **Blender 5.0+**. No weird UI, no external apps.

### ⚡ Non-Destructive
Enable it when you want it. Disable it when you don't. Your settings stay saved either way.

---

## Installation

### From Releases (recommended)
1. Download the latest `.zip` from [Releases](https://github.com/novincode/rendernames/releases)
2. In Blender: `Edit → Preferences → Extensions → Install from Disk`
3. Select the zip, enable the extension
4. Done.

### Full Installation Guide
See [docs/INSTALL.md](docs/INSTALL.md) for detailed setup, troubleshooting, and developer instructions.

---

## Quick Start

1. Open **Output Properties** (printer icon in properties panel)
2. Find the **RenderNames** section
3. Click the **Enable** checkbox
4. Edit the template or pick a preset
5. Hit render—your files land exactly where the preview says

---

## Template Variables

Every variable gets replaced when you render:

| Variable | What It Does | Example Output |
|----------|-------------|----------------|
| `{{scene}}` | Current scene name | `Scene` |
| `{{blend_file}}` | Your .blend filename | `my_project` |
| `{{camera}}` | Active camera | `Camera.001` |
| `{{date}}` | Today's date | `2025-01-15` |
| `{{time}}` | Current time | `14-30-45` |
| `{{datetime}}` | Date + time | `2025-01-15_14-30-45` |
| `{{resolution}}` | Render resolution | `1920x1080` |
| `{{fps}}` | Frame rate | `24` |
| `{{format}}` | Output format | `png` |
| `{{engine}}` | Render engine | `cycles` |
| `{{samples}}` | Sample count | `128` |
| `{{frame_start}}` | First frame | `0001` |
| `{{frame_end}}` | Last frame | `0250` |
| `{{frame_range}}` | Frame range | `0001-0250` |

**Note on animations**: Blender automatically adds frame numbers (`0001`, `0002`, etc.) to the end of your filename. For videos, use `{{frame_range}}` to get the full range in the filename.

---

## Example Templates

**Simple** (no folders):
```
{{scene}}_
→ Scene_0001.png, Scene_0002.png, ...
```

**Professional** (organized):
```
{{blend_file}}/{{date}}/{{scene}}_{{camera}}_
→ my_project/2025-01-15/Scene_Camera_0001.exr
```

**Archival** (timestamped):
```
renders/{{datetime}}/{{scene}}_
→ renders/2025-01-15_14-30-45/Scene_0001.png
```

**By Camera**:
```
{{camera}}/{{scene}}_
→ Camera.001/Scene_0001.png
```

**Video with Frame Range**:
```
{{scene}}_{{frame_range}}
→ Scene_0001-0250.mkv
```

Mix them however you want. The preview shows you exactly what you'll get.

---

## Built-in Presets

RenderNames comes with templates ready to use:

- **Simple** — Just scene name, no folders
- **Professional** — Full organization with date and camera folders
- **Archival** — Timestamped for version control
- **By Camera** — Organizes renders by camera name
- **Minimal** — Bare minimum naming

### Custom Presets

Save your own:
1. Set up your template and options
2. Click "Save Preset"
3. Give it a name
4. Load it anytime from the dropdown

You can also **export presets as JSON files** and share them with teammates or use them across projects.

---

## Options

### Folder Organization
- **Blend File Root** — Use your .blend filename as the base folder
- **Per Scene** — Subfolder for each scene
- **Per Camera** — Subfolder for each camera
- **Per Date** — Subfolder for each render date

### Naming
- **Sanitize Names** — Replace weird characters with underscores
- **Lowercase** — Convert everything to lowercase
- **Frame Padding** — How many digits for frame numbers (1-8)

Everything updates the live preview so you know what you're getting.

---

## Compatibility

- ✅ **Blender 4.2+** — Full support
- ✅ **Blender 5.0+** — Tested and working
- ❌ **Blender 4.1 and earlier** — Not supported (requires extension system)

---

## Documentation

- **[Installation Guide](docs/INSTALL.md)** — Detailed install instructions for users and developers
- **[Changelog](CHANGELOG.md)** — Version history and updates
- **[Architecture](docs/architecture.md)** — Technical documentation for contributors
- **[Vision](docs/vision.md)** — Design philosophy and goals

---

## Development

Want to contribute or build from source?

```bash
# Clone the repo
git clone https://github.com/novincode/rendernames.git
cd rendernames

# Build the extension
python3 scripts/build.py

# Release
python3 scripts/release.py patch
```

Check out the [Installation Guide](docs/INSTALL.md) for developer setup details.

---

## Support & Contributing

Found a bug? Want a feature?

- 🐛 **Bug reports**: [GitHub Issues](https://github.com/novincode/rendernames/issues)
- 💡 **Feature requests**: [GitHub Discussions](https://github.com/novincode/rendernames/discussions)
- 🤝 **Pull requests**: Always welcome

If this saves you time, **give it a star ⭐** — it helps others find it.

---

## License

GPL-3.0-or-later — Same license as Blender.

---

**Made by humans who got tired of manually naming render files.**
