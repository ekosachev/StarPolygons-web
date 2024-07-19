from math import tau, cos, sin, degrees

from PIL import Image, ImageDraw

n = int(input())
m = int(input())

COLOR_EDGE = [
    (103, 78, 167),
    (217, 210, 233),
    (103, 78, 167),

]
COLOR_EDGE.reverse()
COLOR_BG = (180,167,214)

image = Image.new('RGB', (2048, 2048), COLOR_BG)
imageDraw = ImageDraw.Draw(image)

r = 1
for cur_m in range(m, 0, -1):

    points = []
    theta = tau / n

    if cur_m % 2 == 0:
        rot = theta / 2
    else:
        rot = 0

    for k in range(n):
        points.append((
            cos(theta * k + rot),
            sin(theta * k + rot)
        ))

    edges = []

    usedVertices = 0
    shift = 0
    while usedVertices < n:
        start_i = shift
        i1 = start_i
        i2 = start_i + cur_m
        i2 %= n
        edge = (points[i1], points[i2])
        if edge not in edges: edges.append(edge)
        while i2 != start_i:
            i1 = i2
            i2 += cur_m
            i2 %= n
            edge = (points[i1], points[i2])
            if edge not in edges: edges.append(edge)
            usedVertices += 1
        shift += 1

    for edge in edges:
        imageDraw.line(
            (
                (
                    edge[0][0] * 1000 * r + 1024,
                    edge[0][1] * 1000 * r + 1024,
                ),
                (
                    edge[1][0] * 1000 * r + 1024,
                    edge[1][1] * 1000 * r + 1024,
                ),
            ),
            fill=COLOR_EDGE[cur_m - 1],
            width=10
        )

    alpha = (tau / 4 * (n - 2 * cur_m)) / n
    beta = theta / 2
    gamma = tau / 2 - alpha - beta

    print(degrees(alpha), degrees(beta), degrees(gamma))

    r *= sin(alpha) / sin(gamma)
    print(r)

image.save('./inlayed_stars.png', format='PNG')