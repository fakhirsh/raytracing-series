# Modulo Arithmetic & Visual Patterns: The Deep Mechanics

Understanding exactly how modulo creates patterns and how to control them precisely.

---

## Lesson 1: Vertical Stripes - The Fundamental Mechanism

**The Core Insight:**
```python
pattern = w % 20
```

This creates vertical stripes because:
- As `w` goes from 0→199, `w % 20` cycles: `0,1,2...18,19,0,1,2...18,19,0...`
- This cycle repeats exactly 10 times across 200 pixels
- **Key**: The value depends ONLY on `w`, not on `h`
- Therefore, every pixel at `w=5` has the same value regardless of `h`
- Result: vertical columns of identical values = vertical stripes

**The Scaling Operation:**
```python
r = (pattern * 255) // 20
```

This maps our cycle to color space:
- `pattern` ranges from 0→19
- `pattern * 255` ranges from 0→4845
- `(pattern * 255) // 20` ranges from 0→242 (not quite 255!)
- This creates a gradient within each stripe: black at left edge, almost-white at right

**Full Control Code:**
```python
WIDTH = 200
HEIGHT = 200
STRIPE_WIDTH = 20  # Control: width of each stripe
GRADIENT = True    # Control: gradient vs solid stripes

print(f"P3\n{WIDTH} {HEIGHT}\n255")

for h in range(HEIGHT):
    for w in range(WIDTH):
        position_in_stripe = w % STRIPE_WIDTH
        
        if GRADIENT:
            # Smooth gradient: map [0, STRIPE_WIDTH) to [0, 255]
            # Note: multiply first to avoid integer truncation
            color = (position_in_stripe * 255) // STRIPE_WIDTH
        else:
            # Solid stripes: threshold at midpoint
            stripe_number = w // STRIPE_WIDTH
            color = (stripe_number % 2) * 255  # Alternating black/white
        
        print(f"{color} 0 0")
```

**Precise Control Parameters:**
- `STRIPE_WIDTH`: pixels per stripe (smaller = more stripes)
- `w % STRIPE_WIDTH`: position within current stripe (0 to STRIPE_WIDTH-1)
- `w // STRIPE_WIDTH`: which stripe number we're in
- Combine both for complex patterns!

---

## Lesson 2: Why Checkerboards Work - The Parity Trick

**The Mechanism:**
```python
checker = (tile_x + tile_y) % 2
```

This creates checkerboards because:
- Moving right: `tile_x` increases by 1, flipping parity
- Moving down: `tile_y` increases by 1, flipping parity
- Moving diagonally: both increase, parity stays same
- This creates the alternating pattern automatically!

**Controlling Checkerboard Patterns:**
```python
WIDTH = 200
HEIGHT = 200

print(f"P3\n{WIDTH} {HEIGHT}\n255")

# Control parameters
TILE_SIZE = 20
PATTERN_TYPE = "diagonal"  # "checker", "diagonal", "brick"

for h in range(HEIGHT):
    for w in range(WIDTH):
        # Which tile are we in?
        tile_x = w // TILE_SIZE
        tile_y = h // TILE_SIZE
        
        # Position within tile (for sub-patterns)
        local_x = w % TILE_SIZE
        local_y = h % TILE_SIZE
        
        if PATTERN_TYPE == "checker":
            # Standard checkerboard
            pattern = (tile_x + tile_y) % 2
            
        elif PATTERN_TYPE == "diagonal":
            # Diagonal stripes using just tile coordinates
            pattern = (tile_x - tile_y) % 3  # 3 colors cycling diagonally
            
        elif PATTERN_TYPE == "brick":
            # Brick pattern: offset every other row
            offset = (tile_y % 2) * (TILE_SIZE // 2)
            adjusted_x = (w + offset) // TILE_SIZE
            pattern = (adjusted_x + tile_y) % 2
        
        # Map pattern to color
        color = (pattern * 255) // (3 if PATTERN_TYPE == "diagonal" else 2)
        print(f"{color} {color} {color}")
```

**Key Insight**: `(a + b) % n` and `(a - b) % n` create different oriented patterns:
- Addition: checkerboard (changes along both axes)
- Subtraction: diagonal stripes (constant along one diagonal)
- Multiplication: creates scaling/stretching effects

---

## Lesson 3: Radial Patternss

Let me break down radial patterns from the ground up, with visual examples and careful explanations.

### Part 1: What IS a Radial Pattern?

A **radial pattern** is any pattern that depends on **distance from a center point**.

Examples in real life:
- Ripples in water when you drop a stone (circles spreading outward)
- Tree rings (circles from the center)
- A target/bullseye
- Sound waves spreading from a speaker

The key idea: **Every point at the same distance from center looks the same.**

### Part 2: Measuring Distance - The Foundation

Let's say our image is 200×200 pixels, and we want the center to be at (100, 100).

For any pixel at position `(w, h)`, we need to know: **"How far is this pixel from the center?"**

#### Step-by-Step Distance Calculation

**Example: Pixel at (150, 130)**

**Step 1: Find the offset from center**
```
dx = w - CENTER_X = 150 - 100 = 50
dy = h - CENTER_Y = 130 - 100 = 30
```

Think of this as: "The pixel is 50 steps to the right, and 30 steps down from center."

**Step 2: Use the Pythagorean theorem**

Remember from geometry: In a right triangle, `a² + b² = c²`

```
      (w, h) = (150, 130)
         •
         |
         | dy = 30
         |
         •─────────• (CENTER_X, CENTER_Y) = (100, 100)
           dx = 50
```

