import argparse
from math import sin, cos, tau, degrees
from PIL import Image, ImageDraw

argumentParser = argparse.ArgumentParser(
    prog='StarPolygons image generator',
    description='Generates an image of a star polygon with given number of vertices and skip amount',
    epilog='Made for the Great Mathematical Workshop by Egor Kosachev'
)

argumentParser.add_argument(
    '-v',
    '--vertices',
    required=True,
    type=int,
    help='Number of vertices polygon will have',
)

argumentParser.add_argument(
    '-s',
    '--skip',
    required=True,
    type=int,
    help='Number of vertices that are skipped when generating the polygon',
)

argumentParser.add_argument(
    '--save',
    required=False,
    action='store_true',
    help='Saves the image to disk',
)

args = argumentParser.parse_args()
print(args)

vertices = args.vertices
skip = args.skip
step = skip + 1

if vertices < 5:
    print("Number of vertices must be greater than 5")
    exit(1)

if skip >= (vertices - 1):
    print("Skip must be strictly less than the number of vertices minus 1")
    exit(1)

points = []

for k in range(vertices):
    points.append((
        cos(tau * k / vertices),
        sin(tau * k / vertices)
    ))

edges = []

usedVertices = 0
shift = 0
while usedVertices < vertices:
    start_i = shift
    i1 = start_i
    i2 = start_i + 1 + skip
    i2 %= vertices
    edge = (points[i1], points[i2])
    if edge not in edges: edges.append(edge)
    while i2 != start_i:
        i1 = i2
        i2 += 1 + skip
        i2 %= vertices
        edge = (points[i1], points[i2])
        if edge not in edges: edges.append(edge)
        usedVertices += 1
    shift += 1


image = Image.new('RGB', (1024, 1024), (255, 255, 255))
imageDraw = ImageDraw.Draw(image)

for edge in edges:
    imageDraw.line(
        (
            (
                edge[0][0] * 300 + 512,
                edge[0][1] * 300 + 512,
            ),
            (
                edge[1][0] * 300 + 512,
                edge[1][1] * 300 + 512,
            )
        ),
        fill=(0, 0, 0),
        width=1,
    )

for i, point in enumerate(points):
    imageDraw.circle(
        (
            point[0] * 300 + 512,
            point[1] * 300 + 512,
        ),
        radius=5,
        fill=(255, 0, 0)
    )
    imageDraw.text(
        (
            point[0] * 300 + 520,
            point[1] * 300 + 520,
        ),
        text=f"{i} ({point[0]:.2f}; {point[1]:.2f})",
        fill=(255, 0, 0),
        font_size=20,
    )

# вычисляем точки пересечения боковых сторон

intersections = []

alpha = (tau / 4 * (vertices - 2 * (skip + 1))) / vertices
print(degrees(alpha))
beta = tau / vertices / 2
print(degrees(beta))
gamma = tau / 2 - alpha - beta
print(degrees(gamma))


r = sin(alpha) / sin(gamma)

for i in range(vertices):
    angle = (tau / vertices) * (i + .5)

    intersections.append(
        (
            r * cos(angle),
            r * sin(angle),
        )
    )

for i, point in enumerate(intersections):
    imageDraw.circle(
        (
            point[0] * 300 + 512,
            point[1] * 300 + 512,
        ),
        radius=3,
        fill=(0, 0, 255)
    )
    imageDraw.text(
        (
            point[0] * 300 + 520,
            point[1] * 300 + 520,
        ),
        text=f"{i} ({point[0]:.2f}; {point[1]:.2f})",
        fill=(0, 0, 255),
        font_size=20,
    )

# Определение связности/несвязности
is_connected = not any((step % i == 0) and (vertices % i == 0) for i in range(2, step + 1))
print([i for i in range(2, step + 1) if (step % i == 0) and (vertices % i == 0)])

if is_connected:
    print("Connected")
    color = (0, 255, 0)
else:
    print("Not connected")
    color = (255, 0, 0)

total = 0
for i in range(vertices):
    edge = (points[i], intersections[i])
    total += edge[0][0] * edge[1][1] - edge[1][0] * edge[0][1]
    edge = (intersections[i], points[(i + 1) % vertices])
    total += edge[0][0] * edge[1][1] - edge[1][0] * edge[0][1]

total /= 2
area = abs(total)

imageDraw.text(
    (10, 10),
    text=str(f"Area: {area:.2f}"),
    fill=color,
    font_size=20,
)

perimeter = 0
for edge in set(edges):
    perimeter += ((edge[0][0] - edge[1][0])**2 + (edge[0][1] - edge[1][1])**2)**.5

imageDraw.text(
    (10, 40),
    text=str(f"Perimeter: {perimeter:.2f}"),
    fill=color,
    font_size=20,
)

print(perimeter / vertices)

image.show(title="Polygon ({} vertices, {} skip)".format(vertices, skip))
if args.save:
    image.save('./polygon-{}-{}.png'.format(vertices, skip))

print(f"Generating a polygon with {vertices} vertices, skipping {skip}")