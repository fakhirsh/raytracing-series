# Answer Key - Modulo Arithmetic & Visual Patterns

Complete solutions and explanations for the worksheet exercises.

---

## Exercise 1 Answers: Vertical Stripes

**Answer 1.1:**
`STRIPE_WIDTH = 40`

Explanation: 200 pixels ÷ 5 stripes = 40 pixels per stripe.

**Answer 1.2:**
- Maximum color value: 242 (not 255!)
- Why: When `pattern = 19`, `(19 * 255) // 20 = 4845 // 20 = 242`
- Fix: Use `color = (pattern * 256) // 20` or `color = min(255, (pattern * 255 + 19) // 20)`

The issue is that `255/20 = 12.75`, so `19 * 12.75 = 242.25`, which truncates to 242.

**Answer 1.3:**
**Approach A is correct.**

```python
# Approach A - CORRECT
color = ((w % 20) * 255) // 20
# This multiplies first: (w % 20) * 255, giving range 0-4845
# Then divides by 20, giving range 0-242

# Approach B - WRONG
color = (w % 20) * 255 // 20
# Due to operator precedence, this is: (w % 20) * (255 // 20)
# 255 // 20 = 12, so this becomes: (w % 20) * 12
# Giving range 0-228, not 0-242!
```

The parentheses matter! Always multiply before dividing to preserve precision.

**Answer 1.4:**
**The stripes become horizontal instead of vertical.**

- `w % 20`: Every pixel in a vertical column has the same `w` value, so same pattern value → vertical stripes
- `h % 20`: Every pixel in a horizontal row has the same `h` value, so same pattern value → horizontal stripes

The stripes run perpendicular to the varying coordinate.

**Answer 1.5:**
```python
STRIPE_WIDTH = 15
for h in range(HEIGHT):
    for w in range(WIDTH):
        stripe_number = w // STRIPE_WIDTH
        color = (stripe_number % 2) * 255  # 0 or 255
        print(f"{color} {color} {color}")
```

Key insight: Use `//` to get stripe number, then `% 2` for alternation.

---

## Exercise 2 Answers: Checkerboards

**Answer 2.1:**
The formula creates a checkerboard because moving one tile in any direction flips the parity:

- (0, 0) → 0 + 0 = 0 → 0 % 2 = 0 (black)
- (0, 1) → 0 + 1 = 1 → 1 % 2 = 1 (white)
- (1, 0) → 1 + 0 = 1 → 1 % 2 = 1 (white)
- (1, 1) → 1 + 1 = 2 → 2 % 2 = 0 (black)

Moving right OR down flips the color. Moving diagonally keeps the same color (both coordinates change, parity stays same).

**Answer 2.2:**
`(tile_x - tile_y) % 2` creates **diagonal stripes** (running from top-left to bottom-right).

Difference:
- Addition: Changes when moving in ANY direction → checkerboard
- Subtraction: Constant along diagonals where `x - y` is constant → diagonal stripes

For example, all pixels where `x - y = 0` (the main diagonal) have the same value.

**Answer 2.3:**
```python
TILE_SIZE = 25

# Find which tile
tile_x = 137 // 25 = 5
tile_y = 89 // 25 = 3

# Determine color
pattern = (5 + 3) % 2 = 8 % 2 = 0  # Black tile
```

**Answer 2.4:**
Using `% 3` creates a pattern with **three colors** instead of two.

```python
pattern = (tile_x + tile_y) % 3  # Returns 0, 1, or 2
```

You'd need to map these to three distinct colors:
```python
if pattern == 0:
    color = 0      # Black
elif pattern == 1:
    color = 127    # Gray
else:
    color = 255    # White
```

The pattern still changes when moving in any direction, but now cycles through three states.

**Answer 2.5:**
The `offset` shifts every other row horizontally by half a tile width.

```python
offset = (tile_y % 2) * (TILE_SIZE // 2)
```

- When `tile_y` is even: `offset = 0` (no shift)
- When `tile_y` is odd: `offset = TILE_SIZE // 2` (shift right by half a tile)

This creates the staggered appearance of bricks in a wall, where each row is offset from the one above/below it.

---

## Exercise 3 Answers: Radial Patterns

**Answer 3.1:**
```python
dx = 150 - 100 = 50
dy = 120 - 100 = 20
dist_squared = 50*50 + 20*20 = 2500 + 400 = 2900

ring = 2900 // 400 = 7
```
This pixel is in ring number 7.

**Answer 3.2:**
- **Approach A (with sqrt): Creates evenly-spaced rings**
  - Each ring is exactly 10 pixels wide at all radii
  - Rings are uniform/linear spacing

- **Approach B (squared distance): Creates rings that get wider outward**
  - Ring thickness increases quadratically with radius
  - Inner rings tight, outer rings progressively wider
  - More "natural" looking for ripples/waves