The actual straight-line distance is:
```
distance = √(dx² + dy²)
distance = √(50² + 30²)
distance = √(2500 + 900)
distance = √3400
distance ≈ 58.3 pixels
```

### Part 3: Why Sometimes We Skip the Square Root

Here's where it gets interesting. We have TWO choices:

#### Choice A: Use Actual Distance (with square root)
```python
dist = (dx * dx + dy * dy) ** 0.5
```

#### Choice B: Use Distance Squared (no square root)
```python
dist_squared = dx * dx + dy * dy
```

Let me show you what difference this makes with **concrete numbers**:

#### Example: Three pixels at different distances

| Pixel | dx | dy | Actual Distance | Distance Squared |
|-------|----|----|-----------------|------------------|
| A | 10 | 0 | 10 | 100 |
| B | 20 | 0 | 20 | 400 |
| C | 30 | 0 | 30 | 900 |

**Notice the pattern:**
- Actual distances: 10, 20, 30 (increases by 10 each time)
- Squared distances: 100, 400, 900 (increases by 300, then 500!)

**This is the key insight:**
- **With square root**: Rings are evenly spaced (10 pixels, 10 pixels, 10 pixels...)
- **Without square root**: Rings get wider as you go out (100, 300, 500...)

### Part 4: Creating Rings - The Modulo Step

Once we have a distance (squared or not), we use **modulo to create repeating rings**.

#### Example with ACTUAL distance (evenly spaced rings)

```python
dist = (dx * dx + dy * dy) ** 0.5
ring_number = int(dist) // 20  # Which ring? (each ring is 20 pixels wide)
```

Let's trace through some pixels:

