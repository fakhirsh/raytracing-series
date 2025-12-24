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

## Performance Profiling

The code includes built-in cProfile instrumentation to analyze performance bottlenecks.

### Running the Profiler

When you run the main script, profiling data is automatically collected:

```bash
python3 src/main.py > image.ppm
```

This will:
- Generate the rendered image (`image.ppm`)
- Save profiling data to `profile_output.prof`
- Print top 30 functions by cumulative time and total time to console

### Visualizing Profile Data

#### Option 1: SnakeViz (Recommended - Interactive Browser Visualization)

Install and visualize with interactive sunburst/icicle charts:

```bash
pip install snakeviz
snakeviz profile_output.prof
```

Features:
- Interactive sunburst chart showing call hierarchy
- Icicle chart with rectangular blocks for time distribution
- Hover to see detailed timing information
- Click to drill down into specific function calls

### Understanding Profile Output

Key metrics to focus on:
- **tottime**: Time spent in the function itself (excluding subfunctions)
- **cumtime**: Total time spent in the function and all functions it calls
- **ncalls**: Number of times the function was called

Common bottlenecks in raytracers:
- Ray-sphere intersection tests
- Material scatter calculations
- Random number generation
- Vector math operations (dot product, normalization, etc.)