**Answer 3.3:**
Non-uniform spacing (squared distance) is preferred for:
- **Wave propagation effects**: Real waves spread out as they travel
- **Ripple effects**: Natural ripples in water have this property
- **Energy dispersion**: Circular waves lose energy as area increases (E ∝ 1/r)
- **Less processing**: Avoids expensive square root calculation

The quadratic falloff matches physical phenomena better than uniform rings.

**Answer 3.4:**
```python
angle = math.atan2(dy, dx)  # Range: -π to π
angle_normalized = int((angle + math.pi) * 255 / (2 * math.pi))
```

Steps:
1. Add π to shift range from [-π, π] to [0, 2π]
2. Multiply by 255/(2π) to scale to [0, 255]
3. Convert to int for pixel value

**Answer 3.5:**
```python
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

for h in range(HEIGHT):
    for w in range(WIDTH):
        dx = w - CENTER_X
        dy = h - CENTER_Y
        
        # Use actual distance for uniform rings
        dist = int((dx * dx + dy * dy) ** 0.5)
        
        # Each ring is 20 pixels wide
        ring_number = dist // 20
        
        # Alternate black (0) and white (255)
        color = (ring_number % 2) * 255
        
        print(f"{color} {color} {color}")
```

---

## Exercise 4 Answers: XOR Patterns

**Answer 4.1:**
```
5 ^ 3:
  0101 (5)
^ 0011 (3)
------
  0110 (6)

12 ^ 9:
  1100 (12)
^ 1001 (9)
------
  0101 (5)

255 ^ 0:
  11111111 (255)
^ 00000000 (0)
----------
  11111111 (255)
```

**Answer 4.2:**
- Bit 0 (LSB) alternates every **1** pixel
- Bit 3 alternates every **8** pixels (2³ = 8)

Each bit position n creates patterns with period 2ⁿ.

**Answer 4.3:**
- **`w ^ h` (XOR)**: Creates diagonal crosshatch/fractal pattern
  - Bright where bits differ
  - Dark where bits match
  - Self-similar at multiple scales

- **`w & h` (AND)**: Creates dark diagonal pattern
  - Only bright where BOTH have 1 bits
  - Creates "holes" or "gaps"
  - Sierpinski-like triangular regions

- **`w | h` (OR)**: Creates bright diagonal pattern
  - Bright where EITHER has 1 bits
  - Only dark where BOTH are 0
  - "Fills" the space

**Answer 4.4:**
```python
pattern = ((w ^ h) >> 4) & 1
color = pattern * 255
```

Explanation:
1. `(w ^ h)` performs the XOR
2. `>> 4` shifts bit 4 down to bit 0 position
3. `& 1` masks out all other bits, keeping only bit 0
4. Multiply by 255 to get black (0) or white (255)

**Answer 4.5:**
"Self-similar patterns at power-of-2 scales" means the pattern looks similar when you zoom in by factors of 2, 4, 8, etc.

This happens because:
- Each bit position creates a pattern at scale 2ⁿ
- Bit 0: 1-pixel period
- Bit 1: 2-pixel period  
- Bit 2: 4-pixel period
- Bit 3: 8-pixel period

When you zoom in 2×, you're essentially looking at the next lower bit, which has the same structure. This creates the fractal/self-similar property.

It only works for power-of-2 because binary representation naturally divides space into power-of-2 regions.

**Answer 4.6:**
The Sierpinski triangle appears because `(w & h) == 0` checks whether `w` and `h` share any 1 bits in the same position.

Connection to Pascal's triangle:
- Pascal's triangle has entries C(n, k) = n!/(k!(n-k)!)
- A cell is odd if C(n, k) is odd
- Lucas's theorem: C(n, k) is odd if and only if `(n & k) == k`
- Equivalently, no bit overlap means C(n, k) is odd

So `(w & h) == 0` colors pixels where the binomial coefficient is odd, revealing the Sierpinski triangle hidden in Pascal's triangle mod 2!

---

## Exercise 5 Answers: Interference

**Answer 5.1:**
To find LCM(17, 13):
- Both are prime, so LCM = 17 × 13 = **221**
- The combined pattern repeats every 221 pixels

**Answer 5.2:**
Prime numbers create more interesting patterns because:
- **Maximum cycle length**: LCM of coprime numbers is their product
- **No common factors**: Prevents premature repetition
- **Complex interactions**: No simple harmonic relationships

For example:
- LCM(10, 15) = 30 (not very interesting, repeats quickly)
- LCM(11, 13) = 143 (prime, much more complex before repeating)

