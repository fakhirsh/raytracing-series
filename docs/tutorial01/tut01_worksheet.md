# Modulo Arithmetic & Visual Patterns: Worksheet

Test your understanding of procedural texture generation with these exercises.

---

## Exercise 1: Vertical Stripes - Understanding the Fundamentals

**Question 1.1:** If you want to create 5 vertical stripes across a 200-pixel-wide image, what value should `STRIPE_WIDTH` be?

**Question 1.2:** Given the code `color = (pattern * 255) // 20` where `pattern` ranges from 0-19:
- What is the maximum color value this produces?
- Why doesn't it reach 255?
- How would you modify this to ensure the maximum value is exactly 255?

**Question 1.3:** What's the difference between these two approaches for creating stripes?
```python
# Approach A
color = ((w % 20) * 255) // 20

# Approach B
color = (w % 20) * 255 // 20
```
Which one is correct and why?

**Question 1.4:** If you write `pattern = h % 20` instead of `pattern = w % 20`, what changes in the output? Draw or describe what you'd see.

**Question 1.5:** You want alternating black and white stripes (not gradients). The stripe width should be 15 pixels. Write the code to generate this pattern.

**Question 1.6:** Draw diagonal stripes with alternating colors (e.g., red and blue) where each stripe is 30 pixels wide. Write the code.

**Question 1.7:** Try the following patterns and describe what you see:
```python
pattern1 = (w + h) % 40
pattern2 = (w - h) % 40
pattern3 = (w * h) % 40
pattern3 = (w ^ h) % 40
```

---

## Exercise 2: Checkerboards - The Parity Trick

**Question 2.1:** Explain in your own words why `(tile_x + tile_y) % 2` creates a checkerboard pattern. What happens at these coordinates?
- (0, 0)
- (0, 1)
- (1, 0)
- (1, 1)

**Question 2.2:** What pattern does `(tile_x - tile_y) % 2` create? How is it different from `(tile_x + tile_y) % 2`?

**Question 2.3:** You want a checkerboard where each square is 25×25 pixels in a 200×200 image. Write the complete calculation for:
- Finding which tile a pixel at (137, 89) belongs to
- Determining if that tile should be black or white

**Question 2.4:** What's the effect of using `% 3` instead of `% 2` in the checkerboard formula? How many colors would you need?

**Question 2.5:** The "brick" pattern uses this formula:
```python
offset = (tile_y % 2) * (TILE_SIZE // 2)
adjusted_x = (w + offset) // TILE_SIZE
pattern = (adjusted_x + tile_y) % 2
```
Explain what the `offset` variable does and why it creates a brick-like appearance.

**Question 2.6:** Can you draw the squares at an angle (like a diamond shape) instead of axis aligned boxes? Can you draw at any angle? Write code.

**Question 2.7:** Can you modify the brick pattern to create a "herringbone" pattern? Describe your approach.

---

## Exercise 3: Radial Patterns - Distance Mathematics

**Question 3.1:** For a point at (150, 120) with center at (100, 100):
- Calculate `dx` and `dy`
- Calculate `dist_squared`
- If `RING_THICKNESS = 400`, which ring number is this pixel in?

**Question 3.2:** Compare these two approaches:
```python
# Approach A
dist = int((dx * dx + dy * dy) ** 0.5)
ring = (dist // 10) % NUM_RINGS

# Approach B
dist_squared = dx * dx + dy * dy
ring = (dist_squared // 400) % NUM_RINGS
```
Which creates more evenly-spaced rings? Which creates rings that get wider as you move outward?

**Question 3.3:** Why might you prefer non-uniform ring spacing (using squared distance) for certain visual effects?

**Question 3.4:** If you want to create a spiral pattern, you need both radial distance and angular information. Given that `angle = math.atan2(dy, dx)` returns a value from -π to π, how would you normalize this to a 0-255 range?

**Question 3.5:** Write code to create a "target" pattern: alternating black and white rings where each ring is exactly 20 pixels wide (uniform spacing).

---

## Exercise 4: XOR Patterns - Binary Operations

**Question 4.1:** Calculate by hand (showing your binary work):
- `5 ^ 3 = ?`
- `12 ^ 9 = ?`
- `255 ^ 0 = ?`

**Question 4.2:** In the pattern `w ^ h`, bit position 0 (LSB) creates patterns that alternate every _____ pixel(s), while bit position 3 creates patterns that alternate every _____ pixel(s).

