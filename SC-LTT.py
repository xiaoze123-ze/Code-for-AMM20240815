from gurobipy import *
import pandas as pd
from datetime import datetime, timedelta

# Define 23:00:00 as the initial time
initial_time_str = "23:00:00"
initial_time = datetime.strptime(initial_time_str, "%H:%M:%S")

# Input basic data
# Randomly generated passenger flow data, with the format of 9 * 9 matrix
demands = pd.DataFrame([[0, 0, 0, 0, 80, 80, 90, 10, 40], [0, 0, 0, 0, 100, 0, 80, 0, 0], [0, 0, 0, 0, 0, 0, 0, 10, 10],
                        [0, 0, 0, 0, 60, 40, 20, 60, 40], [90, 80, 0, 100, 0, 0, 0, 30, 20],
                        [70, 0, 0, 70, 0, 0, 0, 0, 0], [70, 60, 0, 10, 0, 0, 0, 40, 70],
                        [60, 0, 80, 100, 30, 0, 100, 0, 0], [70, 0, 50, 70, 40, 0, 70, 0, 0]], index=range(1, 10),
                       columns=range(1, 10))

# The set of stations on lines 1, 2 and 3 from left to right, respectively
station_list = [[1, 2, 3, 4], [5, 6, 3, 7], [8, 2, 6, 9]]

# The set of transfer connections, with the format of (station_ID, 'feeder_line_ID-direction', 'connecting_line_ID-direction')
# 1 for up direction, 2 for down direction
transfer_connection_list = [(2, '1-1', '3-1'), (2, '1-1', '3-2'), (2, '1-2', '3-1'), (2, '1-2', '3-2'),
                            (2, '3-1', '1-1'), (2, '3-1', '1-2'), (2, '3-2', '1-1'), (2, '3-2', '1-2'),
                            (3, '1-1', '2-1'), (3, '1-1', '2-2'), (3, '1-2', '2-1'), (3, '1-2', '2-2'),
                            (3, '2-1', '1-1'), (3, '2-1', '1-2'), (3, '2-2', '1-1'), (3, '2-2', '1-2'),
                            (6, '2-1', '3-1'), (6, '2-1', '3-2'), (6, '2-2', '3-1'), (6, '2-2', '3-2'),
                            (6, '3-1', '2-1'), (6, '3-1', '2-2'), (6, '3-2', '2-1'), (6, '3-2', '2-2')]

# The preset set of each OD pair's candidate paths, with format of (od_pair_ID): [path_1, path_2, ...]
path_dict = {(1, 5): [(1, 2, 6, 5), (1, 3, 5)],
             (1, 6): [(1, 2, 6), (1, 3, 6)],
             (1, 7): [(1, 2, 6, 7), (1, 3, 7)],
             (1, 8): [(1, 2, 8), (1, 3, 6, 8)],
             (1, 9): [(1, 2, 9), (1, 3, 6, 9)],
             (2, 5): [(2, 6, 5), (2, 3, 5)],
             (2, 7): [(2, 6, 7), (2, 3, 7)],
             (3, 8): [(3, 6, 8), (3, 2, 8)],
             (3, 9): [(3, 6, 9), (3, 2, 9)],
             (4, 5): [(4, 3, 5), (4, 2, 6, 5)],
             (4, 6): [(4, 3, 6), (4, 2, 6)],
             (4, 7): [(4, 3, 7), (4, 2, 6, 7)],
             (4, 8): [(4, 2, 8), (4, 3, 6, 8)],
             (4, 9): [(4, 3, 6, 9), (4, 2, 9)],
             (5, 1): [(5, 6, 2, 1), (5, 3, 1)],
             (5, 2): [(5, 6, 2), (5, 3, 2)],
             (5, 4): [(5, 3, 4), (5, 6, 2, 4)],
             (5, 8): [(5, 6, 8), (5, 3, 2, 8)],
             (5, 9): [(5, 6, 9), (5, 3, 2, 9)],
             (6, 1): [(6, 2, 1), (6, 3, 1)],
             (6, 4): [(6, 3, 4), (6, 2, 4)],
             (7, 1): [(7, 3, 1), (7, 6, 2, 1)],
             (7, 2): [(7, 6, 2), (7, 3, 2)],
             (7, 4): [(7, 3, 4), (7, 6, 2, 4)],
             (7, 8): [(7, 3, 2, 8), (7, 6, 8)],
             (7, 9): [(7, 6, 9), (7, 3, 2, 9)],
             (8, 1): [(8, 2, 1), (8, 6, 3, 1)],
             (8, 3): [(8, 2, 3), (8, 6, 3)],
             (8, 4): [(8, 2, 4), (8, 6, 3, 4)],
             (8, 5): [(8, 6, 5), (8, 2, 3, 5)],
             (8, 7): [(8, 6, 7), (8, 2, 3, 7)],
             (9, 1): [(9, 2, 1), (9, 6, 3, 1)],
             (9, 3): [(9, 6, 3), (9, 2, 3)],
             (9, 4): [(9, 6, 3, 4), (9, 2, 4)],
             (9, 5): [(9, 6, 5), (9, 2, 3, 5)],
             (9, 7): [(9, 6, 7), (9, 2, 3, 7)]}

