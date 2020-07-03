import numpy as np


class Genetic:
    # pixel in 1 block, blocks in row, path with pictures
    def __init__(self, block_size, block_cnt, path):
        self.block_size = block_size
        self.block_cnt = block_cnt
        self.path = path

    def InitPopulation(self):
        population = list()

        for i in range(10000):
            new_permutation = np.random.permutation(
                                                    np.arange(self.block_cnt * self.block_cnt)
                                                        ).reshape(self.block_cnt, self.block_cnt)
            population.append(new_permutation)

        return population


    def Selection(self, population):
        new_population = list()
        pass

    def Crossover(self, left_parent, right_parent):
        pass

    # mey be doesnt metter
    def GetId(self, row, column, blocks_cnt):
        return row * blocks_cnt + column


if __name__ == '__main__':
    g = Genetic(64, 8, 'image_parts/')
    a = g.InitPopulation()
    #print(a)
