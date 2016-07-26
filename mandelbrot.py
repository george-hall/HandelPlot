from PIL import Image

def main():

    x_width = 750
    y_width = 500

    x_lower = int(x_width * (-2 / 3.0))
    x_upper = int(x_width * (1 / 3.0)) + 1

    y_lower = int(y_width * (-1 / 2.0))
    y_upper = int(y_width * (1 / 2.0)) + 1

    img = Image.new('RGB', (x_width + 1, y_width + 1), "black")
    pixels = img.load()

    for i in xrange(x_lower, x_upper):
        real_part = i / 100.0
        for j in xrange(y_lower, y_upper):
            im_part = j / 100.0

            z = (0+0j)
            c = (real_part + (im_part * 1j))

            for k in xrange(64):
                if z.real > 2 or z.imag > 2:
                    pixels[i + abs(x_lower), j + abs(y_lower)] = (k, k, k)
                    break
                else:
                    z = (z**2) + c

    img.show()

if __name__ == "__main__":
    main()
