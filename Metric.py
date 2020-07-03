from math import sqrt


def GetMetricDistance(image_1, image_2, side, pixel_cnt):
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
def CalcGenViability(current_gen, metric_info, blocks_cnt):
    viability = 0
    for rows in range(blocks_cnt - 1):  # right sum  # -> #
        for columns in range(blocks_cnt):
            first_cmp = current_gen[rows][columns]
            second_cmp = current_gen[rows + 1][columns]
            viability += metric_info[first_cmp][second_cmp][3]

    for rows in range(blocks_cnt):  # down sum
        for columns in range(blocks_cnt - 1):
            first_cmp = current_gen[rows][columns]
            second_cmp = current_gen[rows][columns + 1]
            viability += metric_info[first_cmp][second_cmp][1]

    return viability