| Pixel Distance | Ring Number (dist // 20) |
|----------------|--------------------------|
| 0-19 | 0 (innermost ring) |
| 20-39 | 1 |
| 40-59 | 2 |
| 60-79 | 3 |
| 80-99 | 4 |

If we want alternating black/white rings:
```python
color = (ring_number % 2) * 255
```

| Ring Number | Ring Number % 2 | Color |
|-------------|-----------------|-------|
| 0 | 0 | Black (0) |
| 1 | 1 | White (255) |
| 2 | 0 | Black (0) |
| 3 | 1 | White (255) |

**Result: Perfect bullseye with evenly-spaced rings!**

### Part 5: The Squared Distance Approach

Now let's use distance SQUARED:

```python
dist_squared = dx * dx + dy * dy
ring_number = dist_squared // 400
```

Why 400? Because we want the first ring to end around distance 20:
- Distance 20 means dist_squared = 20² = 400

Let's see what happens:

| Actual Distance | Dist Squared | Ring Number (// 400) |
|-----------------|--------------|----------------------|
| 0-20 | 0-400 | 0 |
| 20-28 | 400-800 | 1 |
| 28-35 | 800-1200 | 2 |
| 35-40 | 1200-1600 | 3 |

**See the difference?**
- First ring: 20 pixels wide
- Second ring: only 8 pixels wide (28-20)
- Third ring: only 7 pixels wide (35-28)
- Fourth ring: only 5 pixels wide (40-35)

**Rings get THINNER as you go outward!**

Actually, I made an error above. Let me recalculate correctly:

| Actual Distance | Dist Squared | Ring Number (// 400) |
|-----------------|--------------|----------------------|
| 0-20 | 0-400 | 0 |
| 20-28.3 | 400-800 | 1 |
| 28.3-34.6 | 800-1200 | 2 |
| 34.6-40 | 1200-1600 | 3 |
| 40-44.7 | 1600-2000 | 4 |

The rings are getting progressively narrower! This creates a "ripple" effect.

### Part 6: Visual Comparison

Let me create actual code to show both approaches:

#### Approach A: Evenly Spaced Rings
```python
WIDTH = 200
HEIGHT = 200
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

print(f"P3\n{WIDTH} {HEIGHT}\n255")

for h in range(HEIGHT):
    for w in range(WIDTH):
        dx = w - CENTER_X
        dy = h - CENTER_Y
        
        # ACTUAL distance - evenly spaced
        dist = int((dx * dx + dy * dy) ** 0.5)
        
        # Each ring is 20 pixels wide
        ring_number = dist // 20
        
        # Alternate black and white
        color = (ring_number % 2) * 255
        
        print(f"{color} {color} {color}")
```

**What you'll see:**
- Concentric circles
- Each ring exactly 20 pixels wide
- Like a target at a shooting range
- Uniform, regular pattern

#### Approach B: Accelerating Rings (No Square Root)
```python
WIDTH = 200
HEIGHT = 200
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

print(f"P3\n{WIDTH} {HEIGHT}\n255")

for h in range(HEIGHT):
    for w in range(WIDTH):
        dx = w - CENTER_X
        dy = h - CENTER_Y
        
        # Distance SQUARED - accelerating rings
        dist_squared = dx * dx + dy * dy
        
        # Divide by 400 (which is 20²)
        ring_number = dist_squared // 400
        
        # Alternate black and white
        color = (ring_number % 2) * 255
        
        print(f"{color} {color} {color}")
```

**What you'll see:**
- Concentric circles
- Inner rings tight/narrow
- Outer rings wider
- Like ripples in water (they spread out as they travel)
- More organic, natural look

### Part 7: Why Choose One Over The Other?

#### Use ACTUAL distance (with sqrt) when:
- You want geometric precision
- Creating a target/bullseye
- Need exactly equal ring widths
- Mathematical/technical visualization

#### Use SQUARED distance (no sqrt) when:
- Creating water ripples
- Simulating wave propagation (physics)
- Want an organic/natural look
- Performance matters (sqrt is expensive)
- Creating explosion/impact effects

### Part 8: The Complete Picture - Adding Gradients

Instead of just black/white, we can create gradients within each ring:

```python
WIDTH = 200
HEIGHT = 200
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

print(f"P3\n{WIDTH} {HEIGHT}\n255")

for h in range(HEIGHT):
    for w in range(WIDTH):
        dx = w - CENTER_X
        dy = h - CENTER_Y
        
        dist = int((dx * dx + dy * dy) ** 0.5)
        
        # Where are we WITHIN the current ring?
        position_in_ring = dist % 20  # 0 to 19
        
        # Create gradient: 0→255 across each ring
        gradient = (position_in_ring * 255) // 20
        
        print(f"{gradient} {gradient} {gradient}")
```

**What this does:**
- `dist % 20` gives position within current 20-pixel ring
- Position 0 (start of ring) → black (0)
- Position 19 (end of ring) → almost white (242)
- Then resets to black for next ring

**Result: Alternating dark-to-light gradients in concentric rings**

### Part 9: Common Mistakes and Fixes

#### Mistake 1: Forgetting to subtract center
```python
# WRONG - measures from corner, not center
dist = (w * w + h * h) ** 0.5

# CORRECT - measures from center
dist = ((w - CENTER_X)**2 + (h - CENTER_Y)**2) ** 0.5
```

#### Mistake 2: Mixing squared and non-squared approaches
```python
# WRONG - using squared distance with non-squared threshold
dist_squared = dx * dx + dy * dy
ring = dist_squared // 20  # Should be 400 (20²), not 20!

# CORRECT
dist_squared = dx * dx + dy * dy
ring = dist_squared // 400  # 20² = 400
```

#### Mistake 3: Integer overflow (rare, but possible)
```python
# If WIDTH and HEIGHT are very large (>32000), this could overflow
dist_squared = dx * dx + dy * dy  # Could exceed 2^31

# Fix: Use floating point for very large images
dist = (dx * dx + dy * dy) ** 0.5
```

### Part 10: Practice Exercise

Try to predict what this code creates:

```python
dx = w - CENTER_X
dy = h - CENTER_Y
dist = int((dx * dx + dy * dy) ** 0.5)

ring = (dist // 15) % 3

if ring == 0:
    color = 255  # White
elif ring == 1:
    color = 128  # Gray
else:
    color = 0    # Black
```

**Answer:** Concentric circles with 3-color pattern (white, gray, black, white, gray, black...), each ring 15 pixels wide.

### Summary: The Two Key Ideas

1. **Distance from center** determines which ring a pixel belongs to
   - Calculate using Pythagorean theorem: √(dx² + dy²)
   - OR use squared distance for performance/effects: dx² + dy²

2. **Modulo creates repetition** in the radial direction
   - `dist // RING_WIDTH` tells you which ring
   - `dist % RING_WIDTH` tells you position within that ring
   - Use `% NUM_RINGS` for alternating patterns

**The formula structure:**
```
Distance → Ring Number → Pattern Value → Color

(dx² + dy²)^0.5 → dist // 20 → ring % 2 → value * 255
```

---

## Lesson 4: XOR Patterns - Binary Magic Explained

**Why XOR Creates Fractals:**
```python
pattern = w ^ h
```

The binary mechanism:
- `5 ^ 3` in binary: `101 ^ 011 = 110` (decimal 6)
- Each bit position creates patterns at different scales
- Bit 0 (LSB): alternates every pixel
- Bit 1: alternates every 2 pixels
- Bit 2: alternates every 4 pixels
- Result: self-similar patterns at power-of-2 scales!

**Controlling XOR Patterns:**
```python
WIDTH = 256  # Power of 2 for clean patterns
HEIGHT = 256

print(f"P3\n{WIDTH} {HEIGHT}\n255")

# Control parameters
OPERATION = "xor"  # "xor", "and", "or", "sierpinski"
SCALE = 1  # Scale the input coordinates
ISOLATE_BIT = -1  # -1 for all bits, 0-7 for specific bit

for h in range(HEIGHT):
    for w in range(WIDTH):
        # Scale coordinates for larger patterns
        scaled_w = w // SCALE
        scaled_h = h // SCALE
        
        if OPERATION == "xor":
            pattern = scaled_w ^ scaled_h
        elif OPERATION == "and":
            pattern = scaled_w & scaled_h  # Different fractal structure
        elif OPERATION == "or":
            pattern = scaled_w | scaled_h   # Fill pattern
        elif OPERATION == "sierpinski":
            # True Sierpinski: check if C(h, w) is odd
            # Approximation using AND
            pattern = 255 if (scaled_w & scaled_h) == 0 else 0
        
        if ISOLATE_BIT >= 0:
            # Show only one bit plane (visualize specific scale)
            pattern = ((pattern >> ISOLATE_BIT) & 1) * 255
        else:
            # Use all bits
            pattern = pattern % 256
        
        print(f"{pattern} {pattern} {pattern}")
```

**Key Insight**: Each bit position represents a different frequency component:
- AND creates "holes" (zero where both have zeros)
- OR creates "fills" (one where either has ones)  
- XOR creates "edges" (one where bits differ)

---

## Lesson 5: Interference - Controlling Wave Interactions

**The Interference Mechanism:**
```python
wave1 = (w * FREQ1) % PERIOD1
wave2 = (h * FREQ2) % PERIOD2
interference = (wave1 + wave2) % COMBINED_PERIOD
```

What's really happening:
- Each wave is a sawtooth (not sine) due to modulo
- Adding waves creates beat frequencies
- The GCD of periods determines the large-scale pattern
- The LCM determines when the pattern repeats

**Precise Wave Control:**
```python
WIDTH = 200
HEIGHT = 200

print(f"P3\n{WIDTH} {HEIGHT}\n255")

# Control parameters - the key to interference patterns!
FREQ1 = 3    # Frequency multiplier for wave 1
FREQ2 = 5    # Frequency multiplier for wave 2
PERIOD1 = 17  # Period of wave 1 (use primes for interesting patterns)
PERIOD2 = 13  # Period of wave 2
PHASE1 = 0    # Phase shift for wave 1
PHASE2 = 0    # Phase shift for wave 2

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return (a * b) // gcd(a, b)

# Pattern will repeat every LCM pixels
pattern_period = lcm(PERIOD1, PERIOD2)

for h in range(HEIGHT):
    for w in range(WIDTH):
        # Generate waves with controllable parameters
        wave1 = ((w * FREQ1 + PHASE1) % PERIOD1)
        wave2 = ((h * FREQ2 + PHASE2) % PERIOD2)
        
        # Different interference modes
        additive = (wave1 + wave2) % pattern_period
        multiplicative = (wave1 * wave2) % 256
        difference = abs(wave1 - wave2)
        
        # Normalize to color range
        r = (additive * 255) // pattern_period
        g = multiplicative
        b = (difference * 255) // max(PERIOD1, PERIOD2)
        
        print(f"{r} {g} {b}")
```

**Control Strategies:**
- **Primes for periods**: Creates maximum cycle before repetition
- **Frequency multipliers**: Stretch/compress the waves
- **Phase shifts**: Move patterns without changing structure
- **Coprime periods**: Most interesting interference

---

## Lesson 6: Hash Functions - Controlled Randomness

**Why Hash Functions Work for Textures:**
```python
def hash2d(x, y):
    n = x + y * 57  # Combine coordinates
    n = (n << 13) ^ n  # Bit mixing
    return ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) % 256
```

The mechanism:
1. **Coordinate combination**: `y * 57` ensures different rows differ
2. **Bit shifting**: Spreads low bits to high bits
3. **Polynomial mixing**: Creates avalanche effect (small input change → large output change)
4. **Large primes**: Minimize patterns/repetition

**Building Controlled Noise:**
```python
WIDTH = 200
HEIGHT = 200

def hash2d(x, y, seed=0):
    """Controllable hash with seed"""
    # Different primes for different patterns
    PRIME1 = 73856093
    PRIME2 = 19349663
    PRIME3 = 83492791
    
    n = x * PRIME1 ^ y * PRIME2 ^ seed * PRIME3
    n = ((n >> 16) ^ n) * 0x45d9f3b
    n = ((n >> 16) ^ n) * 0x45d9f3b
    n = (n >> 16) ^ n
    return n & 0xFF  # Return 0-255

print(f"P3\n{WIDTH} {HEIGHT}\n255")

# Control parameters
SCALE = 8  # Size of noise cells
OCTAVES = 3  # Number of detail layers
PERSISTENCE = 0.5  # How much each octave contributes
SEED = 42  # Change for different patterns

for h in range(HEIGHT):
    for w in range(WIDTH):
        value = 0
        amplitude = 1.0
        max_value = 0
        
        for octave in range(OCTAVES):
            # Sample at this octave's scale
            scale = SCALE // (2 ** octave)
            if scale < 1:
                scale = 1
            
            cell_x = w // scale
            cell_y = h // scale
            
            # Position within cell (for interpolation)
            local_x = (w % scale) / float(scale)
            local_y = (h % scale) / float(scale)
            
            # Get corner values
            v00 = hash2d(cell_x, cell_y, SEED + octave)
            v10 = hash2d(cell_x + 1, cell_y, SEED + octave)
            v01 = hash2d(cell_x, cell_y + 1, SEED + octave)
            v11 = hash2d(cell_x + 1, cell_y + 1, SEED + octave)
            
            # Smooth interpolation (quintic for better smoothness)
            def smoothstep(t):
                return t * t * t * (t * (t * 6 - 15) + 10)
            
            sx = smoothstep(local_x)
            sy = smoothstep(local_y)
            
            # Bilinear interpolation
            v0 = v00 * (1 - sx) + v10 * sx
            v1 = v01 * (1 - sx) + v11 * sx
            v = v0 * (1 - sy) + v1 * sy
            
            value += v * amplitude
            max_value += amplitude * 255
            amplitude *= PERSISTENCE
        
        # Normalize
        normalized = int((value / max_value) * 255)
        
        print(f"{normalized} {normalized} {normalized}")
```

**Key Controls:**
- **SCALE**: Base size of noise features
- **OCTAVES**: How many layers of detail
- **PERSISTENCE**: Relative strength of fine details
- **Interpolation function**: Linear vs smooth (quintic)

---

## Lesson 7: Cellular Patterns - Discrete Dynamical Systems

**How Cellular Automata Create Patterns:**
```python
# Rule 30: left XOR (center OR right)
new_state = left ^ (center | right)
```

The mechanism of emergence:
- Local rules (3 cells) create global patterns
- Information propagates at "speed of light" (1 cell/generation)
- Boundaries/edges create reflections in patterns
- Different rules create different pattern classes

**Controlling Cellular Automata:**
```python
WIDTH = 200
HEIGHT = 200

print(f"P3\n{WIDTH} {HEIGHT}\n255")

# Control parameters
RULE = 30  # Wolfram rule number (0-255)
NEIGHBORHOOD = 3  # How many neighbors to consider
WRAP = True  # Wrap edges (toroidal topology)

def apply_rule(left, center, right, rule_number):
    """Apply a Wolfram elementary CA rule"""
    # Create 3-bit index from neighborhood
    index = (left << 2) | (center << 1) | right
    # Extract bit from rule number
    return (rule_number >> index) & 1

# Initialize with controlled pattern
current_row = []
INIT_PATTERN = "single"  # "single", "random", "periodic"

if INIT_PATTERN == "single":
    current_row = [0] * WIDTH
    current_row[WIDTH // 2] = 1
elif INIT_PATTERN == "random":
    import random
    current_row = [random.randint(0, 1) for _ in range(WIDTH)]
elif INIT_PATTERN == "periodic":
    current_row = [(i // 10) % 2 for i in range(WIDTH)]

for h in range(HEIGHT):
    next_row = []
    
    for w in range(WIDTH):
        if h == 0:
            value = current_row[w]
        else:
            if WRAP:
                left = current_row[(w - 1) % WIDTH]
                right = current_row[(w + 1) % WIDTH]
            else:
                left = current_row[w - 1] if w > 0 else 0
                right = current_row[w + 1] if w < WIDTH - 1 else 0
            
            center = current_row[w]
            value = apply_rule(left, center, right, RULE)
        
        next_row.append(value)
        
        # Multi-state visualization
        history_bit = current_row[w] if h > 0 else 0
        r = value * 255
        g = history_bit * 128  # Show previous state dimly
        b = 0
        
        print(f"{r} {g} {b}")
    
    current_row = next_row
```

**Pattern Classes by Rule:**
- Rules 0-29: Often simple/repetitive
- Rule 30: Chaotic (used in Mathematica's RNG)
- Rule 90: Sierpinski triangle
- Rule 110: Turing complete!
- Rule 184: Traffic flow model

---

## Lesson 8: Voronoi - Distance to Multiple Points

**The Voronoi Mechanism:**
Each pixel belongs to its nearest seed point. This creates organic cell patterns.

**Controlling Voronoi Patterns:**
```python
WIDTH = 200
HEIGHT = 200

def hash2d(x, y):
    n = x + y * 57
    n = (n << 13) ^ n
    return ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff)

print(f"P3\n{WIDTH} {HEIGHT}\n255")

# Control parameters
GRID_SIZE = 20  # Size of each Voronoi cell
RANDOMNESS = 0.8  # 0 = perfect grid, 1 = fully random
DISTANCE_TYPE = "euclidean"  # "euclidean", "manhattan", "chebyshev"
SHOW_EDGES = True  # Highlight cell boundaries

# Generate seed points with controlled randomness
seeds = []
for gy in range(-1, HEIGHT // GRID_SIZE + 2):
    for gx in range(-1, WIDTH // GRID_SIZE + 2):
        # Base grid position
        base_x = gx * GRID_SIZE + GRID_SIZE // 2
        base_y = gy * GRID_SIZE + GRID_SIZE // 2
        
        # Add controlled randomness
        hash_val = hash2d(gx, gy)
        offset_x = ((hash_val % 256) / 256.0 - 0.5) * GRID_SIZE * RANDOMNESS
        offset_y = (((hash_val >> 8) % 256) / 256.0 - 0.5) * GRID_SIZE * RANDOMNESS
        
        seeds.append((base_x + offset_x, base_y + offset_y, hash_val))

for h in range(HEIGHT):
    for w in range(WIDTH):
        # Find two nearest seeds
        distances = []
        
        for sx, sy, seed_hash in seeds:
            if DISTANCE_TYPE == "euclidean":
                dist = ((w - sx) ** 2 + (h - sy) ** 2) ** 0.5
            elif DISTANCE_TYPE == "manhattan":
                dist = abs(w - sx) + abs(h - sy)
            elif DISTANCE_TYPE == "chebyshev":
                dist = max(abs(w - sx), abs(h - sy))
            
            distances.append((dist, seed_hash))
        
        distances.sort()
        nearest_dist = distances[0][0]
        second_dist = distances[1][0]
        nearest_hash = distances[0][1]
        
        # Edge detection: where two cells meet
        edge_strength = 1.0 - (second_dist - nearest_dist) / GRID_SIZE
        edge_strength = max(0, min(1, edge_strength * 10))
        
        # Color based on cell ID (from hash)
        cell_color = nearest_hash % 256
        
        if SHOW_EDGES and edge_strength > 0.8:
            # Black edges
            r = g = b = 0
        else:
            # Cell coloring
            r = cell_color
            g = (cell_color * 137) % 256  # Pseudo-random color
            b = (cell_color * 89) % 256
        
        print(f"{r} {g} {b}")
```

**Key Parameters:**
- **GRID_SIZE**: Average cell size
- **RANDOMNESS**: Organic vs regular appearance
- **Distance metric**: Changes cell shape (circles vs diamonds vs squares)

---

## Lesson 9: Fractal Subdivision - Recursive Patterns

**The Subdivision Mechanism:**
Recursively subdivide space and apply rules at each level.

**Controlling Fractal Patterns:**
```python
WIDTH = 256  # Power of 2 for clean subdivision
HEIGHT = 256

def should_subdivide(x, y, size, depth):
    """Determine if a region should subdivide"""
    # Hash-based decision with depth bias
    hash_val = (x * 73856093) ^ (y * 19349663) ^ (size * 83492791)
    threshold = 0.5 + depth * 0.1  # Less likely to subdivide at deeper levels
    return (hash_val % 1000) / 1000.0 < threshold

def fill_region(grid, x, y, size, value):
    """Fill a square region with a value"""
    for dy in range(size):
        for dx in range(size):
            if y + dy < HEIGHT and x + dx < WIDTH:
                grid[y + dy][x + dx] = value

print(f"P3\n{WIDTH} {HEIGHT}\n255")

# Control parameters
MAX_DEPTH = 6  # Maximum recursion depth
MIN_SIZE = 4   # Minimum region size
COLOR_BY = "depth"  # "depth", "size", "position"

# Initialize grid
grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

# Recursive subdivision
def subdivide(x, y, size, depth):
    if size <= MIN_SIZE or depth >= MAX_DEPTH:
        # Base case: fill with value
        if COLOR_BY == "depth":
            value = (depth * 255) // MAX_DEPTH
        elif COLOR_BY == "size":
            value = (size * 255) // WIDTH
        else:  # position
            value = ((x + y) * 255) // (WIDTH + HEIGHT)
        
        fill_region(grid, x, y, size, value)
        return
    
    # Decide whether to subdivide
    if should_subdivide(x, y, size, depth):
        # Subdivide into 4 quadrants
        half = size // 2
        subdivide(x, y, half, depth + 1)
        subdivide(x + half, y, half, depth + 1)
        subdivide(x, y + half, half, depth + 1)
        subdivide(x + half, y + half, half, depth + 1)
    else:
        # Don't subdivide, fill with current depth value
        value = (depth * 255) // MAX_DEPTH
        fill_region(grid, x, y, size, value)

# Start subdivision
subdivide(0, 0, WIDTH, 0)

# Output the grid
for h in range(HEIGHT):
    for w in range(WIDTH):
        val = grid[h][w]
        
        # Add some variety to the coloring
        r = val
        g = (val + 85) % 256
        b = (val + 170) % 256
        
        print(f"{r} {g} {b}")
```

**Control Points:**
- **Subdivision probability**: Controls density
- **MAX_DEPTH**: Controls detail level
- **MIN_SIZE**: Controls finest features
- **Decision function**: Can use position, hash, or external data

---

## Lesson 10: Mastery - Building Complex Textures

**Combining Everything:**
Now you understand the mechanics. Here's how to build any texture you want:

```python
WIDTH = 256
HEIGHT = 256

import math

print(f"P3\n{WIDTH} {HEIGHT}\n255")

# Master control parameters
TEXTURE_TYPE = "stone"  # "stone", "wood", "metal", "fabric"

def fbm_noise(x, y, octaves=4, persistence=0.5):
    """Fractal Brownian Motion"""
    value = 0
    amplitude = 1
    frequency = 1
    max_value = 0
    
    for i in range(octaves):
        # Simple hash noise (replace with Perlin for smoothness)
        n = hash(f"{x*frequency},{y*frequency}") % 256
        value += n * amplitude / 256
        max_value += amplitude
        amplitude *= persistence
        frequency *= 2
    
    return value / max_value

def domain_warp(x, y, strength=10):
    """Warp coordinates for organic feel"""
    # Use noise to distort coordinates
    warp_x = fbm_noise(x * 0.1, y * 0.1) * strength
    warp_y = fbm_noise(x * 0.1 + 100, y * 0.1 + 100) * strength
    return x + warp_x, y + warp_y

for h in range(HEIGHT):
    for w in range(WIDTH):
        if TEXTURE_TYPE == "stone":
            # Voronoi + noise for stone/concrete
            wx, wy = domain_warp(w, h, strength=5)
            
            # Voronoi base
            cell_x = int(wx // 20)
            cell_y = int(wy // 20)
            cell_hash = hash(f"{cell_x},{cell_y}") % 256
            
            # Add surface noise
            detail = fbm_noise(w * 0.5, h * 0.5, octaves=3)
            
            # Cracks (using distance to cell boundary)
            dx = wx % 20 - 10
            dy = wy % 20 - 10
            crack = min(abs(dx), abs(dy)) < 2
            
            base = cell_hash * (1 - detail * 0.3)
            r = int(base * (0.2 if crack else 1))
            g = int(base * 0.9 * (0.2 if crack else 1))
            b = int(base * 0.8 * (0.2 if crack else 1))
            
        elif TEXTURE_TYPE == "wood":
            # Rings with perturbation
            # Distance from a line (wood grain runs along x)
            dist_from_center = abs(h - HEIGHT // 2)
            
            # Add warping for natural wood
            warp = math.sin(w * 0.05) * 10
            ring_pos = (dist_from_center + warp) * 0.5
            
            # Wood rings
            ring = int(ring_pos) % 30
            ring_gradient = ring_pos % 1  # Position within ring
            
            # Base wood color
            base_r = 139 + ring * 2
            base_g = 69 + ring
            base_b = 19
            
            # Add grain detail
            grain = hash(f"{int(w*0.1)},{int(ring_pos)}") % 30
            
            r = min(255, base_r + grain - int(ring_gradient * 20))
            g = min(255, base_g + grain // 2 - int(ring_gradient * 10))
            b = min(255, base_b + grain // 3)
            
        elif TEXTURE_TYPE == "metal":
            # Brushed metal using directional noise
            # Anisotropic pattern (stretched along x)
            brush = hash(f"{w},{int(h*0.1)}") % 40
            
            # Subtle sine wave for shimmer
            shimmer = math.sin(w * 0.1 + h * 0.01) * 10
            
            # Base metal gray
            base = 180 + brush + int(shimmer)
            
            # Slight blue tint for steel
            r = min(255, base)
            g = min(255, base)
            b = min(255, base + 10)
            
        elif TEXTURE_TYPE == "fabric":
            # Woven pattern using interference
            thread_x = (w % 8) < 4
            thread_y = (h % 8) < 4
            
            # XOR gives over-under weave
            weave = thread_x ^ thread_y
            
            # Add fabric texture
            texture = fbm_noise(w * 2, h * 2, octaves=2)
            
            # Fabric colors
            if weave:
                r = int(200 * (1 - texture * 0.2))
                g = int(100 * (1 - texture * 0.2))
                b = int(100 * (1 - texture * 0.2))
            else:
                r = int(150 * (1 - texture * 0.3))
                g = int(50 * (1 - texture * 0.3))
                b = int(50 * (1 - texture * 0.3))
        
        print(f"{r} {g} {b}")
```

---

## The Control Principles

**1. Frequency Control:**
- Modulo period = feature size
- Smaller period = higher frequency = more repetitions
- `(x * frequency) % period`

**2. Phase Control:**
- Add offset before modulo to shift pattern
- `(x + phase) % period`

**3. Amplitude Control:**
- Scale after modulo to control intensity
- `((x % period) * amplitude) / period`

**4. Combining Patterns:**
- Addition: overlays patterns
- Multiplication: creates interference
- XOR: creates edges/transitions
- Min/Max: creates masks/clips

**5. Coordinate Transformation:**
- Rotate: `x_rot = x*cos(θ) - y*sin(θ)`
- Scale: `x_scaled = x * scale`
- Warp: `x_warped = x + f(x, y)`

**6. Multi-scale (Octaves):**
- Each octave doubles frequency
- Each octave halves amplitude
- Sum creates natural complexity

**7. Value Mapping:**
- Linear: `value * 255 / max_value`
- Power: `(value ** gamma) * 255`
- Threshold: `255 if value > threshold else 0`
- Smooth: `smoothstep(value) * 255`

---

## The Essential Formula Cookbook

Here are the exact formulas for common patterns you'll want:

### Stripes (any orientation)
```python
# Axis-aligned stripes
vertical = (x % period) * 255 // period
horizontal = (y % period) * 255 // period

# Diagonal stripes at any angle
angle_rad = angle_degrees * math.pi / 180
rotated = (x * math.cos(angle_rad) + y * math.sin(angle_rad))
diagonal = (int(rotated) % period) * 255 // period
```

### Circles and Rings
```python
# Concentric rings from center
dist = math.sqrt((x - cx)**2 + (y - cy)**2)
rings = (int(dist / ring_width) % num_rings) * 255 // num_rings

# Spiral
angle = math.atan2(y - cy, x - cx)
spiral = (int(dist / spiral_tightness + angle * turns) % num_arms) * 255 // num_arms
```

### Grids and Dots
```python
# Grid lines
on_grid = ((x % grid_size) < line_width) or ((y % grid_size) < line_width)
color = 255 if on_grid else 0

# Dot grid
cell_x = x % grid_size
cell_y = y % grid_size
dist_to_center = math.sqrt((cell_x - grid_size//2)**2 + (cell_y - grid_size//2)**2)
is_dot = dist_to_center < dot_radius
color = 255 if is_dot else 0
```

### Gradients
```python
# Linear gradient
linear = (x * 255) // width  # Left to right

# Radial gradient
dist = math.sqrt((x - cx)**2 + (y - cy)**2)
max_dist = math.sqrt(width**2 + height**2)
radial = (dist * 255) // max_dist

# Angular gradient (conical)
angle = math.atan2(y - cy, x - cx) + math.pi  # 0 to 2π
angular = int(angle * 255 / (2 * math.pi))
```

### Noise Patterns
```python
# Value noise (blocky)
cell_x = x // cell_size
cell_y = y // cell_size
noise = hash((cell_x, cell_y)) % 256

# Interpolated noise (smooth)
cell_x = x // cell_size
cell_y = y // cell_size
local_x = (x % cell_size) / cell_size
local_y = (y % cell_size) / cell_size

# Get 4 corners
v00 = hash((cell_x, cell_y)) % 256
v10 = hash((cell_x + 1, cell_y)) % 256
v01 = hash((cell_x, cell_y + 1)) % 256
v11 = hash((cell_x + 1, cell_y + 1)) % 256

# Bilinear interpolation
top = v00 * (1 - local_x) + v10 * local_x
bottom = v01 * (1 - local_x) + v11 * local_x
smooth_noise = int(top * (1 - local_y) + bottom * local_y)
```

### Wave Patterns
```python
# Sine wave (without using sin - using approximation)
# Taylor series approximation: sin(x) ≈ x - x³/6 + x⁵/120
def approx_sin(x):
    x = x % (2 * math.pi)
    return x - (x**3)/6 + (x**5)/120

wave = int((approx_sin(x * frequency) + 1) * 127.5)

# Sawtooth wave (using modulo)
sawtooth = (x * frequency) % 256

# Triangle wave
triangle = abs(((x * frequency) % 512) - 256)

# Square wave
square = 255 if ((x * frequency) % 256) < 128 else 0
```

---

## Advanced Control Techniques

### Masking and Layering
```python
# Create mask from one pattern
mask = pattern1 > threshold

# Apply mask to blend patterns
result = pattern2 if mask else pattern3

# Soft blend using mask as alpha
alpha = pattern1 / 255.0
result = int(pattern2 * alpha + pattern3 * (1 - alpha))
```

### Domain Warping
```python
# Use one pattern to distort another
warp_amount = 20
warp_x = x + (pattern1 - 128) * warp_amount / 128
warp_y = y + (pattern2 - 128) * warp_amount / 128

# Sample new pattern at warped coordinates
warped_pattern = sample_pattern_at(warp_x, warp_y)
```

### Feedback Loops
```python
# Use previous values to influence next values
previous = 128
for y in range(height):
    for x in range(width):
        # Current value influenced by previous
        current = (hash(x, y) + previous) % 256
        previous = (previous + current) // 2
        pixel[y][x] = current
```

### Reaction-Diffusion
```python
# Simulate chemical reactions for organic patterns
# Gray-Scott model simplified
def update_reaction_diffusion(grid_a, grid_b, feed, kill):
    new_a = grid_a.copy()
    new_b = grid_b.copy()
    
    for y in range(1, height-1):
        for x in range(1, width-1):
            a = grid_a[y][x]
            b = grid_b[y][x]
            
            # Simplified reaction
            reaction = a * b * b
            
            new_a[y][x] = a + feed * (1 - a) - reaction
            new_b[y][x] = b + reaction - (kill + feed) * b
            
            # Clamp values
            new_a[y][x] = max(0, min(1, new_a[y][x]))
            new_b[y][x] = max(0, min(1, new_b[y][x]))
    
    return new_a, new_b
```

---

## Performance Optimization Tips

### Precomputation
```python
# Compute expensive operations once
LOOKUP = [expensive_function(i) for i in range(256)]

# Use lookup instead of computing
for y in range(height):
    for x in range(width):
        value = (x + y) % 256
        color = LOOKUP[value]  # Instead of expensive_function(value)
```

### Bit Operations for Speed
```python
# Fast modulo for powers of 2
value_mod_256 = value & 0xFF  # Same as value % 256
value_mod_128 = value & 0x7F  # Same as value % 128

# Fast multiplication/division by powers of 2
value_times_4 = value << 2   # Same as value * 4
value_div_8 = value >> 3     # Same as value // 8
```

### Avoid Redundant Calculations
```python
# Bad: recalculating for each pixel
for y in range(height):
    for x in range(width):
        center_x = width // 2   # Don't recalculate
        center_y = height // 2  # Don't recalculate

# Good: calculate once
center_x = width // 2
center_y = height // 2
for y in range(height):
    for x in range(width):
        # Use center_x, center_y
```

---

## Common Pitfalls and Solutions

### Integer Division Truncation
```python
# Problem: loses precision
color = pattern * 255 / period  # Returns float, may truncate wrong

# Solution: multiply first, then divide
color = (pattern * 255) // period  # Maintains precision
```

### Modulo with Negative Numbers
```python
# Problem: negative coordinates give unexpected results
pattern = (x - offset) % period  # Negative x gives negative modulo

# Solution: ensure positive before modulo
pattern = ((x - offset) % period + period) % period
```

### Off-by-One Errors in Scaling
```python
# Problem: doesn't reach full 255
color = (value * 255) // max_value  # If value == max_value-1, never gets 255

# Solution: careful boundary handling
color = min(255, (value * 256) // max_value)
```

---

## Debugging Techniques

### Visualize Components Separately
```python
# Debug complex patterns by isolating components
DEBUG_MODE = "component1"  # Change to test different parts

if DEBUG_MODE == "component1":
    color = component1
elif DEBUG_MODE == "component2":
    color = component2
elif DEBUG_MODE == "combined":
    color = (component1 + component2) // 2
```

### Range Checking
```python
# Ensure values are in expected range
assert 0 <= color <= 255, f"Color {color} out of range at ({x}, {y})"
```

### Pattern Verification
```python
# Verify pattern properties
period_actual = 0
last_value = -1
for x in range(width):
    value = x % expected_period
    if value < last_value:  # Wrapped around
        print(f"Period detected: {period_actual}")
        break
    last_value = value
    period_actual += 1
```

---

## Summary: The Path to Mastery

You now understand:

1. **Modulo creates periodicity** - It's the fundamental tool for repeating patterns
2. **Coordinate transforms control orientation** - Rotate, scale, warp as needed
3. **Multiple patterns interfere** - Addition, multiplication, XOR create complexity
4. **Hash functions provide controlled randomness** - Deterministic but random-looking
5. **Interpolation creates smoothness** - Bilinear, bicubic for organic feel
6. **Octaves add detail** - Multiple scales create natural textures
7. **Bitwise operations create fractals** - XOR, AND, OR at different bit levels

The key to mastery is understanding that **every visual pattern is just a function from coordinates to color**: `f(x, y) → (r, g, b)`

By controlling this function through:
- **Input transformation** (warp x, y)
- **Function composition** (combine multiple patterns)
- **Output mapping** (how values become colors)

You can create ANY procedural texture you can imagine.

Remember: The modulo operator isn't creating "magic" - it's creating **predictable, controllable cycles**. Once you internalize how these cycles interact, you can design textures like a composer writes music - layering frequencies, harmonies, and rhythms to create exactly the visual effect you want.