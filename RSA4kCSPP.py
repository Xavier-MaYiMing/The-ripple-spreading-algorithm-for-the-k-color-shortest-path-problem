#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/14 13:37
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : RSA4kCSPP.py
# @Statement : The ripple-spreading algorithm for the k-color shortest path problem
# @Reference : Y.M. Ma, H. Zhou, X.B. Hu. The ripple-spreading algorithm for the k-color shortest path problem[C]//2022 IEEE Symposium Series on Computational Intelligence (SSCI). IEEE.
import copy


def find_neighbor(network):
    """
    find the neighbor of each node
    :param network:
    :return: {node 1: [the neighbor nodes of node 1], ...}
    """
    nn = len(network)
    neighbor = []
    for i in range(nn):
        neighbor.append(list(network[i].keys()))
    return neighbor


def find_speed(network, neighbor):
    """
    find the ripple-spreading speed (v=min(w_{ij}))
    :param network:
    :param neighbor:
    :return:
    """
    min_value = 1e10
    nn = len(network)
    for i in range(nn):
        for j in neighbor[i]:
            min_value = min(min_value, network[i][j][0])
    return min_value


def dominated(length1, color1, length2, color2):
    """
    judge whether ripple 1 is dominated by ripple 2
    :param length1: the length of ripple 1
    :param color1: the color of ripple 1
    :param length2: the length of ripple 2
    :param color2: the color of ripple 2
    :return:
    """
    if length1 > length2 and color1 >= color2:
        return True
    elif length1 >= length2 and color1 > color2:
        return True
    return False


def find_new_ripples(incoming_ripples):
    """
    screen out the dominated ripples
    :param incoming_ripples:
    :param incoming_ripples:
    :return:
    """
    ripple_num = len(incoming_ripples)
    new_ripples_flag = [True for i in range(ripple_num)]
    for i in range(ripple_num):
        length1 = incoming_ripples[i]['objective']
        color1 = incoming_ripples[i]['color']
        for j in range(ripple_num):
            if i != j:
                length2 = incoming_ripples[j]['objective']
                color2 = incoming_ripples[j]['color']
                if dominated(length1, color1, length2, color2):
                    new_ripples_flag[i] = False
                    break
    new_feasible_ripples = []
    for i in range(ripple_num):
        if new_ripples_flag[i]:
            new_feasible_ripples.append(incoming_ripples[i])
    return new_feasible_ripples


def find_POR(incoming_ripples, omega, objective_set, color_set):
    """
    find the Pareto-optimal ripple at a node
    :param incoming_ripples:
    :param omega:
    :param objective_set:
    :param color_set:
    :return:
    """
    new_ripples = []
    new_feasible_ripples = find_new_ripples(incoming_ripples)
    if not omega:
        return new_feasible_ripples
    else:
        for ripple1 in new_feasible_ripples:
            flag = True
            length1 = ripple1['objective']
            color1 = ripple1['color']
            for ripple2 in omega:
                if dominated(length1, color1, objective_set[ripple2], color_set[ripple2]):
                    flag = False
                    break
            if flag:
                new_ripples.append(ripple1)
    return new_ripples


def main(network, source, destination, k):
    """
    the main function
    :param network: {node 1: {node 2: [length, color], ...}, ...}
    :param source: the source node
    :param destination: the destination node
    :param k: the maximum number of colors
    :return:
    """
    # Step 1. Initialization
    nn = len(network)  # node number
    neighbor = find_neighbor(network)  # the neighbor of each node
    v = find_speed(network, neighbor)  # the ripple-spreading speed
    t = 0  # time
    nr = 0  # the current node number
    epicenter_set = []
    active_set = []
    path_set = []
    radius_set = []
    objective_set = []
    color_set = []
    omega = {}
    for node in range(nn):
        omega[node] = []

    # Step 2. Initialize the first ripple
    epicenter_set.append(source)
    radius_set.append(0)
    active_set.append(nr)
    path_set.append([source])
    objective_set.append(0)
    omega[source].append(nr)
    color_set.append(set())
    nr += 1

    # Step 3. The main loop
    while True:

        # Step 3.0. Check if there are active ripples
        if not active_set:
            print('No feasible solution!')
            return

        # Step 3.1. Termination judgment
        if omega[destination]:
            break

        # Step 3.2. Time updates
        t += 1
        incoming_ripples = {}
        remove_ripples = []
        for ripple in active_set:
            flag_inactive = True

            # Step 3.3. Active ripples spread out
            radius_set[ripple] += v

            # Step 3.4. New incoming ripples
            epicenter = epicenter_set[ripple]
            radius = radius_set[ripple]
            path = path_set[ripple]
            obj = objective_set[ripple]
            color = color_set[ripple]
            for node in neighbor[epicenter]:
                temp_length = network[epicenter][node][0]
                if node not in path and temp_length <= radius < temp_length + v:
                    temp_path = copy.deepcopy(path)
                    temp_path.append(node)
                    temp_color = copy.deepcopy(color)
                    temp_color.add(network[epicenter][node][1])
                    if len(temp_color) <= k:
                        if node in incoming_ripples.keys():
                            incoming_ripples[node].append({
                                'path': temp_path,
                                'radius': radius - temp_length,
                                'objective': obj + network[epicenter][node][0],
                                'color': temp_color,
                            })
                        else:
                            incoming_ripples[node] = [{
                                'path': temp_path,
                                'radius': radius - temp_length,
                                'objective': obj + network[epicenter][node][0],
                                'color': temp_color,
                            }]

                # Step 3.5. Active ripple -> inactive
                if radius < temp_length:
                    flag_inactive = False
            if flag_inactive:
                remove_ripples.append(ripple)
        for ripple in remove_ripples:
            active_set.remove(ripple)

        # Step 3.6. Generate new ripples
        for node in incoming_ripples.keys():
            new_ripples = find_POR(incoming_ripples[node], omega[node], objective_set, color_set)
            for item in new_ripples:
                path_set.append(item['path'])
                epicenter_set.append(node)
                radius_set.append(item['radius'])
                active_set.append(nr)
                omega[node].append(nr)
                objective_set.append(item['objective'])
                color_set.append(item['color'])
                nr += 1

    # Step 4. Select the best path
    temp_index = -1
    temp_objective = 1e6
    for ripple in omega[destination]:
        if objective_set[ripple] < temp_objective:
            temp_objective = objective_set[ripple]
            temp_index = ripple
    result = {
        'path': path_set[temp_index],
        'color': color_set[temp_index],
        'length': objective_set[temp_index]
    }
    return result


if __name__ == '__main__':
    # The color: 1 denotes black, 2 denotes red, 3 denotes blue, and 4 denotes green.
    temp_network = {
        0: {1: [1, 1], 3: [1, 4]},
        1: {2: [1, 2], 4: [1, 3]},
        2: {5: [1, 3]},
        3: {6: [1, 1]},
        4: {3: [1, 1], 7: [1, 4]},
        5: {4: [1, 1], 8: [1, 4]},
        6: {7: [1, 3]},
        7: {8: [1, 2]},
        8: {}
    }
    source_node = 0
    destination_node = 8
    color_num = 3
    print(main(temp_network, source_node, destination_node, color_num))
