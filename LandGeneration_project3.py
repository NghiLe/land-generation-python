import random
import sys

ESC = '\x1b'
RESET = ESC + '[0m'
WATER = ESC + '[44m' + ESC + '[97m' + '~' + RESET
SAND = ESC + '[43m' + ESC + '[33m' + '-' + RESET
GRASS = ESC + '[42m' + ESC + '[30m' + '.' + RESET
SNOW = ESC + '[47m' + ESC + '[30m' + ' ' + RESET


seed = int(sys.argv[1])
random.seed(seed)
magnitude = int(sys.argv[2])


def compute_offset(size, depth):
    if magnitude == 0:
        return size
    else:
        return size / (magnitude ** depth)


def x_step(map_, x1, y1, x2, y2, depth):
    mid_x = (x1 + x2) // 2
    mid_y = (y1 + y2) // 2
    size = x2 - x1

    r_offset = compute_offset(size, depth)
    offset = random.uniform(-r_offset, r_offset)

    c1 = map_[x1][y1]
    c2 = map_[x2][y1]
    c3 = map_[x1][y2]
    c4 = map_[x2][y2]

    map_[mid_x][mid_y] = (c1 + c2 + c3 + c4) / 4 + offset


def plus_step(map_, x1, y1, x2, y2, depth):
    mid_x = (x1 + x2) // 2
    mid_y = (y1 + y2) // 2
    size = x2 - x1

    r_offset = compute_offset(size, depth)

    map_[mid_x][y1] = (map_[x1][y1] + map_[x2][y1] + map_[mid_x][mid_y]) / 3 \
        + random.uniform(-r_offset, r_offset)
    map_[mid_x][y2] = (map_[x1][y2] + map_[x2][y2] + map_[mid_x][mid_y]) / 3 \
        + random.uniform(-r_offset, r_offset)
    map_[x1][mid_y] = (map_[x1][y1] + map_[x1][y2] + map_[mid_x][mid_y]) / 3 \
        + random.uniform(-r_offset, r_offset)
    map_[x2][mid_y] = (map_[x2][y1] + map_[x2][y2] + map_[mid_x][mid_y]) / 3 \
        + random.uniform(-r_offset, r_offset)


def x_plus(map_, x1, y1, x2, y2, depth):
    if x2 - x1 < 2:
        return

    x_step(map_, x1, y1, x2, y2, depth)
    plus_step(map_, x1, y1, x2, y2, depth)

    mid_x = (x1 + x2) // 2
    mid_y = (y1 + y2) // 2

    x_plus(map_, x1, y1, mid_x, mid_y, depth + 1)
    x_plus(map_, mid_x, y1, x2, mid_y, depth + 1)
    x_plus(map_, x1, mid_y, mid_x, y2, depth + 1)
    x_plus(map_, mid_x, mid_y, x2, y2, depth + 1)


def run(size=65):
    land = [[0 for _ in range(size)] for _ in range(size)]

    land[0][0] = random.randint(0, 100)
    land[0][size - 1] = random.randint(0, 100)
    land[size - 1][0] = random.randint(0, 100)
    land[size - 1][size - 1] = random.randint(0, 100)

    x_plus(land, 0, 0, size - 1, size - 1, 1)

    min_val = min(min(row) for row in land)
    max_val = max(max(row) for row in land)

    r = max_val - min_val
    t1 = min_val + 0.25 * r
    t2 = min_val + 0.50 * r
    t3 = min_val + 0.75 * r

    for row in land:
        line = ""
        for v in row:
            if v < t1:
                line += WATER
            elif v < t2:
                line += SAND
            elif v < t3:
                line += GRASS

        print(line)


run()
