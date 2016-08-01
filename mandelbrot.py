
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


def main():

    """
    Set up image canvas and plot the Mandelbrot Set.
    """

    window_width = 750
    window_height = 500

    img = create_blank_image(window_width, window_height)
    pixels = img.load()

    real_axis_range = (-2, 1) # Min and max on real (x) axis
    im_axis_range = (-1, 1) # Min and max on imaginary (y) axis

    # Increase in real component per pixel moved to the right
    dx = abs(real_axis_range[1] - real_axis_range[0]) / window_width

    # Increase in imaginary component per pixel moved downwards
    dy = abs(im_axis_range[1] - im_axis_range[0]) / window_height

    real_part = real_axis_range[0]

    for x_pixel in xrange(window_width):
        im_part = im_axis_range[0]
        for y_pixel in xrange(window_height):

            z_value = (0+0j)
            c_value = (real_part + (im_part * 1j))

            for k in xrange(64):
                if z_value.real > 2 or z_value.imag > 2:
                    pixels[x_pixel, y_pixel] = (k, k, k)
                    break
                else:
                    z_value = (z_value**2) + c_value

            im_part += dy
        real_part += dx

    img.show()

if __name__ == "__main__":
    main()
