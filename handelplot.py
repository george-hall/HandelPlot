#! /usr/bin/env python


"""
Plot the Mandelbrot Set.
"""


from __future__ import division

import argparse
import math
import colorsys

import Tkinter


def iterate_point(current_point, iters_cutoff):

    """
    Compute and return the number of iterations required for this point to
    escape the Mandelbrot Set, and the value of the point when the escape
    occurred. Otherwise, return -1 and the value of the point, signifying that
    the point is, in fact in the Set.
    """

    z_value = (0+0j)
    c_value = (current_point.real + (current_point.imag * 1j))

    for iteration_number in xrange(iters_cutoff):
        if z_value.real > 2 or z_value.imag > 2:
            return (z_value, iteration_number)
        else:
            z_value = (z_value**2) + c_value

    return (z_value, -1)


def colour_pixel(image, pos, num_iterations, escape_val):

    """
    Set pixel with co-ordinates given in pos to colour reflecting how quickly
    that point escaped the Set.
    """

    if num_iterations != -1:

        # Alter hue in proportion to how quickly the point escapes the
        # Set and how large it grows
        h = num_iterations + 1 - \
                (math.log(math.log(abs(escape_val))) / math.log(2))
        (h, s, v) = (h/64, 1, 1)
    else:
        (h, s, v) = (0, 0, 0)

    x, y = pos

    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    image.put("#%02x%02x%02x" % (r * 255, g * 255, b * 255), (y, x))


def compute_mandelbrot_set(image, diagram):

    """
    Iterate over all pixels in the diagram, computing how quickly each point
    escapes the Set.
    """

    window_width, window_height = diagram.get_window_dimensions()
    real_axis_range, im_axis_range = diagram.get_axis_ranges()
    dx, dy = diagram.get_deltas()

    current_point = real_axis_range[0] + (im_axis_range[0] * 1j)

    for x_pixel in xrange(window_width):
        for y_pixel in xrange(window_height):
            # Number of iterations until point is deemed to not be in the Set:
            iters_cutoff = 256
            escape_val, num_iters = iterate_point(current_point, iters_cutoff)
            colour_pixel(image, (window_height - y_pixel, x_pixel), \
                         num_iters, escape_val)

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


def convert_to_diagram_coords(window_x, window_y, diagram):

    """
    Converts coordinate pairs from being given in the context of the window
    (i.e. being given in terms of pixels) to being given in the context of the
    Argand Diagram (i.e. being given as the (real, imaginary) pair which
    corresponds to the pixel's location in the Argand Diagram).
    """

    dx, dy = diagram.get_deltas()
    real_range = diagram.get_real_range()
    im_range = diagram.get_im_range()

    # Components of the co-ordinates of the mouse's current location
    real_ordinate = real_range[0] + (window_x * dx)
    im_ordinate = im_range[1] - (window_y * dy)

    return (real_ordinate, im_ordinate)


def convert_real_im_to_str(real, imaginary):

    """
    Converts a (real, imaginary) pair to a string representation.
    """

    if imaginary >= 0:
        return str(real) + "+" + str(imaginary) + "i"
    else:
        return str(real) + str(imaginary) + "i"


def motion(event, diagram, current_pos_str):

    """
    Event handler for motion of the mouse over the diagram. Currently, this
    prints the co-ordiantes of the location of the mouse in terms of the Argand
    Diagram.
    """

    real_ordinate, im_ordinate = convert_to_diagram_coords(event.x,
                                                           event.y,
                                                           diagram)

    # Update current position label to display mouse's new position
    new_location_str = convert_real_im_to_str(real_ordinate, im_ordinate)
    current_pos_str.set(new_location_str)


class Diagram(object):

    """
    The Diagram class is used to represent Argand Diagram used to display the
    plot of the Mandelbrot Set.
    """

    class UserDrawnRectangle(object):

        """
        Class to represent the rectangle currently being drawn by the user.
        """

        def __init__(self, canvas, start_x, start_y):
            self.start_x = start_x
            self.start_y = start_y
            self.rect_object = canvas.create_rectangle(self.get_start_x(),
                                                            self.get_start_y(),
                                                            self.get_start_x(),
                                                            self.get_start_y())

        def get_start_x(self):
            """Getter for the x ordinate of where the rectangle was started"""
            return self.start_x

        def get_start_y(self):
            """Getter for the y ordinate of where the rectangle was started"""
            return self.start_y

        def get_rect_object(self):
            """Getter for the rectangle object itself"""
            return self.rect_object

    def __init__(self, window_width, window_height):
        self.real_range = (-2, 1)
        self.im_range = (-1, 1)
        self.zoom_list = [(self.real_range, self.im_range)]
        self.window_width = window_width
        self.window_height = window_height
        self.set_deltas()
        self.dx, self.dy = self.get_deltas()
        self.rect = None

    def create_user_drawn_rect(self, canvas, start_x, start_y):

        """
        Creates an instance of class UserDrawnRectangle and stores it at
        self.rectangle.
        """

        self.rect = self.UserDrawnRectangle(canvas, start_x, start_y)

    def get_user_drawn_rect(self):
        """Getter for user drawn rectangle"""
        return self.rect

    def append_to_zoom_list(self, real_range, im_range):
        """Append current axis ranges to zoom list"""
        self.zoom_list.append((real_range, im_range))

    def revert_to_prev_zoom(self):
        """
        Revert to previous zoom level by removing the final element from
        zoom_list.
        """
        self.set_zoom_list(self.get_zoom_list()[:-1])

    def set_zoom_list(self, new_zoom_list):
        self.zoom_list = new_zoom_list

    def set_deltas(self):

        """
        Sets self.dx and self.dy to be the size of the range covered by each
        pixel for the x and y axes.  I.e. 'dx' is the jump in value of the real
        component of the a point for every pixel moved in the positive x
        direction. 'dy' is the analaogue of 'dx' but for the imaginary (y)
        axis.
        """

        real_axis_range = self.get_real_range()
        im_axis_range = self.get_im_range()

        window_width = self.window_width
        window_height = self.window_height

        self.dx = abs(real_axis_range[1] - real_axis_range[0]) / window_width
        self.dy = abs(im_axis_range[1] - im_axis_range[0]) / window_height

    def get_real_range(self):
        """Getter for real_range"""
        return self.get_zoom_list()[-1][0]

    def get_im_range(self):
        """Getter for im_range"""
        return self.get_zoom_list()[-1][1]

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

    def get_zoom_list(self):
        return self.zoom_list


