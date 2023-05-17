def draw_corners(canvas, x1, y1, x2, y2, color='red', width=5, corner_length=30, tags=None):
    canvas.create_line(x1, y1, x1 + corner_length, y1, fill=color, width=width, tags=tags)  # Top/left corner
    canvas.create_line(x1, y1, x1, y1 + corner_length, fill=color, width=width, tags=tags)  # Top/left corner

    canvas.create_line(x2, y1, x2 - corner_length, y1, fill=color, width=width, tags=tags)  # Top/right corner
    canvas.create_line(x2, y1, x2, y1 + corner_length, fill=color, width=width, tags=tags)  # Top/right corner

    canvas.create_line(x1, y2, x1, y2 - corner_length, fill=color, width=width, tags=tags)  # Bottom/left corner
    canvas.create_line(x2, y2, x2, y2 - corner_length, fill=color, width=width, tags=tags)  # Bottom/right corner

    canvas.create_line(x1, y2, x1 + corner_length, y2, fill=color, width=width, tags=tags)  # Bottom/left corner
    canvas.create_line(x2, y2, x2 - corner_length, y2, fill=color, width=width, tags=tags)  # Bottom/right corner