**Answer 5.3:**
```python
additive = (wave1 + wave2) % pattern_period
# Creates BRIGHT spots where both waves are at maximum (constructive interference)
# Max when wave1 = max AND wave2 = max

multiplicative = (wave1 * wave2) % 256  
# Creates BRIGHT spots where both waves are at maximum
# But grows faster (multiplication vs addition)
# Creates more contrast

difference = abs(wave1 - wave2)
# Creates DARK spots where waves cancel (wave1 ≈ wave2)
# Creates BRIGHT spots where waves differ maximally
# This is destructive interference visualization
```

**Answer 5.4:**
- **`PERIOD`**: How long before the wave repeats (wavelength)
- **`FREQ`**: How fast the coordinate changes affect the wave (frequency multiplier)

```python
wave = (x * FREQ) % PERIOD
```

- Higher `FREQ`: Compresses the wave (more cycles in same space)
- Higher `PERIOD`: Stretches individual cycles
- They have opposite effects!

**Answer 5.5:**
**Very similar periods (like 17 and 19) create moiré patterns.**

Reasoning:
- Moiré patterns occur when two similar frequencies beat against each other
- The "beat frequency" is `|freq1 - freq2|`
- With periods 17 and 19: beat period = LCM(17, 19) / |17 - 19| ≈ 323 / 2 ≈ 161 pixels
- This creates slow, visible oscillations (the moiré effect)

Very different frequencies (7 and 29) would create obvious separate patterns.
Identical frequencies would just reinforce (no moiré).

---

## Exercise 6 Answers: Hash Functions

**Answer 6.1:**
A good hash function needs these properties because:

1. **Combine x and y**: Otherwise, (3, 5) and (5, 3) would hash the same
   - Need unique output for each coordinate pair

2. **Use large primes**: Minimize collision patterns
   - Non-prime might create visible periodicities
   - Primes help "mix" bits more chaotically

3. **Mix bits**: Ensure small changes cascade through entire value
   - If only low bits changed, high bits would show patterns
   - Bit shifting/XOR spreads influence

**Answer 6.2:**
Multiplying y by 57 (or any constant) is crucial:

```python
# Bad: x + y
# (3, 5) and (5, 3) both give 8 - collision!
# (2, 6) and (4, 4) both give 8 - collision!

# Good: x + y * 57  
# (3, 5) → 3 + 285 = 288
# (5, 3) → 5 + 171 = 176  (different!)
# (2, 6) → 2 + 342 = 344
# (4, 4) → 4 + 228 = 232  (different!)
```

The multiplication creates a unique "space" for each y value, preventing coordinates that sum to the same value from colliding.

**Answer 6.3:**
- **`SCALE = 2, OCTAVES = 1`**: 
  - Small blocky noise cells (2×2 pixels)
  - Single detail level
  - Very pixelated look

- **`SCALE = 8, OCTAVES = 1`**:
  - Larger blocky noise cells (8×8 pixels)
  - Still single detail level
  - Smoother but still somewhat uniform

- **`SCALE = 8, OCTAVES = 3`**:
  - Base 8×8 cells PLUS finer details
  - Multiple scales combined
  - Natural, complex appearance
  - Most realistic of the three

**Answer 6.4:**
With `PERSISTENCE = 0.5`:
- Octave 1: amplitude = 1.0
- Octave 2: amplitude = 0.5
- Octave 3: amplitude = 0.25

The third octave contributes **1/4 as much** as the first octave.

**Answer 6.5:**
`smoothstep` creates C² continuous interpolation (smooth second derivative).

```python
def smoothstep(t):
    return t * t * t * (t * (t * 6 - 15) + 10)
```

**Without smoothstep (linear interpolation):**
- Creates visible seams between cells
- Derivative is discontinuous → "blocky" appearance
- You can see the grid structure

**With smoothstep:**
- Smooth transitions, no visible seams
- Natural, organic look
- Grid structure hidden

**Answer 6.6:**
Bilinear interpolation in words:

1. Interpolate horizontally along the top edge using `sx`:
   - `top = v00 * (1 - sx) + v10 * sx`

2. Interpolate horizontally along the bottom edge using `sx`:
   - `bottom = v01 * (1 - sx) + v11 * sx`

3. Interpolate vertically between top and bottom using `sy`:
   - `final = top * (1 - sy) + bottom * sy`

Or in one formula:
```python
final = (v00 * (1-sx) * (1-sy) + 
         v10 * sx * (1-sy) + 
         v01 * (1-sx) * sy + 
         v11 * sx * sy)
```

---

## Exercise 7 Answers: Cellular Automata

**Answer 7.1:**
Rule 30 in binary: `00011110`

```python
# Left=1, Center=1, Right=1
index = (1<<2) | (1<<1) | 1 = 4 + 2 + 1 = 7
bit_7 of 00011110 = 0 → Result: 0

# Left=0, Center=1, Right=0  
index = (0<<2) | (1<<1) | 0 = 0 + 2 + 0 = 2
bit_2 of 00011110 = 1 → Result: 1

# Left=0, Center=0, Right=0
index = (0<<2) | (0<<1) | 0 = 0
bit_0 of 00011110 = 0 → Result: 0
```