def zoom_image(diagram, image):
    diagram.set_deltas()
    compute_mandelbrot_set(image, diagram)


def remove_rect(diagram, canvas):
    if diagram.get_user_drawn_rect() is not None:
        canvas.delete(diagram.get_user_drawn_rect().get_rect_object())
        diagram.rect = None


def button_1_press(event, diagram, canvas):

    """
    Event handler for the left mouse button being pressed. This function
    creates a rectangle at the location of the click, which can be expanded by
    the user dragging the mouse with the button held.
    """

    diagram.create_user_drawn_rect(canvas, event.x, event.y)


def button_1_motion(event, diagram, canvas, rect_pos_str):

    """
    Event handler for the mouse being dragged with button 1 held. This expands
    the rectangle created when the button was first pressed.
    """

    rect = diagram.get_user_drawn_rect()
    canvas.coords(rect.get_rect_object(), rect.get_start_x(),
                  rect.get_start_y(), event.x, event.y)
    new_rect_coords = canvas.coords(rect.get_rect_object())
    top_left_re, top_left_im = convert_to_diagram_coords(new_rect_coords[0],
                                                         new_rect_coords[1],
                                                         diagram)
    bot_right_re, bot_right_im = convert_to_diagram_coords(new_rect_coords[2],
                                                           new_rect_coords[3],
                                                           diagram)

    upper_left_str = convert_real_im_to_str(top_left_re, top_left_im)
    bot_right_str = convert_real_im_to_str(bot_right_re, bot_right_im)

    rect_pos_str.set(upper_left_str + " to " + bot_right_str)


def button_1_release(event, diagram, canvas, image):

    """
    When mouse button is released, zoom into the selected area of the set.
    """

    rect = diagram.get_user_drawn_rect()
    rect_coords = canvas.coords(rect.get_rect_object())
    top_left_re, top_left_im = convert_to_diagram_coords(rect_coords[0],
                                                         rect_coords[1],
                                                         diagram)
    bot_right_re, bot_right_im = convert_to_diagram_coords(rect_coords[2],
                                                           rect_coords[3],
                                                           diagram)
    real_range = (top_left_re, bot_right_re)
    im_range = (bot_right_im, top_left_im)
    diagram.append_to_zoom_list(real_range, im_range)

    zoom_image(diagram, image)
    remove_rect(diagram, canvas)

    back_button['state'] = 'active'



def go_back_one_zoom(diagram, image):
    diagram.revert_to_prev_zoom()
    zoom_image(diagram, image)
    if len(diagram.get_zoom_list()) == 1:
        back_button.config(state='disabled')


def main():

    """
    Do Tkinter bootplating, and create blank image to be populated. Do this
    population and then plot the result.
    """

    root = Tkinter.Tk()

    parser = create_parser()
    args = parser.parse_args()

    diagram = Diagram(args.width, args.height)

    image = Tkinter.PhotoImage(height=diagram.get_window_height(),
                               width=diagram.get_window_width())

    diagram_canvas = Tkinter.Canvas(root, width=diagram.get_window_width(),
                                    height=diagram.get_window_height(),
                                    cursor='tcross')
    diagram_canvas.create_image((diagram.get_window_width() / 2,
                                 diagram.get_window_height() / 2),
                                image=image)

    global back_button
    back_button = Tkinter.Button(root, text="Back", state="disabled", \
                                 command=lambda: go_back_one_zoom(diagram, \
                                                                  image))

    diagram_canvas.bind('<Motion>',
                        lambda event: motion(event, diagram, current_pos_str))
    diagram_canvas.bind('<Button-1>',
                        lambda event: button_1_press(event,
                                                     diagram,
                                                     diagram_canvas))
    diagram_canvas.bind('<B1-Motion>',
                        lambda event: button_1_motion(event,
                                                      diagram,
                                                      diagram_canvas,
                                                      rect_pos_str))

    diagram_canvas.bind('<ButtonRelease-1>',
                        lambda event: button_1_release(event, diagram,
                                                       diagram_canvas, image))

    diagram_canvas.grid()

    compute_mandelbrot_set(image, diagram)

    current_pos_str = Tkinter.StringVar()
    current_pos_str.set("Current mouse position")
    current_pos_label = Tkinter.Label(root, textvariable=current_pos_str)
    current_pos_label.grid()

    rect_pos_str = Tkinter.StringVar()
    rect_pos_str.set("Rectangle position")
    rect_pos_label = Tkinter.Label(root, textvariable=rect_pos_str, width=30)
    rect_pos_label.grid()

    back_button.grid()

    root.iconbitmap('@images/handel_icon.xbm')
    root.title("HandelPlot")
    root.mainloop()


if __name__ == "__main__":
    main()
