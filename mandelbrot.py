
"""
Plot the Mandelbrot Set.
"""

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

    window_horiz_width = 750
    window_vert_width = 500

    img = create_blank_image(window_horiz_width, window_vert_width)
    pixels = img.load()

    window_min_x = int(window_horiz_width * (-2 / 3.0))
    window_max_x = int(window_horiz_width * (1 / 3.0)) + 1

    window_min_y = int(window_vert_width * (-1 / 2.0))
    window_max_y = int(window_vert_width * (1 / 2.0)) + 1


    for i in xrange(window_min_x, window_max_x):
        real_part = i / 100.0
        for j in xrange(window_min_y, window_max_y):
            im_part = j / 100.0

            z_value = (0+0j)
            c_value = (real_part + (im_part * 1j))

            for k in xrange(64):
                if z_value.real > 2 or z_value.imag > 2:
                    pixels[i + abs(window_min_x), j + abs(window_min_y)] = (k, k, k)
                    break
                else:
                    z_value = (z_value**2) + c_value

    img.show()

if __name__ == "__main__":
    main()