**Answer 7.2:**
- **`WRAP = True` (toroidal)**: 
  - Left edge connects to right edge
  - Pattern continues seamlessly
  - No boundary effects
  - Good for tileable patterns

- **`WRAP = False`**: 
  - Edges treated as 0 (dead cells)
  - Creates boundary effects/reflections
  - Pattern influenced by edge conditions
  - Can create interesting wave patterns off boundaries

**Answer 7.3:**
Rule 90's formula is `new_cell = left ^ right` (ignoring center!).

This creates Sierpinski triangles because:
- XOR creates additive patterns (as we learned in Exercise 4)
- Each row is essentially the XOR of shifted copies of the previous row
- This is equivalent to Pascal's triangle modulo 2
- Sierpinski triangle = Pascal's triangle mod 2

The connection: Just as `w ^ h` creates 2D Sierpinski patterns, repeatedly applying `left ^ right` creates the 1D version that grows into the triangle.

**Answer 7.4:**
**With "single" initial condition:**
- One cell creates a deterministic, symmetric pattern
- Rule 30 creates chaotic but structured output
- Pattern has vertical axis of symmetry (at least initially)
- Classic visualization of Rule 30

**With "random" initial condition:**
- Pattern is chaotic from the start
- No symmetry
- Still shows Rule 30's characteristic behavior
- Harder to see the "emergent" structure
- More like natural randomness

Single center cell is preferred for visualizing the rule's intrinsic behavior.

**Answer 7.5:**
Elementary CA are limited to 256 rules because:

- Each cell has 3 inputs: left, center, right
- Each input is binary: 0 or 1
- Total possible neighborhoods: 2³ = 8
- Each neighborhood needs an output: 0 or 1
- Total rule combinations: 2⁸ = 256

The rule number encodes all 8 outputs as an 8-bit binary number:
```
Neighborhood:  111 110 101 100 011 010 001 000
Rule 30:        0   0   0   1   1   1   1   0
Rule number = 00011110₂ = 30₁₀
```

---

## Exercise 8 Answers: Voronoi

**Answer 8.1:**
Seeds at (30, 30), (70, 40), (40, 70). Pixel at (50, 50).

**Euclidean distance:**
```python
d1 = sqrt((50-30)² + (50-30)²) = sqrt(400 + 400) = sqrt(800) ≈ 28.28
d2 = sqrt((50-70)² + (50-40)²) = sqrt(400 + 100) = sqrt(500) ≈ 22.36 ← Closest
d3 = sqrt((50-40)² + (50-70)²) = sqrt(100 + 400) = sqrt(500) ≈ 22.36 ← Tie!
```

**Manhattan distance:**
```python
d1 = |50-30| + |50-30| = 20 + 20 = 40
d2 = |50-70| + |50-40| = 20 + 10 = 30 ← Closest
d3 = |50-40| + |50-70| = 10 + 20 = 30 ← Tie!
```

**Chebyshev distance:**
```python
d1 = max(|50-30|, |50-30|) = max(20, 20) = 20 ← Closest
d2 = max(|50-70|, |50-40|) = max(20, 10) = 20 ← Tie!
d3 = max(|50-40|, |50-70|) = max(10, 20) = 20 ← Tie!
```

With Euclidean and Manhattan, seeds 2 and 3 tie. With Chebyshev, all three tie!

**Answer 8.2:**
- **Euclidean** → **Circular/rounded cells** (natural, organic)
- **Manhattan** → **Diamond-shaped cells** (45° rotated squares)
- **Chebyshev** → **Square cells** (axis-aligned squares)

**Answer 8.3:**
`second_dist - nearest_dist` measures how far you are from the boundary:

- At the boundary: `second_dist ≈ nearest_dist`, so difference ≈ 0
  - Two cells are equally close → you're on the edge
  
- Deep inside a cell: `second_dist >> nearest_dist`, difference is large
  - One cell is much closer → far from any boundary

By computing `1.0 - (difference / GRID_SIZE)`:
- Near boundary: small difference → high edge_strength
- Inside cell: large difference → low edge_strength

Then multiplying by 10 and thresholding sharpens the edges.

**Answer 8.4:**
- **`RANDOMNESS = 0`**: 
  - Perfect grid, no jitter
  - Seeds at exact grid intersections
  - Creates regular hexagonal/square patterns
  - Very artificial looking

- **`RANDOMNESS = 1`**: 
  - Maximum jitter (±GRID_SIZE/2)
  - Seeds highly displaced from grid
  - Organic, natural cell patterns
  - Irregular cell sizes

