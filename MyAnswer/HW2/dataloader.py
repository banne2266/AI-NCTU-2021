import csv

def edgeloader(filename):
    edge_dict = {}
    with open(filename, newline='') as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            if row[0] == 'start':
                continue
            if row[0] in edge_dict:
                edge_dict[row[0]][row[1]] = {'distance':float(row[2]), 'speed_limit':float(row[3])}
            else:
                edge_dict[row[0]] = {row[1] : {'distance':float(row[2]), 'speed_limit':float(row[3])}}
    return edge_dict


def heuristic_loader(filename):
    heuristic_dict = {}
    with open(filename, newline='') as csvfile:
        rows = csv.reader(csvfile)
        go_list = []
        for row in rows:
            if row[0] == 'node':
                for go in row[1:]:
                    go_list.append(go)
            else:
                heuristic_dict[row[0]] = {}
                for i in range(len(go_list)):
                    heuristic_dict[row[0]][go_list[i]] = float(row[i+1])
    return heuristic_dict
