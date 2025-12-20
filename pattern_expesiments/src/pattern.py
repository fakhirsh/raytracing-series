WIDTH = 800
HEIGHT = 600

def main():
    print(f"P3\n{WIDTH} {HEIGHT}\n255")

    for h in range(HEIGHT):
        for w in range(WIDTH):
            pattern = (w) % 100
            r = (pattern * 255) // 100
            g = 0
            b = 0

            print(f"{r} {g} {b}")

if __name__ == "__main__":
    main()