**Answer 8.5:**
```python
# Center of image
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

for h in range(HEIGHT):
    for w in range(WIDTH):
        # Find nearest seed
        min_dist = float('inf')
        nearest_seed_x = 0
        nearest_seed_y = 0
        
        for sx, sy, seed_hash in seeds:
            dist = ((w - sx)**2 + (h - sy)**2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                nearest_seed_x = sx
                nearest_seed_y = sy
        
        # Color based on seed's distance from center
        seed_center_dist = ((nearest_seed_x - CENTER_X)**2 + 
                           (nearest_seed_y - CENTER_Y)**2) ** 0.5
        max_seed_dist = ((WIDTH//2)**2 + (HEIGHT//2)**2) ** 0.5
        
        color = int((seed_center_dist / max_seed_dist) * 255)
        print(f"{color} {color} {color}")
```

---

## Exercise 9 Answers: Fractal Subdivision

**Answer 9.1:**
Starting with 256×256 image:
- **Depth 0**: 256×256 (entire image)
- **Depth 1**: 128×128 (quarters)
- **Depth 2**: 64×64
- **Depth 3**: 32×32 ← Answer
- **Depth 4**: 16×16
- **Depth 5**: 8×8
- **Depth 6**: 4×4 ← Answer

Formula: `size_at_depth = WIDTH // (2 ** depth)`

**Answer 9.2:**
Power-of-2 dimensions are required because:

1. **Clean division**: 256 / 2 / 2 / 2 ... always gives integers
2. **No remainder issues**: Avoids edge cases with odd-sized regions
3. **Symmetric subdivision**: Each quadrant is exactly 1/4 of parent
4. **Fits binary tree structure**: Depth corresponds to bit positions

With non-power-of-2 (like 200):
- 200 / 2 = 100 ✓
- 100 / 2 = 50 ✓  
- 50 / 2 = 25 ✓
- 25 / 2 = 12 (with remainder!) ✗

**Answer 9.3:**
```python
threshold = 0.5 + depth * 0.1
```

As depth increases, threshold increases, making subdivision **less likely** at deeper levels.

**Visual effect:**
- **Shallow depths**: More subdivision → smaller regions
- **Deep depths**: Less subdivision → larger regions at bottom of tree
- **Result**: Prevents infinite subdivision, creates variety in region sizes
- **Natural look**: Mix of large and small features

Without this, you'd get uniform smallest-size regions everywhere (or nothing if threshold too high).

**Answer 9.4:**
- **`"depth"`**: 
  - Colors by recursion level
  - Creates "layers" visualization
  - Shows recursive structure clearly
  - Gradient from top-level to bottom-level

- **`"size"`**: 
  - Colors by region area
  - Larger regions brighter (or darker)
  - Shows scale distribution
  - Emphasizes size hierarchy

- **`"position"`**: 
  - Colors by x+y coordinates
  - Diagonal gradient across image
  - Independent of subdivision structure
  - Shows spatial variation

**Answer 9.5:**
For a "city block" pattern:

```python
def subdivide(x, y, size, depth, is_street_x=False, is_street_y=False):
    if size <= MIN_SIZE or depth >= MAX_DEPTH:
        # Color based on whether it's a street or building
        if is_street_x or is_street_y:
            color = 64  # Dark street
        else:
            # Building height varies
            height = hash(f"{x},{y}") % 128 + 128
            color = height
        fill_region(grid, x, y, size, color)
        return
    
    # Subdivide with street gaps
    street_width = 4
    building_size = (size - street_width) // 2
    
    # Four buildings with streets between
    subdivide(x, y, building_size, depth+1, False, False)
    subdivide(x + building_size + street_width, y, building_size, depth+1, False, False)
    subdivide(x, y + building_size + street_width, building_size, depth+1, False, False)
    subdivide(x + building_size + street_width, y + building_size + street_width, building_size, depth+1, False, False)
    
    # Horizontal street
    fill_region(grid, x, y + building_size, size, street_width, 64)
    # Vertical street
    fill_region(grid, x + building_size, y, street_width, size, 64)
```

Key modifications:
- Add street spacing between subdivisions
- Track whether region is street or building
- Vary building "height" (brightness) randomly

---

## Exercise 10 Answers: Complex Textures

**Answer 10.1:**
**Stone texture** combines:

1. **Voronoi cells**: 
   - Creates base "chunks" of stone
   - Each cell = one piece of aggregate/mineral
   - Provides large-scale structure

2. **FBM noise**:
   - Adds surface roughness/texture within each cell
   - Simulates micro-fractures and grain
   - Creates variation in brightness

3. **Crack detection**:
   - Uses distance to cell boundaries
   - Darkens pixels near edges
   - Simulates gaps/cracks between stone pieces

Together: macro-structure (Voronoi) + micro-texture (noise) + defects (cracks) = realistic stone.

**Answer 10.2:**
**Warping is essential for realistic wood** because:

```python
warp = math.sin(w * 0.05) * 10
```

