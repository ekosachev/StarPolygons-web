from image_generator import generate_polygon
from math import ceil

for n in range(5, 13):
    for m in range(2, ceil(n/2)):
        generate_polygon(n, m, 1, True, './')