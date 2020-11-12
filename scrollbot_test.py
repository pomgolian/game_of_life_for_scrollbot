import scrollphathd as sphd
import time


for x in range(17):
    sphd.clear()
    for y in range(7):
        sphd.set_pixel(x, y, 0.25)
    sphd.show()
    time.sleep(1/17.0)


my_pixels = (10, 20, .5)
sphd.set_pixel(*my_pixels)