**With warping:**
- Rings undulate naturally
- Follows grain irregularities
- Looks organic and grown
- Mimics real wood fiber variation

**Without warping:**
- Perfectly circular/straight rings
- Looks artificial, like a target
- No wood "grain" direction
- Obviously computer-generated

Real wood rings aren't perfect circles due to growth variations, wind stress, and environmental factors. Warping simulates this.

**Answer 10.3:**
```python
brush = hash(f"{w},{int(h*0.1)}") % 40
```

**The asymmetry creates directional texture:**

- **`w` used directly**: Creates high-frequency variation in x-direction
  - Vertical "brushing lines"
  - Every pixel in x can differ

- **`h * 0.1` and `int()`**: Creates low-frequency variation in y-direction
  - Only changes every 10 pixels in y
  - Horizontal consistency
  - `int(h*0.1)` groups 10 rows together

**Result**: Anisotropic texture - variation along one axis, smooth along the other - exactly like real brushed metal!

**Answer 10.4:**
**XOR for weave** is perfect because:

```python
thread_x = (w % 8) < 4  # Thread runs horizontally
thread_y = (h % 8) < 4  # Thread runs vertically  
weave = thread_x ^ thread_y
```

**XOR creates the over-under pattern:**
- When `thread_x=1, thread_y=0`: XOR=1 (horizontal thread on top)
- When `thread_x=0, thread_y=1`: XOR=1 (vertical thread on top)
- When `thread_x=1, thread_y=1`: XOR=0 (both present → dark)
- When `thread_x=0, thread_y=0`: XOR=0 (gap → dark)

This creates the classic checkerboard weave where threads alternate going over/under.

**Answer 10.5:**
**Example: Reptile Scales**

I would combine:

1. **Voronoi (Lesson 8)**: Base scale shapes
   - Each cell = one scale
   - Use low RANDOMNESS for regular patterns (like snake)
   - Or high RANDOMNESS for irregular (like lizard)

2. **Radial gradient (Lesson 3)**: Within each scale
   - Brighter at center
   - Darker at edges
   - Creates 3D bump effect

3. **FBM noise (Lesson 6)**: Surface texture
   - Subtle variation within scales
   - Roughness/aging
   - Octaves=2-3 for fine detail

4. **Edge detection (Lesson 8)**: Scale boundaries
   - Darken at cell edges
   - Creates separation between scales
   - Maybe add slight color shift

Code structure:
```python
# Find nearest Voronoi cell (scale)
nearest_dist, second_dist, cell_id = voronoi(w, h)

# Radial gradient within scale (from cell center)
scale_gradient = 1.0 - (nearest_dist / SCALE_SIZE)

# Surface texture
noise = fbm_noise(w, h, octaves=2)

# Edge darkening
edge = (second_dist - nearest_dist) < 2

# Combine
base_color = (cell_id % 3) * 30 + 100  # Slight color variation
brightness = scale_gradient * (1 - noise * 0.3)
if edge:
    brightness *= 0.3  # Darken edges

color = int(base_color * brightness)
```

---

## Bonus Challenge Answers

**Challenge 1: Brick Wall**

```python
WIDTH = 200
HEIGHT = 200
BRICK_WIDTH = 40
BRICK_HEIGHT = 20
MORTAR_WIDTH = 2

print(f"P3\n{WIDTH} {HEIGHT}\n255")

for h in range(HEIGHT):
    for w in range(WIDTH):
        # Which row of bricks?
        brick_row = h // (BRICK_HEIGHT + MORTAR_WIDTH)
        
        # Offset every other row
        offset = (brick_row % 2) * (BRICK_WIDTH // 2)
        adjusted_w = w + offset
        
        # Position within the brick pattern
        x_in_pattern = adjusted_w % (BRICK_WIDTH + MORTAR_WIDTH)
        y_in_pattern = h % (BRICK_HEIGHT + MORTAR_WIDTH)
        
        # Is this pixel mortar?
        is_horizontal_mortar = y_in_pattern >= BRICK_HEIGHT
        is_vertical_mortar = x_in_pattern >= BRICK_WIDTH
        
        if is_horizontal_mortar or is_vertical_mortar:
            # Mortar - light gray
            r = g = b = 180
        else:
            # Brick - reddish with slight variation
            brick_x = adjusted_w // (BRICK_WIDTH + MORTAR_WIDTH)
            brick_y = brick_row
            variation = hash((brick_x, brick_y)) % 30
            
            r = 180 + variation
            g = 80 + variation // 2
            b = 60 + variation // 3
        
        print(f"{r} {g} {b}")
```

**Key insights:**
- Use `(brick_row % 2)` to alternate row offsets
- Add MORTAR_WIDTH to both dimensions for spacing
- Check position within pattern for mortar vs brick

**Challenge 2: Spiral Explanation**

