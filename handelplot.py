

"""
Plot the Mandelbrot Set.
"""


from __future__ import division

import argparse
import math
import colorsys

import Tkinter


def decide_if_point_escapes(current_point):

    """
    Compute and return the number of iterations required for this point to
    escape the Mandelbrot Set, and the value of the point when the escape
    occurred. Otherwise, return -1 and the value of the point, signifying that
    the point is, in fact in the Set.
    """

    z_value = (0+0j)
    c_value = (current_point.real + (current_point.imag * 1j))

    for iteration_number in xrange(64):
        if z_value.real > 2 or z_value.imag > 2:
            return (z_value, iteration_number)
        else:
            z_value = (z_value**2) + c_value

    return (z_value, -1)


def colour_pixel(image, pos, colours):

    """
    Set pixel with co-ordinates given in pos to RGB colour given by colours.
    """

    h, s, v = colours
    x, y = pos

    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    image.put("#%02x%02x%02x" % (r * 255, g * 255, b * 255), (y, x))


def populate_pixel_array(image, diagram):

    """
    Populate pixels in 'image' with colours set according to how quickly each
    pixel's corresponding point escapes the Mandelbrot Set.
    """

    window_width, window_height = diagram.get_window_dimensions()
    real_axis_range, im_axis_range = diagram.get_axis_ranges()
    dx, dy = diagram.get_deltas()

    current_point = real_axis_range[0] + (im_axis_range[0] * 1j)

    for x_pixel in xrange(window_width):
        for y_pixel in xrange(window_height):
            escape_val, num_iterations = decide_if_point_escapes(current_point)
            if num_iterations != -1:

                # Alter hue in proportion to how quickly the point escapes the
                # Set and how large it grows
                hue = num_iterations + 1 - \
                        (math.log(math.log(abs(escape_val))) / math.log(2))
                hue = hue / 64

                colour_pixel(image, (y_pixel, x_pixel),
                             (hue, 1, 1))
            else:
                colour_pixel(image, (y_pixel, x_pixel), (0, 0, 0))

            current_point += (dy * 1j)
        current_point = (current_point.real + dx) + (im_axis_range[0] * 1j)


def create_parser():

    """
    Creates and returns an Argparse parser.
    """

    parser = argparse.ArgumentParser(description="Plot the Mandelbrot set")

    parser.add_argument("--width", default=750, type=int,
                        help="width of the window in pixels")
    parser.add_argument("--height", default=500, type=int,
                        help="height of the window in pixels")

    return parser


def motion(event, diagram):

    """
    Event handler for motion of the mouse over the diagram. Currently, this
    prints the co-ordiantes of the location of the mouse in terms of the Argand
    Diagram.
    """

    x, y = event.x, event.y
    dx, dy = diagram.get_deltas()
    real_range = diagram.get_real_range()
    im_range = diagram.get_im_range()

    # Components of the co-ordinates of the mouse's current location
    real_ordinate = real_range[0] + (x * dx)
    im_ordinate = im_range[1] - (y * dy)

    if im_ordinate >= 0:
        print str(real_ordinate) + "+" + str(im_ordinate) + "i"
    else:
        print str(real_ordinate) + str(im_ordinate) + "i"


class Diagram(object):

    """
    The Diagram class is used to represent Argand Diagram used to display the
    plot of the Mandelbrot Set.
    """

    def __init__(self, window_width, window_height):
        self.real_range = (-2, 1)
        self.im_range = (-1, 1)
        self.window_width = window_width
        self.window_height = window_height
        self.dx, self.dy = self.set_deltas()

    def set_deltas(self):

        """
        Sets self.dx and self.dy to be the size of the range covered by each
        pixel for the x and y axes.  I.e. 'dx' is the jump in value of the real
        component of the a point for every pixel moved in the positive x
        direction. 'dy' is the analaogue of 'dx' but for the imaginary (y)
        axis.
        """

        real_axis_range = self.real_range
        im_axis_range = self.im_range

        window_width = self.window_width
        window_height = self.window_height

        dx = abs(real_axis_range[1] - real_axis_range[0]) / window_width
        dy = abs(im_axis_range[1] - im_axis_range[0]) / window_height

        return (dx, dy)

    def get_real_range(self):
        """Getter for real_range"""
        return self.real_range

    def get_im_range(self):
        """Getter for im_range"""
        return self.im_range

    def get_axis_ranges(self):
        """Getter for ranges of both axes"""
        return (self.get_real_range(), self.get_im_range())

    def get_dx(self):
        """Getter for dx"""
        return self.dx

    def get_dy(self):
        """Getter for dy"""
        return self.dy

    def get_deltas(self):
        """Getter for both deltas"""
        return (self.get_dx(), self.get_dy())

    def get_window_height(self):
        """Getter for window_height"""
        return self.window_height

    def get_window_width(self):
        """Getter for window_width"""
        return self.window_width

    def get_window_dimensions(self):
        """Getter for both window dimensions"""
        return (self.get_window_width(), self.get_window_height())


def main():

    """
    Do Tkinter bootplating, and create blank image to be populated. Do this
    population and then plot the result.
    """

    root = Tkinter.Tk()

    parser = create_parser()
    args = parser.parse_args()

    window_width = args.width
    window_height = args.height

    diagram = Diagram(window_width, window_height)

    image = Tkinter.PhotoImage(height=window_height, width=window_width)
    populate_pixel_array(image, diagram)

    root.bind('<Motion>', lambda event: motion(event, diagram))

    label = Tkinter.Label(root, image=image)
    label.grid()

    root.iconbitmap('@images/handel_icon.xbm')
    root.title("HandelPlot")
    root.mainloop()


if __name__ == "__main__":
    main()
