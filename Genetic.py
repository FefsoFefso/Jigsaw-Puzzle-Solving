import numpy as np
import Metric
import random


class Genetic:
    # pixel in 1 block, blocks in row, path with pictures
    def __init__(self, block_size, block_cnt, metric_info, path):
        self.block_size = block_size
        self.block_cnt = block_cnt
        self.metric_info = metric_info
        self.path = path

        self.percent = 0.8
        self.elite_cnt = 4

    def init_population(self):
        population = list()

        for i in range(1000):
            new_permutation = np.random.permutation(
                np.arange(self.block_cnt * self.block_cnt)
            ).reshape(self.block_cnt, self.block_cnt)
            population.append(new_permutation)

        return population

    def get_elite(self, population):
        gen_match = list()
        elite_list = list()
        print('len population : ' + str(len(population)))

        for gen in population:
            cur_viability = Metric.calc_gen_viability(gen, self.metric_info, self.block_cnt)
            gen_match.append([cur_viability, gen])

        gen_match.sort()

        for i in range(self.elite_cnt):
            elite_list.append(gen_match[i][1])

        elite_list.append(gen_match[random.randint(0, len(population) - 1)][1])
        """
        for elite_gen in elite_list:
            population.append(elite_gen)
        """
        # print('best : ' + str(gen_match[0][0]) + ' ' + str(gen_match[0][1]))
        # len(gen_match) - 1
        # print(str(len(elite_list)) + ' <- elite')
        # return gen_match[0][1], gen_match[1][1]
        return elite_list

    def selection(self, population):
        new_population = list()
        matching_info = list()
        new_population_size = int(len(population) * self.percent)
        print(len(population))

        for gen in population:
            cur_viability = Metric.calc_gen_viability(gen, self.metric_info, self.block_cnt)
            matching_info.append([cur_viability, gen])

        matching_info.sort()

        for gen in matching_info:
            new_population.append(gen[1])

        del new_population[new_population_size:len(population)]
        return new_population

    def is_best_body(self, first_part, second_part, side):
        side_index = Metric.get_side_index(side)
        reverse_size_index = Metric.get_reversed_side_index(side)
        min_cost_first = 100000.0
        min_cost_second = 100000.0

        for i in range(self.block_cnt):
            if self.metric_info[first_part][i][side_index] != -1:
                if self.metric_info[first_part][i][side_index] < min_cost_first:
                    min_cost_first = self.metric_info[first_part][i][side_index]

            if self.metric_info[second_part][i][reverse_size_index] != -1:
                if self.metric_info[second_part][i][reverse_size_index] < min_cost_second:
                    min_cost_second = self.metric_info[second_part][i][reverse_size_index]
        # print('first: ' + str(min_cost_first) + ' ' + str(side_index) + ' second: ' + str(min_cost_second) + ' ' + str(
        #   reverse_size_index))

        if min_cost_first == min_cost_second:
            # print(' -> mins : ' + str(min_cost_first) + ' second: ' + str(min_cost_second))
            return True
        return False

    def dfs(self, gen, graph, x_cord, y_cord, components_cnt):
        graph[y_cord][x_cord] = components_cnt
        if Metric.is_inside_box(x_cord + 1, y_cord, self.block_cnt):
            # print('y = ' + str(y_cord) + '  x = ' + str(x_cord) + ' -> ' + str(y_cord) + ' ' + str(x_cord + 1))
            if graph[y_cord][x_cord + 1] == 0 and self.is_best_body(gen[y_cord][x_cord], gen[y_cord][x_cord + 1], 'R'):
                graph = self.dfs(gen, graph, x_cord + 1, y_cord, components_cnt)

        if Metric.is_inside_box(x_cord, y_cord + 1, self.block_cnt):
            # print('y = ' + str(y_cord) + ' x = ' + str(x_cord) + ' -> ' + str(y_cord + 1) + ' ' + str(x_cord))
            if graph[y_cord + 1][x_cord] == 0 and self.is_best_body(gen[y_cord][x_cord], gen[y_cord + 1][x_cord], 'D'):
                graph = self.dfs(gen, graph, x_cord, y_cord + 1, components_cnt)

        if Metric.is_inside_box(x_cord, y_cord - 1, self.block_cnt):
            # print('y = ' + str(y_cord) + ' x = ' + str(x_cord) + ' -> ' + str(y_cord - 1) + ' ' + str(x_cord))
            if graph[y_cord - 1][x_cord] == 0 and self.is_best_body(gen[y_cord][x_cord], gen[y_cord - 1][x_cord], 'U'):
                graph = self.dfs(gen, graph, x_cord, y_cord - 1, components_cnt)

        if Metric.is_inside_box(x_cord - 1, y_cord, self.block_cnt):
            # print('y = ' + str(y_cord) + ' x = ' + str(x_cord) + ' -> ' + str(y_cord) + ' ' + str(x_cord - 1))
            if graph[y_cord][x_cord - 1] == 0 and self.is_best_body(gen[y_cord][x_cord], gen[y_cord][x_cord - 1], 'L'):
                graph = self.dfs(gen, graph, x_cord - 1, y_cord, components_cnt)

        return graph

    def get_connectivity_components(self, gen):
        components_cnt = 1
        graph = [0] * self.block_cnt
        for i in range(len(graph)):
            graph[i] = [0] * self.block_cnt

        for y_cord in range(self.block_cnt):
            for x_cord in range(self.block_cnt):
                # print('comp : ' + str(components_cnt))
                if graph[y_cord][x_cord] == 0:
                    graph = self.dfs(gen, graph, x_cord, y_cord, components_cnt)
                    components_cnt += 1

        return graph

    def debug(self):
        Metric.debug(self.metric_info)

    def crossover(self, left_parent, right_parent):
        left_cc = self.get_connectivity_components(left_parent)
        right_cc = self.get_connectivity_components(right_parent)
        return self.union(left_cc, left_parent, right_cc, right_parent)

    def do_genetic(self, population):
        while True:
            population = self.selection(population)

            if len(population) < 2:
                break

    def union(self, left_cc, left_gen, right_cc, right_gen):
        pass
