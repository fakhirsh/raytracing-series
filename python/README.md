# Raytracing Series
The Raytracing Series (Python version)

## Running the Code

### Basic Usage
To generate a PPM image:

```bash
python3 src/main.py > image.ppm
```

### Live Preview
To watch a PPM file and see updates in real-time:

```bash
python3 src/watch_ppm.py
```

This defaults to watching `image.ppm`. You can specify a different file and a maximum width:

```bash
python3 src/watch_ppm.py --input image.ppm --max-width 800 --interval 200
```