# The set of each od pair's transfer connections on candidate paths, with the format of
# (od_pair_ID): [[transfer_connection_1_of path_1, transfer_connection_2_of_path_1, ...], [transfer_connection_1_of_path_2, transfer_connection_2_of_path_2, ...], ...]
transfer_connection_dict = {(1, 5): [[(2, '1-1', '3-1'), (6, '3-1', '2-2')], [(3, '1-1', '2-2')]],
                            (1, 6): [[(2, '1-1', '3-1')], [(3, '1-1', '2-2')]],
                            (1, 7): [[(2, '1-1', '3-1'), (6, '3-1', '2-1')], [(3, '1-1', '2-1')]],
                            (1, 8): [[(2, '1-1', '3-2')], [(3, '1-1', '2-2'), (6, '2-2', '3-2')]],
                            (1, 9): [[(2, '1-1', '3-1')], [(3, '1-1', '2-2'), (6, '2-2', '3-1')]],
                            (2, 5): [[(6, '3-1', '2-2')], [(3, '1-1', '2-2')]],
                            (2, 7): [[(6, '3-1', '2-1')], [(3, '1-1', '2-1')]],
                            (3, 8): [[(6, '2-2', '3-2')], [(2, '1-2', '3-2')]],
                            (3, 9): [[(6, '2-2', '3-1')], [(2, '1-2', '3-1')]],
                            (4, 5): [[(3, '1-2', '2-2')], [(2, '1-2', '3-1'), (6, '3-1', '2-2')]],
                            (4, 6): [[(3, '1-2', '2-2')], [(2, '1-2', '3-1')]],
                            (4, 7): [[(3, '1-2', '2-1')], [(2, '1-2', '3-1'), (6, '3-1', '2-1')]],
                            (4, 8): [[(2, '1-2', '3-2')], [(3, '1-2', '2-2'), (6, '2-2', '3-2')]],
                            (4, 9): [[(3, '1-2', '2-2'), (6, '2-2', '3-1')], [(2, '1-2', '3-1')]],
                            (5, 1): [[(6, '2-1', '3-2'), (2, '3-2', '1-2')], [(3, '2-1', '1-2')]],
                            (5, 2): [[(6, '2-1', '3-2')], [(3, '2-1', '1-2')]],
                            (5, 4): [[(3, '2-1', '1-1')], [(6, '2-1', '3-2'), (2, '3-2', '1-1')]],
                            (5, 8): [[(6, '2-1', '3-2')], [(3, '2-1', '1-2'), (2, '1-2', '3-2')]],
                            (5, 9): [[(6, '2-1', '3-1')], [(3, '2-1', '1-2'), (2, '1-2', '3-1')]],
                            (6, 1): [[(2, '3-2', '1-2')], [(3, '2-1', '1-2')]],
                            (6, 4): [[(3, '2-1', '1-1')], [(2, '3-2', '1-1')]],
                            (7, 1): [[(3, '2-2', '1-2')], [(6, '2-2', '3-2'), (2, '3-2', '1-2')]],
                            (7, 2): [[(6, '2-2', '3-2')], [(3, '2-2', '1-2')]],
                            (7, 4): [[(3, '2-2', '1-1')], [(6, '2-2', '3-2'), (2, '3-2', '1-1')]],
                            (7, 8): [[(3, '2-2', '1-2'), (2, '1-2', '3-2')], [(6, '2-2', '3-2')]],
                            (7, 9): [[(6, '2-2', '3-1')], [(3, '2-2', '1-2'), (2, '1-2', '3-1')]],
                            (8, 1): [[(2, '3-1', '1-2')], [(6, '3-1', '2-1'), (3, '2-1', '1-2')]],
                            (8, 3): [[(2, '3-1', '1-1')], [(6, '3-1', '2-1')]],
                            (8, 4): [[(2, '3-1', '1-1')], [(6, '3-1', '2-1'), (3, '2-1', '1-1')]],
                            (8, 5): [[(6, '3-1', '2-2')], [(2, '3-1', '1-1'), (3, '1-1', '2-2')]],
                            (8, 7): [[(6, '3-1', '2-1')], [(2, '3-1', '1-1'), (3, '1-1', '2-1')]],
                            (9, 1): [[(2, '3-2', '1-2')], [(6, '3-2', '2-1'), (3, '2-1', '1-2')]],
                            (9, 3): [[(6, '3-2', '2-1')], [(2, '3-2', '1-1')]],
                            (9, 4): [[(6, '3-2', '2-1'), (3, '2-1', '1-1')], [(2, '3-2', '1-1')]],
                            (9, 5): [[(6, '3-2', '2-2')], [(2, '3-2', '1-1'), (3, '1-1', '2-2')]],
                            (9, 7): [[(6, '3-2', '2-1')], [(2, '3-2', '1-1'), (3, '1-1', '2-1')]]}

