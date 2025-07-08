# pip install pillow numpy

from PIL import Image
import numpy as np


def mandelbrot(c_min, c_max, f_width, f_height, f_maxiter):
    """
    cmin: bottom left corner, as a complex number
    cmax: top right corner, as a complex number
    width: width of the resultant array
    height: height of the resultant array
    maxiter: maximum number of iterations
    """

    # make the real axis as an array of shape (width)
    real = np.linspace(c_min.real, c_max.real, f_width, dtype=np.float32)
    # make the imaginary axis as an array of shape (height)
    image = np.linspace(c_min.imag, c_max.imag, f_height, dtype=np.float32) * 1j
    # combine them into a complex array of shape (width, height)
    c = real + image[:, None]

    # make the output array of the same shape, fill it with int zeroes
    output = np.zeros(c.shape, dtype='uint16')
    # and a z array of the same shape, fill it with complex zeroes
    z = np.zeros(c.shape, np.complex64)
    # do the mandelbrot thing:
    for i in range(f_maxiter):
        # make a bool array of the same shape showing where `z` is within range
        not_done = np.less(z.real * z.real + z.imag * z.imag, 4.0)
        # at the places where `not_done` is true,
        # update the current iteration number;
        # the places where `z` got out of range will be unaffected
        output[not_done] = i
        # update `z` in those same places
        z[not_done] = z[not_done] ** 2 + c[not_done]
    # make the center zero for nice contrast
    output[output == f_maxiter - 1] = 0

    return output


# Adapted from https://gist.github.com/jfpuget/60e07a82dece69b011bb
cmin, cmax = -2 - 1j, 1 + 1j
width, height = 800, 600
maxiter = 80
# calculate the mandelbrot set
m = mandelbrot(cmin, cmax, width, height, maxiter)
# calculate the greyscale pixels
pixels = (m * 255 / maxiter).astype('uint8')
# make the greyscale image
img = Image.fromarray(pixels, 'L')
# and let us see it
img.show()
