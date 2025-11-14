# Raytracing Series
The Raytracing Series (Python version)

## Running the Code

### Basic Usage
To generate a PPM image:

```bash
python3 main.py > output.ppm
```

### Live Preview with Hot Reload
For real-time visualization while developing:

```bash
python3 live_preview.py main.py
```

This opens a window that:
- Displays your rendered image immediately
- Automatically updates when you save changes to `main.py`
- Shows the timestamp of the last update
- Displays any errors if the PPM generation fails

## Requirements

For live preview functionality:
```bash
pip install pillow watchdog
```

## File Structure
- `main.py` - Your raytracer that outputs PPM format to stdout
- `live_preview.py` - The hot-reload viewer tool
- `output.ppm` - Generated PPM image file (optional)

## Development Workflow
1. Run the live preview: `python3 live_preview.py main.py`
2. Edit your raytracer code in `main.py`
3. Save the file - the preview updates automatically
4. Iterate quickly with instant visual feedback