# The indicator of the shortest path for od pairs, 1 means the shortest path, 0 means not the shortest path
shortest_path_indicator = {(1, 5): [1, 0],
                           (1, 6): [1, 0],
                           (1, 7): [1, 0],
                           (1, 8): [1, 0],
                           (1, 9): [1, 0],
                           (2, 5): [1, 0],
                           (2, 7): [1, 0],
                           (3, 8): [1, 0],
                           (3, 9): [1, 0],
                           (4, 5): [1, 0],
                           (4, 6): [1, 0],
                           (4, 7): [1, 0],
                           (4, 8): [0, 1],
                           (4, 9): [1, 0],
                           (5, 1): [1, 0],
                           (5, 2): [1, 0],
                           (5, 4): [1, 0],
                           (5, 8): [1, 0],
                           (5, 9): [1, 0],
                           (6, 1): [1, 0],
                           (6, 4): [1, 0],
                           (7, 1): [0, 1],
                           (7, 2): [1, 0],
                           (7, 4): [1, 0],
                           (7, 8): [0, 1],
                           (7, 9): [1, 0],
                           (8, 1): [1, 0],
                           (8, 3): [0, 1],
                           (8, 4): [1, 0],
                           (8, 5): [1, 0],
                           (8, 7): [1, 0],
                           (9, 1): [1, 2],
                           (9, 3): [1, 0],
                           (9, 4): [1, 0],
                           (9, 5): [1, 0],
                           (9, 7): [1, 0]}

# The length of each section, only the lengths of sections (2,3) and (3,2) are set to 2.5d, and the lengths of the others are set to d.
distance_dict = {}
for i in range(3):
    for j in range(len(station_list[i]) - 1):
        if station_list[i][j] == 2 and station_list[i][j + 1] == 3:
            distance_dict[station_list[i][j], station_list[i][j + 1]] = 2.5
            distance_dict[station_list[i][j + 1], station_list[i][j]] = 2.5
        else:
            distance_dict[station_list[i][j], station_list[i][j + 1]] = 1
            distance_dict[station_list[i][j + 1], station_list[i][j]] = 1
for i in range(3):
    for j in range(len(station_list[i]) - 1):
        for j_1 in range(j + 1, len(station_list[i])):
            if (station_list[i][j], station_list[i][j_1]) in distance_dict.keys():
                continue
            else:
                tem_dis = sum(distance_dict[station_list[i][_], station_list[i][_ + 1]] for _ in range(j, j_1))
                distance_dict[station_list[i][j], station_list[i][j_1]] = tem_dis
                distance_dict[station_list[i][j_1], station_list[i][j]] = tem_dis

# Construct the SC-LTT model
m = Model('SC-LTT')

# Construct the variables
t_run = {}
t_dwell = {}
t_arr = {}
t_dep = {}
transfer_indicator = {}
od_pair_path_transfer_indicator = {}
od_pair_path_remaining_distance = {}
od_pair_path_selection = {}
od_pair_path_reachability = {}
od_pair_reachability = {}
f_od_pair_path = {}

# Running time variables of each last train in each section
# If the length of a section is 2.5d, the lower and upper limit of the train running time in this section are set to 13 and 15 respectively.
# If the length of a section is d, the lower and upper limit of the train running time in this section are set to 4 and 6 repectively.
for i in range(3):
    # for the up direction of each line
    for j in range(len(station_list[i]) - 1):
        var_name = 't_run_' + str(i + 1) + '_1_' + str(station_list[i][j]) + '_' + str(station_list[i][j + 1])
        if station_list[i][j] == 2 and station_list[i][j + 1] == 3:
            t_run[i + 1, 1, station_list[i][j], station_list[i][j + 1]] = m.addVar(lb=13, ub=15, vtype=GRB.INTEGER,
                                                                                   name=var_name)
        else:
            t_run[i + 1, 1, station_list[i][j], station_list[i][j + 1]] = m.addVar(lb=4, ub=6, vtype=GRB.INTEGER,
                                                                                   name=var_name)
    # for the down direction of each line
    for k in range(len(station_list[i]) - 1):
        var_name = 't_run_' + str(i + 1) + '_2_' + str(station_list[i][::-1][k]) + '_' + str(
            station_list[i][::-1][k + 1])
        if station_list[i][::-1][k] == 3 and station_list[i][::-1][k + 1] == 2:
            t_run[i + 1, 2, station_list[i][::-1][k], station_list[i][::-1][k + 1]] = m.addVar(lb=13, ub=15,
                                                                                               vtype=GRB.INTEGER,
                                                                                               name=var_name)
        else:
            t_run[i + 1, 2, station_list[i][::-1][k], station_list[i][::-1][k + 1]] = m.addVar(lb=4, ub=6,
                                                                                               vtype=GRB.INTEGER,
                                                                                               name=var_name)

# Dwell time variables of each last train at each station
# For each station, the lower and upper limit of the train dwell time are set to 1 and 2 respectively.
for i in range(3):
    # for the up direction of each line
    for j in range(len(station_list[i]) - 2):
        var_name = 't_dwell_' + str(i + 1) + '_1_' + str(station_list[i][j + 1])
        t_dwell[i + 1, 1, station_list[i][j + 1]] = m.addVar(lb=1, ub=2, vtype=GRB.INTEGER, name=var_name)
    # for the down direction of each line
    for k in range(len(station_list[i]) - 2):
        var_name = 't_dwell_' + str(i + 1) + '_2_' + str(station_list[i][::-1][k + 1])
        t_dwell[i + 1, 2, station_list[i][::-1][k + 1]] = m.addVar(lb=1, ub=2, vtype=GRB.INTEGER, name=var_name)