```python
spiral = (int(dist * 0.1 + angle * 2) % 10)
```

**How it works:**
- `dist * 0.1`: Radial component - increases slowly with distance
- `angle * 2`: Angular component - `* 2` means **2 full rotations** per 2π radians
  - Without `* 2`: one spiral arm per revolution
  - With `* 2`: two spiral arms per revolution
  - With `* 3`: three spiral arms, etc.

**The sum creates a spiral because:**
- As you move outward (dist increases), the value increases
- As you rotate (angle changes), the value also increases
- The combination creates a path that winds outward
- Modulo 10 creates 10 distinct spiral bands

**Changing `* 2` to other values:**
- `* 1`: Looser spiral (one arm)
- `* 3`: Tighter spiral (three arms)
- `* 0.5`: Very loose spiral (half arm per revolution)

**Challenge 3: Performance Calculation**

Given:
- Image size: 1000 × 1000 = 1,000,000 pixels
- Octaves: 4
- Hash lookups per octave: 4 (for bilinear interpolation corners)

**Calculation:**
```
Total = pixels × octaves × lookups_per_octave
Total = 1,000,000 × 4 × 4
Total = 16,000,000 hash calculations
```

**Additional consideration:**
If you're using smoothstep or other interpolation, you're also doing:
- 1,000,000 × 4 × 4 multiplications (for weights)
- 1,000,000 × 4 × 3 additions (for bilinear combination)

Total operations: ~40-50 million for the full texture.

**Challenge 4: Debug Concentric Squares**

**The bugs:**

```python
# BUGGY CODE
dist = max(abs(w - CENTER_X), abs(h - CENTER_Y))
ring = dist % 20
color = ring * 255 / 20  # BUG 1: Float division
```

**Problems:**

1. **Float division**: `255 / 20 = 12.75` (float)
   - Should be integer division: `// 20`
   - Or multiply first: `(ring * 255) // 20`

2. **Color range**: Even with integer division, max color is `19 * 255 // 20 = 242`
   - Doesn't reach white (255)

**Fixed code:**

```python
dist = max(abs(w - CENTER_X), abs(h - CENTER_Y))
ring = dist % 20
color = (ring * 256) // 20  # Or use min(255, ...)

# OR for alternating black/white squares:
square_num = dist // 20
color = (square_num % 2) * 255

print(f"{color} {color} {color}")
```

**Challenge 5: Masked Stripes**

```python
WIDTH = 200
HEIGHT = 200
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

print(f"P3\n{WIDTH} {HEIGHT}\n255")

for h in range(HEIGHT):
    for w in range(WIDTH):
        # Radial gradient (0 at center, 255 at edges)
        dx = w - CENTER_X
        dy = h - CENTER_Y
        dist = (dx * dx + dy * dy) ** 0.5
        max_dist = (CENTER_X ** 2 + CENTER_Y ** 2) ** 0.5
        gradient = int((dist / max_dist) * 255)
        
        # Vertical stripes
        stripe_pattern = (w % 20) * 255 // 20
        
        # Mask: stripes only visible where gradient is bright (outer regions)
        # Use gradient as alpha/opacity
        alpha = gradient / 255.0
        
        # Blend: background black, stripes appear based on alpha
        color = int(stripe_pattern * alpha)
        
        print(f"{color} {color} {color}")
```

**Key technique:**
- Use one pattern as "alpha" (opacity)
- Multiply second pattern by alpha
- Result: second pattern "fades in" based on first pattern

---

## Conceptual Question Answers

**Concept 1: Modulo vs Hash**

**Fundamental difference:**

**Modulo:**
- **Deterministic and periodic**: Same input always gives same output, repeats predictably
- **Local**: Nearby coordinates give nearby values (continuity)
- **Structured**: Creates geometric patterns (stripes, rings, grids)
- **Fast**: Simple arithmetic operation
- **Example**: `x % 20` creates stripes with perfect 20-pixel period

**Hash:**
- **Deterministic but chaotic**: Same input gives same output, but no apparent pattern
- **Non-local**: Nearby coordinates give unrelated values (discontinuous)
- **Random-looking**: Creates noise, no geometric structure
- **Slower**: Multiple operations, bit mixing
- **Example**: `hash(x, y)` creates white noise texture

**When to use each:**
- Modulo: Geometric patterns, regular textures, mathematical art
- Hash: Organic textures, randomness, breaking up regularity

**Concept 2: Why Combine Multiple Techniques?**

Natural textures are **multi-scale and heterogeneous**:

1. **Multiple scales**: Wood has rings (large) AND grain (small)
   - Single pattern = single scale
   - Combined patterns = multiple scales → natural

2. **Structure + randomness**: Stone has chunks (structured) AND roughness (random)
   - Pure modulo = too regular
   - Pure hash = too chaotic
   - Combined = structured randomness → realistic

