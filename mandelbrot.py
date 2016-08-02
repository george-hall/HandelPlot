
"""
Plot the Mandelbrot Set.
"""

from __future__ import division

from PIL import Image

def create_blank_image(horiz_width, vert_width):

    """
    Returns a blank image with each pixel independently accessable.
    """

    return Image.new('RGB', (horiz_width + 1, vert_width + 1), "black")


def compute_deltas(real_axis_range, im_axis_range, window_width,
                   window_height):

    """
    Return the size of the range covered by each pixel for the x and y axes.
    I.e. 'dx' is the jump in value of the real component of the a point for
    every pixel moved in the positive x direction. 'dy' is the analaogue of
    'dx' but for the imaginary (y) axis.
    """

    dx = abs(real_axis_range[1] - real_axis_range[0]) / window_width
    dy = abs(im_axis_range[1] - im_axis_range[0]) / window_height

    return (dx, dy)


def compute_escape_iterations(real_part, im_part):

    """
    Compute the number of iterations required for this point to escape the
    Mandelbrot Set. Otherwise, return -1, signifying that the point is, in fact
    in the Set.
    """

    z_value = (0+0j)
    c_value = (real_part + (im_part * 1j))

    for k in xrange(64):
        if z_value.real > 2 or z_value.imag > 2:
            return k
        else:
            z_value = (z_value**2) + c_value

    return -1


def populate_pixel_array(pixels, window_width, window_height,
                         real_axis_range=(-2, 1), im_axis_range=(-1, 1)):

    """
    Populate pixel array with colours set according to how quickly each point
    escapes the Mandelbrot Set.
    """

    (dx, dy) = compute_deltas(real_axis_range, im_axis_range, window_width,
                              window_height)

    real_part = real_axis_range[0] # Real component of current point

    for x_pixel in xrange(window_width):
        im_part = im_axis_range[0] # Imaginary component of current point
        for y_pixel in xrange(window_height):

            escape_iterations = compute_escape_iterations(real_part, im_part)
            if escape_iterations != -1:
                pixels[x_pixel, y_pixel] = (escape_iterations,
                                            escape_iterations,
                                            escape_iterations)

            im_part += dy
        real_part += dx

    return pixels


def main():

    """
    Set up blank image canvas and run function to populate pixels. Then plot
    the result.
    """

    window_width = 750
    window_height = 500

    img = create_blank_image(window_width, window_height)
    pixels = img.load()
    pixels = populate_pixel_array(pixels, window_width, window_height)
    img.show()


if __name__ == "__main__":
    main()
