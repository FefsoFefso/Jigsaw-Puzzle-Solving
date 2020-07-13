import os
import Metric

from PIL import Image


class PuzzlePicture:
    """
    Performing picture get, save and display
    Picture must be a square (N x N size)
    """

    def __init__(self, picture_size, block_size, path):
        self.picture_size = picture_size
        self.block_size = block_size
        self.path = path

        self.blocks_cnt = self.picture_size // self.block_size
        self.blocks_path = 'images_parts/'

    def cut_picture(self):
        """
         Saving blocks in dir 'image_parts'
         TODO: may be making map, save info .. ! !
        """

        input_image = Image.open(self.path)
        counter = 0  # 1 ??

        for y_cord in range(self.blocks_cnt):
            for x_cord in range(self.blocks_cnt):
                part = input_image.crop((x_cord * self.block_size,  # x1
                                         y_cord * self.block_size,  # y1
                                         (x_cord + 1) * self.block_size,  # x2
                                         (y_cord + 1) * self.block_size))  # y2

                part.save(self.blocks_path + str(counter) + '.png')
                counter += 1

    def build_image(self, matrix):
        """
        Build a new picture from sorted (previously) parts of the picture
        TODO: getting parts without extra dir
        """

        new_image = Image.new("RGB", (self.picture_size, self.picture_size))
        files = sorted(os.listdir(self.blocks_path), key=lambda string: int(string[0: string.find('.')]))
        iterator = 0

        for y_cord in range(self.blocks_cnt):
            for x_cord in range(self.blocks_cnt):
                """files[iterator] -> matrix[i][j]"""
                current_block = Image.open(self.blocks_path + str(matrix[x_cord][y_cord]) + '.png')
                new_image.paste(current_block, (x_cord * self.block_size, y_cord * self.block_size))
                iterator += 1

        new_image.save('result.png')
        new_image.show()

    # Getting RGB pictures info
    def get_metric_matching_info(self):
        """
        Getting R, G and B pixels data for any part of the puzzle
        """
        files = sorted(os.listdir(self.blocks_path), key=lambda string: int(string[0: string.find('.')]))
        distances = list()
        cnt = 0
        for file in files:
            current_dist = list()

            for another_file in files:
                if file != another_file:
                    img_file = Image.open(self.blocks_path + file)
                    img_another_file = Image.open(self.blocks_path + another_file)

                    up = Metric.get_metric_distance(img_file, img_another_file, 'U', self.block_size)
                    down = Metric.get_metric_distance(img_file, img_another_file, 'D', self.block_size)
                    left = Metric.get_metric_distance(img_file, img_another_file, 'L', self.block_size)
                    right = Metric.get_metric_distance(img_file, img_another_file, 'R', self.block_size)

                    current_dist.append([up, down, left, right])
                else:
                    current_dist.append([-1, -1, -1, -1])
            cnt += 1
            print(str(cnt) + ' ' + str(current_dist))
            distances.append(current_dist)

        return distances

    # Debug image showing, may be no
    def show_image(self):
        current_image = Image.open(self.path)
        current_image.show()

    # One more debug func
    def debug(self, num):
        ok = False
        new_image = Image.new("RGB", (self.picture_size, self.picture_size))
        file = open('data_train/data_train_64_answers.txt', 'r')
        iterator = 0
        for line in file:
            if ok:
                lst = list()
                new_ln = line.split()
                for png_id in new_ln:
                    lst.append(str(int(png_id)) + '.png')

                #print(lst)
                # blocks = sorted(os.listdir('image_parts/'), key=lambda string: int(string[0: string.find('.')]))
                for y_cord in range(self.blocks_cnt):
                    for x_cord in range(self.blocks_cnt):
                        current_block = Image.open(self.blocks_path + str(lst[iterator]))
                        new_image.paste(current_block, (x_cord * self.block_size, y_cord * self.block_size))
                        iterator += 1
                break

            if line == str(num) + ".png\n":
                ok = True

        file.close()
        new_image.show()


if __name__ == '__main__':
    img = PuzzlePicture(512, 64, 'data_train/64-sources/1200.png')