# Installation Guide - RenderNames

## For End Users

### Blender 4.2 or Later

**Option 1: Download from Releases (Recommended)**

1. Go to [GitHub Releases](https://github.com/novincode/rendernames/releases)
2. Download the latest `rendernames-X.Y.Z.zip` file
3. In Blender:
   - Edit → Preferences
   - Go to **Extensions** tab (left sidebar)
   - Click the download icon to open "Get Extensions"
   - Click the menu icon (⋮) → **Install from Disk**
   - Select the downloaded `.zip` file
   - Enable the extension by toggling the checkbox

**Option 2: From Blender's Extension Platform**

1. In Blender: Edit → Preferences → Extensions
2. Search for "RenderNames"
3. Click Install
4. Enable the extension

### After Installation

1. Go to the **Output Properties** panel (looks like a printer icon on the right)
2. Expand the **RenderNames** section
3. Check the **Enable** checkbox
4. Start using templates!

## For Developers / From Source

### Prerequisites
- Python 3.11+
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/novincode/rendernames.git
cd rendernames

# Optional: Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt
```

### Development Install

**Option 1: Manual Install from Folder**

1. Create a symlink to the `rendernames` folder in Blender's extensions directory:

```bash
# On macOS
ln -s $(pwd)/rendernames ~/Library/Application\ Support/Blender/4.2/extensions/rendernames

# On Linux
mkdir -p ~/.config/blender/4.2/extensions
ln -s $(pwd)/rendernames ~/.config/blender/4.2/extensions/rendernames

# On Windows (run as Administrator)
# Adjust Blender version number as needed
mklink /D "%APPDATA%\Blender Foundation\Blender\4.2\extensions\rendernames" "%cd%\rendernames"
```

2. Restart Blender

**Option 2: Install from ZIP (Testing)**

```bash
# Build a test package
python3 scripts/release.py patch

# This creates: dist/rendernames-X.Y.Z.zip
# Install as described above using "Install from Disk"
```

### Running Tests

```bash
python3 -m pytest tests/
```

### Code Style

```bash
# Format code
python3 -m black rendernames/

# Lint
python3 -m flake8 rendernames/

# Type check
python3 -m mypy rendernames/
```

## Troubleshooting

### Extension doesn't appear in Extensions tab

1. Ensure you're using **Blender 4.2 or later**
2. Check that the `.zip` file name matches the expected format: `rendernames-X.Y.Z.zip`
3. Try restarting Blender
4. Check if other extensions work (to test your Blender installation)

### "Module not found" errors

1. Ensure all Python files in `rendernames/` folder are included
2. Try reinstalling: remove and reinstall the extension
3. Check Blender's system console for detailed errors (Windows → Toggle System Console)

### RenderNames panel doesn't appear in Output Properties

1. Make sure the extension is **enabled** (checkbox next to RenderNames in Extensions)
2. Go to **Output Properties** (printer icon)
3. If still missing, try switching between different scenes
4. Restart Blender if needed

### Preview path doesn't update

1. Edit the template text to trigger update
2. Switch scenes and switch back
3. Reload the extension (disable and enable)

### Renders go to unexpected folder

1. Check if **"Use Custom Base Path"** is enabled
2. If enabled, verify the path is correct
3. Disable **"Use Custom Base Path"** to use Blender's default render folder

## Getting Help

- **Report bugs**: [GitHub Issues](https://github.com/novincode/rendernames/issues)
- **Feature requests**: [GitHub Discussions](https://github.com/novincode/rendernames/discussions)
- **Documentation**: [README.md](README.md) and [docs/architecture.md](docs/architecture.md)

## Uninstallation

1. In Blender: Edit → Preferences → Extensions
2. Find "RenderNames" in the list
3. Click the menu icon (⋮) → **Remove**
4. Restart Blender

All settings are automatically cleaned up. Your render paths will return to Blender's defaults.

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.
