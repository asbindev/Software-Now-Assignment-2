import turtle

def koch_indent(t, length, depth):
    """Recursive edge: inward indentation using the Koch turn sequence."""
    if depth == 0:
        t.forward(length)
        return
    seg = length / 3.0
    koch_indent(t, seg, depth - 1)
    t.left(60)            # toward interior when polygon is traced CCW
    koch_indent(t, seg, depth - 1)
    t.right(120)          # apex turn
    koch_indent(t, seg, depth - 1)
    t.left(60)            # restore heading
    koch_indent(t, seg, depth - 1)

def draw_inward_koch_polygon(sides, side_length, depth):
    if sides < 3:
        raise ValueError("Number of sides must be >= 3")
    if side_length <= 0:
        raise ValueError("Side length must be > 0")
    if depth < 0:
        raise ValueError("Recursion depth must be >= 0")

    screen = turtle.Screen()
    screen.title("Inward-Koch Polygon")
    screen.tracer(0, 0)  # batch drawing for speed

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.penup()
    # shift start so drawing stays on-screen for common inputs
    t.goto(-side_length * 0.5, side_length * 0.3)
    t.setheading(0)
    t.pendown()

    exterior = 360.0 / sides  # CCW traversal keeps interior on the left
    for _ in range(sides):
        koch_indent(t, side_length, depth)
        t.left(exterior)

    screen.update()
    turtle.done()

def main():
    try:
        n = int(input("Enter the number of sides: ").strip())
        L = float(input("Enter the side length (pixels): ").strip())
        d = int(input("Enter the recursion depth: ").strip())
        draw_inward_koch_polygon(n, L, d)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