# Arrival time variables of each last train at each station
for i in range(3):
    # for the up direction of each line
    for j in range(len(station_list[i]) - 1):
        var_name = 't_arr_' + str(i + 1) + '_1_' + str(station_list[i][j + 1])
        t_arr[i + 1, 1, station_list[i][j + 1]] = m.addVar(vtype=GRB.INTEGER, name=var_name)
    # for the down direction of each line
    for k in range(len(station_list[i]) - 1):
        var_name = 't_arr_' + str(i + 1) + '_2_' + str(station_list[i][::-1][k + 1])
        t_arr[i + 1, 2, station_list[i][::-1][k + 1]] = m.addVar(vtype=GRB.INTEGER, name=var_name)

# Departure time variables of each last train at each station
for i in range(3):
    # for the up direction of each line
    for j in range(len(station_list[i]) - 1):
        var_name = 't_dep_' + str(i + 1) + '_1_' + str(station_list[i][j])
        t_dep[i + 1, 1, station_list[i][j]] = m.addVar(vtype=GRB.INTEGER, name=var_name)
    # for the down direction of each line
    for k in range(len(station_list[i]) - 1):
        var_name = 't_dep_' + str(i + 1) + '_2_' + str(station_list[i][::-1][k])
        t_dep[i + 1, 2, station_list[i][::-1][k]] = m.addVar(vtype=GRB.INTEGER, name=var_name)

# Transfer status indicator variables of each transfer connection
for transfer_connection in transfer_connection_list:
    var_name = 'transfer_indicator_' + str(transfer_connection[0]) + '_' + transfer_connection[1] + '_' + \
               transfer_connection[2]
    transfer_indicator[
        transfer_connection[0], int(transfer_connection[1][0]), int(transfer_connection[1][2]), int(
            transfer_connection[2][0]), int(
            transfer_connection[2][2])] = m.addVar(vtype=GRB.BINARY, name=var_name)

# Transfer status indicator variables of each od pair's transfer connection
# For example, the key of (1, 5, 1, 2, 1, 1, 3, 1) is set for the transfer status indicator variable of od pair (1, 5)'s transfer connection from the up direction of line 1 to the up direction of line 3 at transfer station 2 on its first path.
for od_pair in transfer_connection_dict:
    for i in range(len(transfer_connection_dict[od_pair])):
        for j in range(len(transfer_connection_dict[od_pair][i])):
            var_name = str(od_pair[0]) + '_' + str(od_pair[1]) + '_path_' + str(i + 1) + '_transfer_indicator_' + str(
                transfer_connection_dict[od_pair][i][j][0]) + '_' + transfer_connection_dict[od_pair][i][j][1] + '_' + \
                       transfer_connection_dict[od_pair][i][j][2]
            od_pair_path_transfer_indicator[
                od_pair[0], od_pair[1], i + 1, transfer_connection_dict[od_pair][i][j][0], int(
                    transfer_connection_dict[od_pair][i][j][1][0]), int(
                    transfer_connection_dict[od_pair][i][j][1][2]), int(
                    transfer_connection_dict[od_pair][i][j][2][0]), int(
                    transfer_connection_dict[od_pair][i][j][2][2])] = m.addVar(
                vtype=GRB.BINARY, name=var_name)

# Path remaining distance variables of each od pair's candidate paths
for od_pair in path_dict:
    for i in range(len(path_dict[od_pair])):
        var_name = str(od_pair[0]) + '_' + str(od_pair[1]) + '_path_' + str(i + 1) + '_remaining_distance'
        od_pair_path_remaining_distance[od_pair[0], od_pair[1], i + 1] = m.addVar(vtype=GRB.CONTINUOUS,
                                                                                  name=var_name)

# Path allocation variables of each od pair
for od_pair in path_dict:
    for i in range(len(path_dict[od_pair])):
        var_name = str(od_pair[0]) + '_' + str(od_pair[1]) + '_path_' + str(i + 1) + '_selection'
        od_pair_path_selection[od_pair[0], od_pair[1], i + 1] = m.addVar(vtype=GRB.BINARY, name=var_name)

# Destination reachability variables of each od pairs' candidate paths
for od_pair in path_dict:
    for i in range(len(path_dict[od_pair])):
        var_name = str(od_pair[0]) + '_' + str(od_pair[1]) + '_path_' + str(i + 1) + '_reachability'
        od_pair_path_reachability[od_pair[0], od_pair[1], i + 1] = m.addVar(vtype=GRB.BINARY, name=var_name)

# Destination reachability variables of each od pair
for od_pair in path_dict:
    var_name = str(od_pair[0]) + '_' + str(od_pair[1]) + '_reachability'
    od_pair_reachability[od_pair[0], od_pair[1]] = m.addVar(vtype=GRB.BINARY, name=var_name)