**Question 4.3:** What's the visual difference between these three patterns?
- `w ^ h`
- `w & h`
- `w | h`

**Question 4.4:** If you want to see ONLY the pattern created by bit position 4 (and ignore all other bits), what formula would you use?

**Question 4.5:** The tutorial mentions XOR creates "self-similar patterns at power-of-2 scales." What does this mean? Why does it only work for power-of-2 scales?

**Question 4.6:** For the Sierpinski triangle approximation using `(w & h) == 0`, explain why this works. What's the connection between the AND operation and Pascal's triangle?

---

## Exercise 5: Interference - Wave Interactions

**Question 5.1:** Given two waves:
```python
wave1 = (w * 3) % 17
wave2 = (h * 5) % 13
```
What is the LCM (Least Common Multiple) of 17 and 13? How many pixels until the combined pattern repeats?

**Question 5.2:** Why does using prime numbers for periods create more interesting interference patterns?

**Question 5.3:** Compare these three interference modes:
```python
additive = (wave1 + wave2) % pattern_period
multiplicative = (wave1 * wave2) % 256
difference = abs(wave1 - wave2)
```
Which one creates the brightest spots where both waves are at maximum? Which creates dark spots where waves cancel?

**Question 5.4:** What's the purpose of `FREQ1` and `FREQ2` parameters? How do they differ from `PERIOD1` and `PERIOD2`?

**Question 5.5:** You want to create a moiré pattern (interference between two similar frequencies). Should the two periods be:
- Very different (like 7 and 29)?
- Very similar (like 17 and 19)?
- Identical (both 20)?

Explain your reasoning.

---

## Exercise 6: Hash Functions - Controlled Randomness

**Question 6.1:** Why does a good hash function for texture generation need to:
- Combine both x and y coordinates
- Use large prime numbers
- Mix bits from different positions

**Question 6.2:** In the hash function:
```python
n = x + y * 57
```
Why multiply y by a number (57) instead of just adding `x + y`?

**Question 6.3:** Compare the visual results of:
- `SCALE = 2` with `OCTAVES = 1`
- `SCALE = 8` with `OCTAVES = 1`
- `SCALE = 8` with `OCTAVES = 3`

Describe what changes in each case.

**Question 6.4:** If `PERSISTENCE = 0.5`, how much does the third octave contribute relative to the first octave?

**Question 6.5:** What's the purpose of the `smoothstep` function in interpolation? What would happen if you used linear interpolation instead?

**Question 6.6:** In bilinear interpolation, you have four corner values (v00, v10, v01, v11) and position weights (sx, sy). Write the formula for the final interpolated value in your own words or pseudocode.

---

## Exercise 7: Cellular Automata - Emergent Patterns

**Question 7.1:** For Rule 30, calculate what happens to the following cell configurations:
- Left=1, Center=1, Right=1 → ?
- Left=0, Center=1, Right=0 → ?
- Left=0, Center=0, Right=0 → ?

(Hint: Rule 30 in binary is 00011110. The index is formed as `left<<2 | center<<1 | right`)

**Question 7.2:** What's the difference between `WRAP = True` and `WRAP = False` in terms of pattern behavior at the edges?

