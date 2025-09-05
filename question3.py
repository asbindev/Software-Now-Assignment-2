import turtle

def koch_indent(t, length, depth):
    """
    Recursive function to draw an inward Koch indentation on one side of a polygon.

    Args:
        t (turtle.Turtle): The turtle object used for drawing.
        length (float): The length of the current segment.
        depth (int): The recursion depth. Higher depth = more detailed fractal.
    """
    if depth == 0:  # Base case: simply draw a straight line
        t.forward(length)
        return

    seg = length / 3.0  # Divide segment into three parts
    # Apply Koch indentation pattern recursively
    koch_indent(t, seg, depth - 1)
    t.left(60)   # Turn inward
    koch_indent(t, seg, depth - 1)
    t.right(120) # Create apex
    koch_indent(t, seg, depth - 1)
    t.left(60)   # Restore heading
    koch_indent(t, seg, depth - 1)

def draw_inward_koch_polygon(sides, side_length, depth):
    """
    Draws a polygon with inward Koch fractal edges.

    Args:
        sides (int): Number of sides of the polygon (>= 3).
        side_length (float): Length of each polygon side (> 0).
        depth (int): Recursion depth for fractal edges (>= 0).
    """
    # Validate inputs
    if not isinstance(sides, int) or sides < 3:
        raise ValueError("Number of sides must be an integer >= 3")
    if not (isinstance(side_length, (int, float)) and side_length > 0):
        raise ValueError("Side length must be a positive number")
    if not isinstance(depth, int) or depth < 0:
        raise ValueError("Recursion depth must be a non-negative integer")

    # Setup turtle screen
    screen = turtle.Screen()
    screen.title("Polygon")
    screen.tracer(0, 0)  # Speed up drawing by disabling auto-refresh

    # Create turtle object
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.penup()
    # Shift starting position so drawing fits nicely on screen
    t.goto(-side_length * 0.5, side_length * 0.3)
    t.setheading(0)
    t.pendown()

    # Calculate exterior angle (for CCW polygon traversal)
    exterior = 360.0 / sides
    for _ in range(sides):
        koch_indent(t, side_length, depth)
        t.left(exterior)

    screen.update()  # Refresh screen after full drawing
    turtle.done()

def main():
    """Main function to get user input and draw the fractal polygon."""
    try:
        # Take user input with safe parsing
        n_str = input("Enter the number of sides (>= 3): ").strip()
        L_str = input("Enter the side length (pixels > 0): ").strip()
        d_str = input("Enter the recursion depth (>= 0): ").strip()

        # Ensure inputs can be converted correctly
        if not n_str.isdigit() or int(n_str) < 3:
            raise ValueError("Number of sides must be an integer >= 3")
        if not L_str.replace('.', '', 1).isdigit() or float(L_str) <= 0:
            raise ValueError("Side length must be a positive number")
        if not d_str.isdigit() or int(d_str) < 0:
            raise ValueError("Recursion depth must be a non-negative integer")

        # Convert inputs
        n = int(n_str)
        L = float(L_str)
        d = int(d_str)

        # Draw the fractal polygon
        draw_inward_koch_polygon(n, L, d)

    except ValueError as ve:
        print("Input Error:", ve)
    except turtle.Terminator:
        print("Turtle graphics window was closed unexpectedly.")
    except Exception as e:
        print("Unexpected Error:", e)

if __name__ == "__main__":
    main()