# Auxiliary variables for linearization of the objective function z2
for od_pair in path_dict:
    for i in range(len(path_dict[od_pair])):
        var_name = 'auxiliary_f_' + str(od_pair[0]) + '_' + str(od_pair[1]) + '_' + str(i + 1)
        f_od_pair_path[od_pair[0], od_pair[1], i + 1] = m.addVar(vtype=GRB.CONTINUOUS, name=var_name)

# Construct the constraints
# Constrains (4)
for i in range(3):
    # for the up direction of each line
    for j in range(len(station_list[i]) - 1):
        expr_1 = LinExpr(0)
        for j_1 in range(j + 1):
            expr_1 += t_run[i + 1, 1, station_list[i][j_1], station_list[i][j_1 + 1]]
        expr_2 = LinExpr(0)
        for j_2 in range(1, j + 1):
            expr_2 += t_dwell[i + 1, 1, station_list[i][j_2]]
        m.addConstr(t_arr[i + 1, 1, station_list[i][j + 1]] == t_dep[i + 1, 1, station_list[i][0]] + expr_1 + expr_2,
                    't_arr_' + str(i + 1) + '_1_' + str(station_list[i][j + 1]))
    # for the down direction of each line
    for k in range(len(station_list[i]) - 1):
        expr_1 = LinExpr(0)
        for k_1 in range(k + 1):
            expr_1 += t_run[i + 1, 2, station_list[i][::-1][k_1], station_list[i][::-1][k_1 + 1]]
        expr_2 = LinExpr(0)
        for k_2 in range(1, k + 1):
            expr_2 += t_dwell[i + 1, 2, station_list[i][::-1][k_2]]
        m.addConstr(
            t_arr[i + 1, 2, station_list[i][::-1][k + 1]] == t_dep[
                i + 1, 2, station_list[i][::-1][0]] + expr_1 + expr_2,
            't_arr_' + str(i + 1) + '_2_' + str(station_list[i][::-1][k + 1]))

# Constrains (5)
for i in range(3):
    # for the up direction of each line
    for j in range(len(station_list[i]) - 1):
        if j == 0:
            m.addConstr(t_dep[i + 1, 1, station_list[i][j]] == t_dep[i + 1, 1, station_list[i][0]],
                        't_dep_' + str(i + 1) + '_1_' + str(station_list[i][j]))
        else:
            expr_1 = LinExpr(0)
            for j_1 in range(j):
                expr_1 += t_run[i + 1, 1, station_list[i][j_1], station_list[i][j_1 + 1]]
            expr_2 = LinExpr(0)
            for j_2 in range(1, j + 1):
                expr_2 += t_dwell[i + 1, 1, station_list[i][j_2]]
            m.addConstr(t_dep[i + 1, 1, station_list[i][j]] == t_dep[i + 1, 1, station_list[i][0]] + expr_1 + expr_2,
                        't_dep_' + str(i + 1) + '_1_' + str(station_list[i][j]))
    # for the down direction of each line
    for k in range(len(station_list[i]) - 1):
        if k == 0:
            m.addConstr(t_dep[i + 1, 2, station_list[i][::-1][k]] == t_dep[i + 1, 2, station_list[i][::-1][0]],
                        't_dep_' + str(i + 1) + '_2_' + str(station_list[i][::-1][k]))
        else:
            expr_1 = LinExpr(0)
            for k_1 in range(k):
                expr_1 += t_run[i + 1, 2, station_list[i][::-1][k_1], station_list[i][::-1][k_1 + 1]]
            expr_2 = LinExpr(0)
            for k_2 in range(1, k + 1):
                expr_2 += t_dwell[i + 1, 2, station_list[i][::-1][k_2]]
            m.addConstr(
                t_dep[i + 1, 2, station_list[i][::-1][k]] == t_dep[
                    i + 1, 2, station_list[i][::-1][0]] + expr_1 + expr_2,
                't_dep_' + str(i + 1) + '_2_' + str(station_list[i][::-1][k]))

# In the small case, since there are no restrictions on the penultimate trains, only the departure time horizons of the last trains at the departure stations are restricted.
m.addConstr(
    t_dep[1, 1, station_list[0][0]] >= 10, 't_dep_earliest_1_1_' + str(station_list[0][0]))
m.addConstr(
    t_dep[1, 1, station_list[0][0]] <= 15, 't_dep_latest_1_1_' + str(station_list[0][0]))
m.addConstr(t_dep[1, 2, station_list[0][::-1][0]] >= 5,
            't_dep_earliest_1_2_' + str(station_list[0][::-1][0]))
m.addConstr(t_dep[1, 2, station_list[0][::-1][0]] <= 10,
            't_dep_latest_1_2_' + str(station_list[0][::-1][0]))

m.addConstr(
    t_dep[2, 1, station_list[1][0]] >= 0, 't_dep_earliest_2_1_' + str(station_list[1][0]))
m.addConstr(
    t_dep[2, 1, station_list[1][0]] <= 5, 't_dep_latest_2_1_' + str(station_list[1][0]))
m.addConstr(t_dep[2, 2, station_list[1][::-1][0]] >= 5,
            't_dep_earliest_2_2_' + str(station_list[1][::-1][0]))
m.addConstr(t_dep[2, 2, station_list[1][::-1][0]] <= 10,
            't_dep_latest_2_2_' + str(station_list[1][::-1][0]))