**Question 7.3:** Rule 90 produces a Sierpinski triangle pattern. Given what you learned about XOR patterns in Exercise 4, why do you think Rule 90 creates this fractal pattern? (Research if needed: Rule 90's formula is `left ^ right`)

**Question 7.4:** If you start with a "single" initial pattern (one cell on in the center) versus a "random" initial pattern, how does this affect the evolution under Rule 30?

**Question 7.5:** Why are elementary cellular automata limited to rules 0-255? How does the rule number encode the complete behavior?

---

## Exercise 8: Voronoi - Distance-Based Patterns

**Question 8.1:** For a pixel at (50, 50) with three seed points at (30, 30), (70, 40), and (40, 70), calculate which seed is closest using:
- Euclidean distance
- Manhattan distance
- Chebyshev distance

**Question 8.2:** What visual effect does changing the distance metric have on cell shapes?
- Euclidean → ?-shaped cells
- Manhattan → ?-shaped cells  
- Chebyshev → ?-shaped cells

**Question 8.3:** The edge detection uses:
```python
edge_strength = 1.0 - (second_dist - nearest_dist) / GRID_SIZE
```
Explain why `second_dist - nearest_dist` gives information about edge locations.

**Question 8.4:** If `RANDOMNESS = 0`, what pattern would you get? If `RANDOMNESS = 1`, what changes?

**Question 8.5:** Write code to create a Voronoi pattern where cells are colored based on their distance from the image center (not their cell ID).

---

## Exercise 9: Fractal Subdivision - Recursive Patterns

**Question 9.1:** In a 256×256 image with `MAX_DEPTH = 6` and `MIN_SIZE = 4`:
- What's the size of regions at depth 0?
- What's the size of regions at depth 3?
- What's the size of regions at depth 6?

**Question 9.2:** Why must the image dimensions be powers of 2 for clean subdivision patterns?

**Question 9.3:** The `should_subdivide` function uses:
```python
threshold = 0.5 + depth * 0.1
```
Why does the threshold increase with depth? What visual effect does this create?

**Question 9.4:** What's the difference between coloring by:
- `"depth"` → Shows recursion level
- `"size"` → Shows region area
- `"position"` → Shows spatial location

Describe what each would look like.

**Question 9.5:** If you wanted to create a "city block" pattern (like looking down at buildings from above), how could you modify the subdivision algorithm?

---

## Exercise 10: Complex Textures - Integration

**Question 10.1:** For the "stone" texture, three techniques are combined:
- Voronoi cells
- FBM noise
- Crack detection

Explain the role each plays in creating the final stone appearance.

**Question 10.2:** Wood grain uses:
```python
warp = math.sin(w * 0.05) * 10
ring_pos = (dist_from_center + warp) * 0.5
```
Why is warping necessary for realistic wood? What would it look like without warping?

**Question 10.3:** The brushed metal texture uses:
```python
brush = hash(f"{w},{int(h*0.1)}") % 40
```
Why is `h` multiplied by 0.1 and converted to int, while `w` is used directly?

**Question 10.4:** For fabric, the weave pattern uses:
```python
weave = thread_x ^ thread_y
```
Why is XOR appropriate here? What pattern does it create?

**Question 10.5:** Design your own texture! Choose one:
- Reptile scales
- Rust on metal
- Marble
- Water ripples

Describe which 3-4 techniques from lessons 1-9 you would combine and how.

---

## Bonus Challenge Questions

**Challenge 1:** Create a "brick wall" pattern where:
- Each brick is 40×20 pixels
- Every other row is offset by 20 pixels
- There's a 2-pixel gap between bricks (mortar)

Write the complete algorithm.

**Challenge 2:** Explain why this formula creates a spiral:
```python
dist = math.sqrt(dx*dx + dy*dy)
angle = math.atan2(dy, dx)
spiral = (int(dist * 0.1 + angle * 2) % 10)
```
What does the `* 2` do to the angle term?

**Challenge 3:** Performance question: You need to generate a 1000×1000 image with Perlin noise (4 octaves). One octave requires 4 hash lookups per pixel. How many total hash calculations are needed?

**Challenge 4:** Debug this code - it's supposed to create concentric squares but doesn't work:
```python
dist = max(abs(w - CENTER_X), abs(h - CENTER_Y))
ring = dist % 20
color = ring * 255 / 20
```
What's wrong and how would you fix it?

**Challenge 5:** Combine two patterns:
- A radial gradient (dark center, bright edges)
- Vertical stripes (20 pixels wide)

Write code where the stripes are only visible in the bright regions (outer parts of the image).

---

## Conceptual Questions

**Concept 1:** What's the fundamental difference between how modulo creates patterns versus how hash functions create patterns?

**Concept 2:** Why do most natural-looking textures require multiple techniques combined rather than a single pattern?

**Concept 3:** Explain the tradeoff between using `//` (integer division) versus `/` (float division) in pattern generation.

**Concept 4:** When would you choose bitwise operations (`&`, `|`, `^`) over arithmetic operations (`+`, `-`, `*`)?

**Concept 5:** The tutorial emphasizes "every visual pattern is just a function from coordinates to color: f(x, y) → (r, g, b)". Given this insight, explain how you would approach creating a pattern you've never seen code for before.

---

**End of Worksheet**

Good luck! Remember: understanding the mechanics is more important than memorizing formulas. Focus on *why* things work, not just *that* they work.