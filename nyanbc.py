#!/usr/bin/env python3

# yes, I know this code is mostly all wrong, but consider the topic
# and also consider I have had considerable to drink.

import cairocffi as cairo  # libffi-dev
import math
import random

random.seed(1337 + 1)
TAU = 2 * math.pi  # pi must die


def main():
    nyan = cairo.ImageSurface.create_from_png('nyan.png')
    frames = 100

    arcs = 600
    dtheta = TAU / (frames - 1)

    sparkles = [
        (120, 100, 5, 20),
        (100, 50, 5, 20),
        (80, 0, 5, 20),
        (75, -30, 5, 20),
        (80, -40, 5, 20),
        (85, 40, 5, 20),
        (100, -50, 5, 20),
        (120, -100, 5, 20),
    ]

    colours = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 0), (0, 1, 1)]

    for i in range(frames):
        spark_idx = round(len(colours) * i / frames) % len(colours)
        sur = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 1000)
        n_w = nyan.get_width()
        n_h = nyan.get_height()

        cr = cairo.Context(sur)
        cr.set_line_width(20)
        cr.set_source_rgb(0.2, 0.2, 0.2)
        cr.move_to(0, 0)
        cr.rectangle(0, 0, sur.get_width(), sur.get_height())
        cr.fill()

        theta = i * dtheta
        darc_theta = (math.pi * 2) / (arcs - 1)
        last_x, last_y = 500, 900
        for j in range(arcs):
            arc_theta = j * darc_theta
            arc_x = 100 + (math.sin(arc_theta) + 1) * 400
            arc_y = 100 + (math.cos(3 * arc_theta) + 1) * 400

            r = math.sin(arc_theta - theta)**2
            g = math.cos(arc_theta - theta)**2
            b = 0.5 + math.sin(arc_theta - theta)**2

            cr.set_source_rgb(r, g, b)
            cr.move_to(last_x, last_y)
            cr.line_to(arc_x, arc_y)
            cr.stroke()
            last_x, last_y = arc_x, arc_y

        x = 100 + (math.sin(theta) + 1) * 400
        y = 100 + (math.cos(3 * theta) + 1) * 400

        cr.set_source_rgb(r, g, b)
        ny_cr = cairo.Context(sur)
        ny_cr.set_source_surface(nyan, x - n_w / 2, y - n_h / 2)
        ny_cr.rectangle(x - n_w / 2, y - n_w / 2, n_w * 2, n_h * 2)

        cr.set_line_width(4)
        for idx, (dx, dy, sz, fuzz) in enumerate(sparkles):
            cr.set_source_rgb(*colours[(idx + spark_idx) % len(colours)])
            xf = random.randint(0, fuzz)
            yf = random.randint(0, fuzz)
            cr.move_to(x + xf - dx - sz, y + yf - dy)
            cr.line_to(x + xf - dx + sz, y + yf - dy)
            cr.stroke()

            cr.move_to(x + xf - dx, y + yf - dy - sz)
            cr.line_to(x + xf - dx, y + yf - dy + sz)
            cr.stroke()

        ny_cr.fill()
        sur.write_to_png('out/frame%04d.png' % (i))


if __name__ == '__main__':
    main()