m.addConstr(
    t_dep[3, 1, station_list[2][0]] >= 15, 't_dep_earliest_3_1_' + str(station_list[2][0]))
m.addConstr(
    t_dep[3, 1, station_list[2][0]] <= 20, 't_dep_latest_3_1_' + str(station_list[2][0]))
m.addConstr(t_dep[3, 2, station_list[2][::-1][0]] >= 10,
            't_dep_earliest_3_2_' + str(station_list[2][::-1][0]))
m.addConstr(t_dep[3, 2, station_list[2][::-1][0]] <= 15,
            't_dep_latest_3_2_' + str(station_list[2][::-1][0]))

# Constraints (13), there are no non-multimodal passengers in the small case, the calculation of the transfer waiting time is also contained in this constraint instead of constructing Constraints (11) extraly
for transfer_connection in transfer_connection_list:
    m.addConstr(t_dep[int(transfer_connection[2][0]), int(transfer_connection[2][2]), transfer_connection[0]] - (
            t_arr[int(transfer_connection[1][0]), int(transfer_connection[1][2]), transfer_connection[
                0]] + 1.5) <= -0.5 + 100 *
                transfer_indicator[
                    transfer_connection[0], int(transfer_connection[1][0]), int(transfer_connection[1][2]), int(
                        transfer_connection[2][0]), int(
                        transfer_connection[2][2])],
                'transfer_status_1_' + str(transfer_connection[0]) + '_' + transfer_connection[1] + '_' +
                transfer_connection[2])
    m.addConstr(t_dep[int(transfer_connection[2][0]), int(transfer_connection[2][2]), transfer_connection[0]] - (
            t_arr[
                int(transfer_connection[1][0]), int(transfer_connection[1][2]), transfer_connection[0]] + 1.5) >= 100 *
                (transfer_indicator[
                     transfer_connection[0], int(transfer_connection[1][0]), int(transfer_connection[1][2]), int(
                         transfer_connection[2][0]), int(
                         transfer_connection[2][2])] - 1),
                'transfer_status_2_' + str(transfer_connection[0]) + '_' + transfer_connection[1] + '_' +
                transfer_connection[2])

# Constraints (16), (27)
for od_pair in transfer_connection_dict:
    for i in range(len(transfer_connection_dict[od_pair])):
        for j in range(len(transfer_connection_dict[od_pair][i])):
            if j == 0:
                m.addConstr(od_pair_path_transfer_indicator[
                                od_pair[0], od_pair[1], i + 1, transfer_connection_dict[od_pair][i][j][0], int(
                                    transfer_connection_dict[od_pair][i][j][1][0]), int(
                                    transfer_connection_dict[od_pair][i][j][1][2]), int(
                                    transfer_connection_dict[od_pair][i][j][2][0]), int(
                                    transfer_connection_dict[od_pair][i][j][2][2])] == transfer_indicator[
                                transfer_connection_dict[od_pair][i][j][0], int(
                                    transfer_connection_dict[od_pair][i][j][1][0]), int(
                                    transfer_connection_dict[od_pair][i][j][1][2]), int(
                                    transfer_connection_dict[od_pair][i][j][2][0]), int(
                                    transfer_connection_dict[od_pair][i][j][2][2])],
                            'od_' + str(od_pair[0]) + '_' + str(od_pair[1]) + '_path_' + str(
                                i + 1) + '_transfer_status_' + str(
                                transfer_connection_dict[od_pair][i][j][0]) + '_' +
                            transfer_connection_dict[od_pair][i][j][
                                1] + '_' +
                            transfer_connection_dict[od_pair][i][j][2])
            else:
                m.addConstr(od_pair_path_transfer_indicator[
                                od_pair[0], od_pair[1], i + 1, transfer_connection_dict[od_pair][i][j][0], int(
                                    transfer_connection_dict[od_pair][i][j][1][0]), int(
                                    transfer_connection_dict[od_pair][i][j][1][2]), int(
                                    transfer_connection_dict[od_pair][i][j][2][0]), int(
                                    transfer_connection_dict[od_pair][i][j][2][2])] <= od_pair_path_transfer_indicator[
                                od_pair[0], od_pair[1], i + 1, transfer_connection_dict[od_pair][i][j - 1][0], int(
                                    transfer_connection_dict[od_pair][i][j - 1][1][0]), int(
                                    transfer_connection_dict[od_pair][i][j - 1][1][2]), int(
                                    transfer_connection_dict[od_pair][i][j - 1][2][0]), int(
                                    transfer_connection_dict[od_pair][i][j - 1][2][2])],
                            'od_' + str(od_pair[0]) + '_' + str(od_pair[1]) + '_path_' + str(
                                i + 1) + '_transfer_status_' + str(
                                transfer_connection_dict[od_pair][i][j][0]) + '_' +
                            transfer_connection_dict[od_pair][i][j][
                                1] + '_' +
                            transfer_connection_dict[od_pair][i][j][2] + '_1')
                m.addConstr(od_pair_path_transfer_indicator[
                                od_pair[0], od_pair[1], i + 1, transfer_connection_dict[od_pair][i][j][0], int(
                                    transfer_connection_dict[od_pair][i][j][1][0]), int(
                                    transfer_connection_dict[od_pair][i][j][1][2]), int(
                                    transfer_connection_dict[od_pair][i][j][2][0]), int(
                                    transfer_connection_dict[od_pair][i][j][2][2])] <= transfer_indicator[
                                transfer_connection_dict[od_pair][i][j][0], int(
                                    transfer_connection_dict[od_pair][i][j][1][0]), int(
                                    transfer_connection_dict[od_pair][i][j][1][2]), int(
                                    transfer_connection_dict[od_pair][i][j][2][0]), int(
                                    transfer_connection_dict[od_pair][i][j][2][2])],
                            'od_' + str(od_pair[0]) + '_' + str(od_pair[1]) + '_path_' + str(
                                i + 1) + '_transfer_status_' + str(
                                transfer_connection_dict[od_pair][i][j][0]) + '_' +
                            transfer_connection_dict[od_pair][i][j][
                                1] + '_' +
                            transfer_connection_dict[od_pair][i][j][2] + '_2')
                m.addConstr(od_pair_path_transfer_indicator[
                                od_pair[0], od_pair[1], i + 1, transfer_connection_dict[od_pair][i][j][0], int(
                                    transfer_connection_dict[od_pair][i][j][1][0]), int(
                                    transfer_connection_dict[od_pair][i][j][1][2]), int(
                                    transfer_connection_dict[od_pair][i][j][2][0]), int(
                                    transfer_connection_dict[od_pair][i][j][2][2])] >= od_pair_path_transfer_indicator[
                                od_pair[0], od_pair[1], i + 1, transfer_connection_dict[od_pair][i][j - 1][0], int(
                                    transfer_connection_dict[od_pair][i][j - 1][1][0]), int(
                                    transfer_connection_dict[od_pair][i][j - 1][1][2]), int(
                                    transfer_connection_dict[od_pair][i][j - 1][2][0]), int(
                                    transfer_connection_dict[od_pair][i][j - 1][2][2])] + transfer_indicator[
                                transfer_connection_dict[od_pair][i][j][0], int(
                                    transfer_connection_dict[od_pair][i][j][1][0]), int(
                                    transfer_connection_dict[od_pair][i][j][1][2]), int(
                                    transfer_connection_dict[od_pair][i][j][2][0]), int(
                                    transfer_connection_dict[od_pair][i][j][2][2])] - 1,
                            'od_' + str(od_pair[0]) + '_' + str(od_pair[1]) + '_path_' + str(
                                i + 1) + '_transfer_status_' + str(
                                transfer_connection_dict[od_pair][i][j][0]) + '_' +
                            transfer_connection_dict[od_pair][i][j][
                                1] + '_' +
                            transfer_connection_dict[od_pair][i][j][2] + '_3')