3. **Different qualities**: Metal has direction (anisotropic) AND shininess (isotropic)
   - Need different techniques for different properties

4. **Breaking uniformity**: Pure repetition looks fake
   - Add noise to geometric patterns
   - Add structure to random noise
   - Result: "controlled chaos" that appears natural

**Example: Tree bark**
- Voronoi: Large crack patterns
- Noise: Surface texture
- Vertical bias: Growth direction
- Color variation: Age/weathering

No single technique captures all these aspects.

**Concept 3: Integer vs Float Division**

**Tradeoff:**

**Integer division (`//`):**
- **Pros:**
  - Faster (no floating point)
  - No precision loss in accumulation
  - Predictable truncation
  - Good for discrete patterns (stripes, checkers)
  
- **Cons:**
  - Can't represent fractional values
  - Loses precision when needed
  - Must be careful with order of operations

**Float division (`/`):**
- **Pros:**
  - Preserves precision
  - Good for gradients, smooth transitions
  - Natural for interpolation
  
- **Cons:**
  - Slower
  - Floating point errors accumulate
  - Need to convert back to int for pixels
  - Can create unexpected artifacts

**Best practice:**
```python
# Good: multiply first (preserves precision), then integer divide
color = (value * 255) // max_value

# Bad: float division might lose precision
color = int(value * 255 / max_value)

# Worse: integer divide first (loses precision)
color = (value // max_value) * 255  # Almost always 0!
```

**Concept 4: Bitwise vs Arithmetic Operations**

**When to choose bitwise:**

1. **Fractal/self-similar patterns needed**:
   - XOR creates Sierpinski-like patterns
   - Automatic multi-scale structure

2. **Performance critical**:
   - Bitwise is faster than arithmetic
   - Especially for powers of 2

3. **Binary decision making**:
   - AND for "both must be true"
   - OR for "either must be true"
   - XOR for "exactly one must be true"

4. **Working with binary data/flags**:
   - Masking specific bits
   - Combining bit fields

**When to choose arithmetic:**

1. **Natural phenomena simulation**:
   - Addition for wave interference
   - Multiplication for attenuation
   - Sin/cos for actual waves

2. **Color blending/mixing**:
   - Arithmetic gives intuitive results
   - Bitwise can create unexpected colors

3. **Gradients and smooth transitions**:
   - Arithmetic interpolation is smooth
   - Bitwise creates discrete jumps

4. **Human-intuitive control**:
   - "Increase brightness by 20%" → arithmetic
   - "Create fractal pattern" → bitwise

**Example decision:**
- Marble texture: Arithmetic (smooth, flowing)
- Circuit board: Bitwise (grid-like, discrete)

**Concept 5: Approaching Novel Patterns**

**The systematic approach:**

1. **Analyze the pattern visually:**
   - Is it periodic? → Modulo
   - Is it random? → Hash
   - Is it fractal? → XOR or recursion
   - Is it smooth? → Interpolation
   - Does it have orientation? → Use angle/rotation
   - Multiple scales? → Octaves

2. **Break down into components:**
   - What's the large-scale structure?
   - What's the fine detail?
   - What's the color scheme?
   - Are there edges/boundaries?

3. **Map to known techniques:**
   - Cells/chunks → Voronoi
   - Stripes/bands → Modulo
   - Rings → Radial distance
   - Noise → Hash + interpolation
   - Directional → Anisotropic (different x/y behavior)

4. **Build incrementally:**
   ```python
   # Step 1: Base structure
   base = create_base_pattern(x, y)
   
   # Step 2: Add detail
   detail = add_noise(x, y)
   
   # Step 3: Combine
   result = combine(base, detail)
   
   # Step 4: Color mapping
   color = map_to_color(result)
   ```

5. **Iterate and refine:**
   - Test each component separately
   - Adjust parameters
   - Add/remove layers as needed

**Example: "Lightning bolt" pattern**

Analysis:
- Branching structure → Recursive/fractal
- Jagged edges → Random walk
- Bright center, dark edges → Distance from path
- Glow effect → Falloff function

Approach:
```python
# 1. Create main bolt path (random walk)
path = random_walk_from(start, end)

# 2. Add branches (recursively)
for point in path:
    if random() < branch_probability:
        create_branch(point)

# 3. For each pixel, find distance to nearest path
dist = min_distance_to_path(x, y, path)

# 4. Brightness based on distance
brightness = 255 / (1 + dist ** 2)  # Inverse square falloff
```

**The key insight:** Any pattern is just a function f(x, y) → color. Your job is to construct that function by combining the primitives you've learned.

---

**End of Answer Key**

Remember: These are reference answers, but your explanations in your own words show true understanding. The goal isn't to match these answers exactly, but to demonstrate you grasp the underlying concepts and can apply them creatively!