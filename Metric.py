from math import sqrt
import numpy as np


def get_metric_distance(image_1, image_2, side, pixel_cnt):
    rgb_image_1 = image_1.convert('RGB')
    rgb_image_2 = image_2.convert('RGB')

    distance = 0

    if side == 'U':
        for i in range(pixel_cnt):
            r1, g1, b1 = rgb_image_1.getpixel((i, 0))
            r2, g2, b2 = rgb_image_2.getpixel((i, pixel_cnt - 1))
            distance += (r2 - r1) ** 2
            distance += (g2 - g1) ** 2
            distance += (b2 - b1) ** 2

    elif side == 'D':
        for i in range(pixel_cnt):
            r1, g1, b1 = rgb_image_1.getpixel((i, pixel_cnt - 1))
            r2, g2, b2 = rgb_image_2.getpixel((i, 0))
            distance += (r2 - r1) ** 2
            distance += (g2 - g1) ** 2
            distance += (b2 - b1) ** 2

    elif side == 'L':
        for i in range(pixel_cnt):
            r1, g1, b1 = rgb_image_1.getpixel((0, i))
            r2, g2, b2 = rgb_image_2.getpixel((pixel_cnt - 1, i))
            distance += (r2 - r1) ** 2
            distance += (g2 - g1) ** 2
            distance += (b2 - b1) ** 2

    elif side == 'R':
        for i in range(pixel_cnt):
            r1, g1, b1 = rgb_image_1.getpixel((pixel_cnt - 1, i))
            r2, g2, b2 = rgb_image_2.getpixel((0, i))
            distance += (r2 - r1) ** 2
            distance += (g2 - g1) ** 2
            distance += (b2 - b1) ** 2

    return sqrt(distance)


# U - 0, D - 1, L - 2, R - 3
def calc_gen_viability(current_gen, metric_info, blocks_cnt):
    viability = 0
    # print(current_gen)
    for rows in range(blocks_cnt - 1):  # right sum  # -> #
        for columns in range(blocks_cnt):
            first_cmp = np.int(current_gen[rows][columns])
            second_cmp = np.int(current_gen[rows + 1][columns])
            viability += metric_info[first_cmp][second_cmp][3]

    for rows in range(blocks_cnt):  # down sum
        for columns in range(blocks_cnt - 1):
            first_cmp = np.int(current_gen[rows][columns])
            second_cmp = np.int(current_gen[rows][columns + 1])
            viability += metric_info[first_cmp][second_cmp][1]

    return viability


def get_side_index(side):
    if side == 'U':
        return 0
    if side == 'D':
        return 1
    if side == 'L':
        return 2
    if side == 'R':
        return 3


def get_reversed_side_index(side):
    if side == 'U':
        return 1
    if side == 'D':
        return 0
    if side == 'L':
        return 3
    if side == 'R':
        return 2


def is_inside_box(x_cord, y_cord, block_cnt):
    if x_cord < 0 or x_cord >= block_cnt or y_cord < 0 or y_cord >= block_cnt:
        return False

    return True


def debug(metric):
    for i in range(len(metric)):
        for j in range(len(metric)):
            for o in range(4):
                print(metric[i][j][o], end=' ')
            print()