# Constraints (18)
for od_pair in path_dict:
    for i in range(len(path_dict[od_pair])):
        expr = LinExpr(0)
        for j in range(1, len(path_dict[od_pair][i]) - 1):
            expr += distance_dict[path_dict[od_pair][i][j], path_dict[od_pair][i][j + 1]] * \
                    (1 - od_pair_path_transfer_indicator[
                        od_pair[0], od_pair[1], i + 1, path_dict[od_pair][i][j], int(
                            transfer_connection_dict[od_pair][i][j - 1][1][0]), int(
                            transfer_connection_dict[od_pair][i][j - 1][1][2]), int(
                            transfer_connection_dict[od_pair][i][j - 1][2][0]), int(
                            transfer_connection_dict[od_pair][i][j - 1][2][2])])
        m.addConstr(od_pair_path_remaining_distance[od_pair[0], od_pair[1], i + 1] == expr,
                    str(od_pair[0]) + '_' + str(od_pair[1]) + '_path_' + str(i + 1) + '_remaining_distance')

# Constraints (28)
for od_pair in path_dict:
    for i in range(len(path_dict[od_pair])):
        m.addConstr(
            - (od_pair_path_remaining_distance[od_pair[0], od_pair[1], i + 1] - 0.5) - 100 * od_pair_path_reachability[
                od_pair[0], od_pair[1], i + 1] <= 0,
            str(od_pair[0]) + '_' + str(od_pair[1]) + '_path_' + str(i + 1) + '_reachability_1')
        m.addConstr(
            od_pair_path_remaining_distance[od_pair[0], od_pair[1], i + 1] - 100 * (1 - od_pair_path_reachability[
                od_pair[0], od_pair[1], i + 1]) <= 0,
            str(od_pair[0]) + '_' + str(od_pair[1]) + '_path_' + str(i + 1) + '_reachability_2')

# Constraints (20), (21)
for od_pair in path_dict:
    expr = LinExpr(0)
    for i in range(len(path_dict[od_pair])):
        expr += od_pair_path_reachability[od_pair[0], od_pair[1], i + 1]
        m.addConstr(
            od_pair_reachability[od_pair[0], od_pair[1]] >= od_pair_path_reachability[od_pair[0], od_pair[1], i + 1],
            str(od_pair[0]) + '_' + str(od_pair[1]) + '_reachability_' + str(i + 1))
    m.addConstr(od_pair_reachability[od_pair[0], od_pair[1]] <= expr,
                str(od_pair[0]) + '_' + str(od_pair[1]) + '_reachability_' + str(len(path_dict[od_pair]) + 1))

