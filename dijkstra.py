import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, o):
        return Vector(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return Vector(self.x - o.x, self.y - o.y)

    def __mul__(self, val):
        return Vector(self.x * val, self.y * val)

    def __abs__(self):
        return math.sqrt(self.abssq())

    def abssq(self):
        return self.x*self.x + self.y*self.y

    def __repr__(self):
        return f"V({self.x}, {self.y})"


def point_line_dist(p1, p2, p3):
    denom = (p2 - p1).abssq()
    u = (p3.x - p1.x)*(p2.x - p1.x) + (p3.y - p1.y)*(p2.y - p1.y)
    u /= denom

    if u > 1:
        u = 1
    if u < 0:
        u = 0

    p = Vector(p1.x + u * (p2.x - p1.x), p1.y + u * (p2.y - p1.y))
    return abs(p - p3)


def line_intersect(a, b, c, d):
    x1 = a.x; y1 = a.y; x2 = b.x; y2 = b.y
    x3 = c.x; y3 = c.y; x4 = d.x; y4 = d.y
    denom = (y4 - y3)*(x2 - x1) - (x4 - x3)*(y2 - y1)
    if abs(denom) < 1e-5:
        return False
    ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom
    if ua < 0 or ua > 1:
        return False
    ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denom
    if ub < 0 or ub > 1:
        return False
    return True


def line_too_close(a, b, c, d, clearing):
    if line_intersect(a, b, c, d):
        return True

    d1 = point_line_dist(a, b, c)
    d2 = point_line_dist(a, b, d)
    d3 = point_line_dist(c, d, a)
    d4 = point_line_dist(c, d, b)
    if min(d1, d2, d3, d4) < clearing:
        return True

    return False


def collision(p, q, ovire, clearing):
    for ovira in ovire:
        if line_too_close(p, q, ovira[0], ovira[1], clearing) \
           or line_too_close(p, q, ovira[1], ovira[2], clearing) \
           or line_too_close(p, q, ovira[2], ovira[3], clearing) \
           or line_too_close(p, q, ovira[3], ovira[0], clearing):
            return True

    return False


def compute_reachable(points, ovire, clearing):
    reachable = [[True] * len(points) for __ in points]
    for i, p in enumerate(points):
        for j, q in enumerate(points):
            if i == j:
                continue
            if collision(p, q, ovire, clearing):
                reachable[i][j] = False
    return reachable


def dijkstra(start, stop, ovire, clearing, show_graph=False):
    points = []
    dists = []

    for o in ovire:
        center = (o[0] + o[1] + o[2] + o[3]) * 0.25
        for i in range(4):
            diff = o[i] - center
            points.append(center + diff * ((abs(diff) + clearing) / abs(diff)))
            dists.append(math.inf)

    points.append(start)
    dists.append(0)
    starti = len(points)-1
    points.append(stop)
    dists.append(math.inf)
    stopi = len(points)-1

    reachable = compute_reachable(points, ovire, clearing*0.65)

    if show_graph:
        for o in ovire:
            plt.fill(
                [p.x for p in o],
                [p.y for p in o]
            )

        for i, p in enumerate(points):
            for j, q in enumerate(points):
                if i == j:
                    continue
                if reachable[i][j]:
                    plt.plot([p.x, q.x], [p.y, q.y])

        plt.axis("equal")
        plt.show()

    prevs = [None for __ in points]
    fixed = [False for __ in points]

    while True:
        idx = 0
        for i in range(len(points)):
            if fixed[i]: continue
            if dists[idx] > dists[i] or fixed[idx]:
                idx = i

        if fixed[idx] or fixed[stopi]:
            break

        fixed[idx] = True
        for i in range(len(points)):
            if fixed[i] or not reachable[idx][i]: continue
            d = dists[idx] + abs(points[i] - points[idx])
            if dists[i] > d:
                dists[i] = d
                prevs[i] = idx

    pt = stopi
    pts = []
    while pt != starti:
        pts.append(points[pt])
        pt = prevs[pt]
    pts.append(points[pt])
    pts.reverse()
    return pts


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    ovire = [
        (
            Vector(0, 0),
            Vector(100, 0),
            Vector(100, 100),
            Vector(0, 100)
        ),
        (
            Vector(300, 100),
            Vector(400, 200),
            Vector(200, 400),
            Vector(100, 300)
        ),
        (
            Vector(200, 0),
            Vector(250, 0),
            Vector(250, 50),
            Vector(200, 50)
        )
    ]

    pot = dijkstra(
        Vector(-100, -100),
        Vector(500, 500),
        ovire,
        50,
        show_graph=True
    )

    print(pot)

    plt.figure()
    plt.axis('equal')

    for o in ovire:
        plt.fill(
            [p.x for p in o],
            [p.y for p in o]
        )

    plt.plot(
        [p.x for p in pot],
        [p.y for p in pot]
    )

    plt.show()

