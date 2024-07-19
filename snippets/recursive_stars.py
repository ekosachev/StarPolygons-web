from math import tau, pi, sin, radians, cos

from PIL import Image, ImageDraw


def generate(n, m, depth=2, save: bool = False):
    image = Image.new(mode='RGB', size=(2048, 2048), color=(180, 167, 214))
    draw = ImageDraw.Draw(image)

    cur_depth = 0
    R = 1
    for d in range(depth):
        THETA = tau / n

        if m % 2 == 0:
            rot = THETA / 2
        else:
            rot = 0


        # генерим вершины
        points = []
        for k in range(n):
            points.append((
                cos(THETA * k + rot * cur_depth) * R,
                sin(THETA * k + rot * cur_depth) * R,
            ))
        # генерим стороны
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
        # рисуем стороны
        for edge in edges:
            draw.line(
                (
                    (
                        edge[0][0] * 1000 + 1024,
                        edge[0][1] * 1000 + 1024,
                    ),
                    (
                        edge[1][0] * 1000 + 1024,
                        edge[1][1] * 1000 + 1024,
                    ),
                ),
                fill=(
                    int(cur_depth * (255 / depth)),
                    int(cur_depth * (255 / depth)),
                    int(cur_depth * (255 / depth)),
                ),
                width=10
            )

        alpha = (tau / (2 * n)) * (n - 2 * m)
        beta = (tau / n)

        if m % 2 == 0:
            beta /= 2

        d1 = R * sin(alpha / 2)
        d2 = sin(pi - alpha / 2 - beta)

        R = d1 / d2
        cur_depth += 1
        print(R)
    image.show("IMAGE")

    if save:
        image.save('./image.png', format='PNG')


def calc_k(alpha, n):
    return sin(pi - alpha / 2 - tau / n) / sin(alpha / 2)

print(calc_k((tau / (2 * 5) * (5 - 2 * 2)), 5))
generate(8, 3, 5, True)