# Constraints (22)
for od_pair in path_dict:
    expr = LinExpr(0)
    for i in range(len(path_dict[od_pair])):
        expr += od_pair_path_selection[od_pair[0], od_pair[1], i + 1]
    m.addConstr(expr == 1, str(od_pair[0]) + '_' + str(od_pair[1]) + '_path_selection')

# Linearization constraints, i.e., Constraints (30)
for od_pair in path_dict:
    for i in range(len(path_dict[od_pair])):
        m.addConstr(f_od_pair_path[od_pair[0], od_pair[1], i + 1] <= 100 * od_pair_path_selection[
            od_pair[0], od_pair[1], i + 1],
                    'linear_' + str(od_pair[0]) + '_' + str(od_pair[1]) + '_' + str(i + 1) + '_1')
        m.addConstr(f_od_pair_path[od_pair[0], od_pair[1], i + 1] <= od_pair_path_remaining_distance[
            od_pair[0], od_pair[1], i + 1],
                    'linear_' + str(od_pair[0]) + '_' + str(od_pair[1]) + '_' + str(i + 1) + '_2')
        m.addConstr(f_od_pair_path[od_pair[0], od_pair[1], i + 1] >= od_pair_path_remaining_distance[
            od_pair[0], od_pair[1], i + 1] - 100 * (1 - od_pair_path_selection[od_pair[0], od_pair[1], i + 1]),
                    'linear_' + str(od_pair[0]) + '_' + str(od_pair[1]) + '_' + str(i + 1) + '_3')

# The objective is to maximize the number of reachable passengers.
obj_3 = LinExpr(0)
for od_pair in path_dict:
    for i in range(len(path_dict[od_pair])):
        obj_3 += demands.loc[od_pair] * f_od_pair_path[od_pair[0], od_pair[1], i + 1]

m.setObjective(obj_3, GRB.MINIMIZE)

m.optimize()

# The departure time of each last train on each line at each station
for i in range(3):
    for j in range(len(station_list[i]) - 1):
        print('The departure time of last train on the up direction of line ' + str(i + 1) + ' at station ' + str(
            station_list[i][j]) + ': ' +
              (initial_time + timedelta(minutes=int(t_dep[i + 1, 1, station_list[i][j]].X))).strftime("%H:%M:%S"))
    for k in range(len(station_list[i]) - 1):
        print('The departure time of last train on the down direction of line ' + str(i + 1) + ' at station ' + str(
            station_list[i][::-1][k]) + ': ' +
              (initial_time + timedelta(minutes=int(t_dep[i + 1, 2, station_list[i][::-1][k]].X))).strftime("%H:%M:%S"))
print()

# The arrival time of each last train on each line at each station
for i in range(3):
    for j in range(len(station_list[i]) - 1):
        print('The arrival time of last train on the up direction of line ' + str(i + 1) + ' at station ' + str(
            station_list[i][j + 1]) + ': ' +
              (initial_time + timedelta(minutes=int(t_arr[i + 1, 1, station_list[i][j + 1]].X))).strftime("%H:%M:%S"))
    for k in range(len(station_list[i]) - 1):
        print('The arrival time of last train on the down direction of line ' + str(i + 1) + ' at station ' + str(
            station_list[i][::-1][k + 1]) + ': ' +
              (initial_time + timedelta(minutes=int(t_arr[i + 1, 2, station_list[i][::-1][k + 1]].X))).strftime(
                  "%H:%M:%S"))

print()

# The transfer status of each transfer connection
transfer_num = 0
for transfer_connection in transfer_connection_list:
    if transfer_indicator[
        transfer_connection[0], int(transfer_connection[1][0]), int(transfer_connection[1][2]), int(
            transfer_connection[2][0]), int(
            transfer_connection[2][2])].X == 1:
        transfer_num += 1
        print('Transfer connection ' + str(transfer_connection) + ' succeeds.')
    else:
        print('Transfer connection ' + str(transfer_connection) + ' fails.')
# The number of successful transfer connections
print()
print('The number of successful transfer connections: ' + str(transfer_num))
print()

# Destination reachability and path allocation scheme of each od pair
reachable_num = 0
for od_pair in path_dict:
    for i in range(len(path_dict[od_pair])):
        if od_pair_path_selection[od_pair[0], od_pair[1], i + 1].X == 1:
            print('The path allocated to od pair ' + str(od_pair) + ': ' + str(path_dict[od_pair][i]))
    if od_pair_reachability[od_pair[0], od_pair[1]].X == 1:
        reachable_num += demands.loc[od_pair]
    print('The destination reachability of od pair ' + str(od_pair) + ': ' +
          str(int(od_pair_reachability[od_pair[0], od_pair[1]].X)))
# The number of reachable passengers
print()
print('The number of reachable passengers: ' + str(reachable_num))
print()

# The total path remaining distance of passengers
print('The total path remaining distance of passengers: ' + str(int(obj_3.getValue())) + 'd')
