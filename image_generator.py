from math import tau, cos, sin, degrees, sqrt

from PIL import Image, ImageDraw


def generate_polygon(n: int, m: int, r: float, save: bool, path: str = './cache') -> tuple[float, float, float]:
    points = []
    theta = tau / n

    COLOR_BG = (227, 227, 227)
    COLOR_EDGE = (30, 22, 33)
    SIZE = (1024, 1024)
    SCALE = 450

    for k in range(n):
        points.append((
            cos(theta * k),
            sin(theta * k)
        ))

    edges = []

    usedVertices = 0
    shift = 0
    while usedVertices < n:
        start_i = shift
        i1 = start_i
        i2 = start_i + m
        i2 %= n
        edge = (points[i1], points[i2])
        if edge not in edges: edges.append(edge)
        while i2 != start_i:
            i1 = i2
            i2 += m
            i2 %= n
            edge = (points[i1], points[i2])
            if edge not in edges: edges.append(edge)
            usedVertices += 1
        shift += 1

    # вычисляем точки пересечения боковых сторон

    intersections = []

    alpha = (tau / 4 * (n - 2 * m)) / n
    beta = theta / 2
    gamma = tau / 2 - alpha - beta

    rad = sin(alpha) / sin(gamma)

    for i in range(n):
        angle = theta * (i + .5)

        intersections.append(
            (
                rad * cos(angle),
                rad * sin(angle),
            )
        )

    is_connected = not any((m % i == 0) and (n % i == 0) for i in range(2, m + 1))

    total = 0
    for i in range(n):
        edge = (points[i], intersections[i])
        total += edge[0][0] * edge[1][1] - edge[1][0] * edge[0][1]
        edge = (intersections[i], points[(i + 1) % n])
        total += edge[0][0] * edge[1][1] - edge[1][0] * edge[0][1]

    total /= 2
    area = abs(total)

    perimeter = 0
    for edge in set(edges):
        perimeter += ((edge[0][0] - edge[1][0]) ** 2 + (edge[0][1] - edge[1][1]) ** 2) ** .5

    if save:
        image = Image.new('RGB', (1024, 1024), COLOR_BG)
        imageDraw = ImageDraw.Draw(image)

        for edge in edges:
            imageDraw.line(
                (
                    (
                        edge[0][0] * SCALE + SIZE[0] // 2,
                        edge[0][1] * SCALE + SIZE[1] // 2,
                    ),
                    (
                        edge[1][0] * SCALE + SIZE[0] // 2,
                        edge[1][1] * SCALE + SIZE[1] // 2,
                    ),
                ),
                fill=COLOR_EDGE,
                width=5
            )

        image.save('{}/{}-{}-{}.png'.format(path, n, m, r))

    return (
        sqrt((edges[0][1][0] - edges[0][0][0]) ** 2 + (edges[0][1][1] - edges[0][0][1]) ** 2) * r,
        area * r ** 2,
        perimeter * r
    )
