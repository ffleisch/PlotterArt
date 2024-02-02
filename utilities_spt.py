import svgpathtools as spt


def make_viewbox(paths_and_stuff,margin_size=0.1):
    xmin, xmax, ymin, ymax = spt.paths2svg.big_bounding_box(paths_and_stuff)
    dx = xmax - xmin
    dy = ymax - ymin

    if dx == 0:
        dx = 1
    if dy == 0:
        dy = 1
    xmin -= margin_size*dx
    ymin -= margin_size*dy
    dx += 2*margin_size*dx
    dy += 2*margin_size*dy
    return "%s %s %s %s" % (xmin, ymin, dx, dy)
