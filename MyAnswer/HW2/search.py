from collections import deque
import heapq
import random
from dataloader import *

def bfs(start, end):
    edges = edgeloader('edges.csv')
    
    bfs_path = []
    bfs_dist = 0
    bfs_visited = 0

    node_info = {}
    for node_idx in edges:
        node_info[node_idx] = {'distance': 0, 'discover': 0, 'pre' : 0}
    queue = deque()
    queue.append(str(start))
    node_info[str(start)]['discover'] = 1

    while len(queue) > 0:
        bfs_visited += 1
        current_node = queue.popleft()
        if current_node == str(end):
            break
        for next_node in edges[current_node]:
            if next_node in node_info and node_info[next_node]['discover'] == 0:
                queue.append(next_node)
                node_info[next_node]['distance'] = node_info[current_node]['distance'] + 1
                node_info[next_node]['pre'] = current_node
                node_info[next_node]['discover'] = 1
        node_info[current_node]['discover'] = 2
    
    #back tracing
    cur = str(end)
    bfs_path.append(end)
    while cur != str(start):
        bfs_dist += edges[node_info[cur]['pre']][cur]['distance']
        cur = node_info[cur]['pre']
        bfs_path.append(int(cur))
    bfs_path.reverse()
    return bfs_path, bfs_dist, bfs_visited
    

def dfs(start, end):
    edges = edgeloader('edges.csv')

    dfs_path = []
    dfs_dist = 0
    dfs_visited = 0

    node_info = {}
    for node_idx in edges:
        node_info[node_idx] = {'distance': 0, 'discover': 0, 'pre' : 0}
    stack = deque()
    stack.append(str(start))
    node_info[str(start)]['discover'] = 1

    while len(stack) > 0:
        dfs_visited += 1
        current_node = stack.pop()
        node_info[current_node]['discover'] = 1
        if current_node == str(end):
            break
        for next_node in edges[current_node]:
            if next_node in node_info and node_info[next_node]['discover'] == 0:
                stack.append(next_node)
                node_info[next_node]['distance'] = node_info[current_node]['distance'] + 1
                node_info[next_node]['pre'] = current_node
        node_info[current_node]['discover'] = 2
    
    #back tracing
    cur = str(end)
    dfs_path.append(end)
    while cur != str(start):
        dfs_dist += edges[node_info[cur]['pre']][cur]['distance']
        cur = node_info[cur]['pre']
        dfs_path.append(int(cur))
    dfs_path.reverse()
    return dfs_path, dfs_dist, dfs_visited
    

def ucs(start, end):
    edges = edgeloader('edges.csv')

    ucs_path = []
    ucs_dist = 0
    ucs_visited = 0

    node_info = {}
    for node_idx in edges:
        node_info[node_idx] = {'distance': 0, 'discover': 0, 'pre' : 0}
    priorirty_queue = []
    
    heapq.heappush(priorirty_queue, (0, str(start)))
    node_info[str(start)]['discover'] = 1
    while len(priorirty_queue) > 0:
        ucs_visited += 1
        current_node = heapq.heappop(priorirty_queue)[1]
        if current_node == str(end):
            break
        for next_node in edges[current_node]:
            if next_node in node_info and node_info[next_node]['discover'] == 0:
                node_info[next_node]['distance'] = node_info[current_node]['distance'] + edges[current_node][next_node]['distance']
                node_info[next_node]['pre'] = current_node
                node_info[next_node]['discover'] = 1
                heapq.heappush(priorirty_queue, (node_info[next_node]['distance'], next_node))
            elif next_node in node_info and node_info[next_node]['discover'] == 1:
                for item in priorirty_queue:
                    if item[1] == next_node:
                        new_distance = node_info[current_node]['distance'] + edges[current_node][next_node]['distance']
                        if item[0] > new_distance:
                            node_info[next_node]['distance'] = new_distance
                            node_info[next_node]['pre'] = current_node
                            item = (node_info[next_node]['distance'], next_node)
                            heapq.heapify(priorirty_queue)
                        break
        node_info[current_node]['discover'] = 2

    cur = str(end)
    ucs_path.append(end)
    while cur != str(start):
        ucs_dist += edges[node_info[cur]['pre']][cur]['distance']
        cur = node_info[cur]['pre']
        ucs_path.append(int(cur))
    ucs_path.reverse()
    return ucs_path, ucs_dist, ucs_visited
    

def astar(start, end):
    edges = edgeloader('edges.csv')
    heuristic = heuristic_loader('heuristic.csv')

    astar_path = []
    astar_dist = 0
    astar_visited = 0

    node_info = {}
    for node_idx in edges:
        node_info[node_idx] = {'distance': 0, 'discover': 0, 'pre' : 0}
    priorirty_queue = []

    heapq.heappush(priorirty_queue, (0, str(start)))
    node_info[str(start)]['discover'] = 1
    while len(priorirty_queue) > 0:
        astar_visited += 1
        current_node = heapq.heappop(priorirty_queue)[1]
        if current_node == str(end):
            break
        for next_node in edges[current_node]:
            if next_node in node_info and node_info[next_node]['discover'] == 0:
                node_info[next_node]['distance'] = node_info[current_node]['distance'] + edges[current_node][next_node]['distance']
                node_info[next_node]['pre'] = current_node
                node_info[next_node]['discover'] = 1
                heapq.heappush(priorirty_queue, (node_info[next_node]['distance'] + heuristic[next_node][str(end)], next_node))
            elif next_node in node_info and node_info[next_node]['discover'] == 1:
                for item in priorirty_queue:
                    if item[1] == next_node:
                        new_distance = node_info[current_node]['distance'] + edges[current_node][next_node]['distance']
                        if item[0] > new_distance + heuristic[next_node][str(end)]:
                            node_info[next_node]['distance'] = new_distance
                            node_info[next_node]['pre'] = current_node
                            item = (node_info[next_node]['distance'] + heuristic[next_node][str(end)], next_node)
                            heapq.heapify(priorirty_queue)
                        break
        node_info[current_node]['discover'] = 2

    cur = str(end)
    astar_path.append(end)
    while cur != str(start):
        astar_dist += edges[node_info[cur]['pre']][cur]['distance']
        cur = node_info[cur]['pre']
        astar_path.append(int(cur))
    astar_path.reverse()
    
    return astar_path, astar_dist, astar_visited
    

def astar_time(start, end):
    edges = edgeloader('edges.csv')
    heuristic = heuristic_loader('heuristic.csv')

    time_path = []
    time_dist = 0
    time_visited = 0

    total_distance = 0
    total_time = 0
    edges = edgeloader('edges.csv')
    for i in edges:
        for j in edges[i]:
            edges[i][j]['time'] = edges[i][j]['distance'] / (edges[i][j]['speed_limit'] / 2)
            edges[i][j]['time'] = max(random.gauss(edges[i][j]['time'], 5), 1)
            total_distance += edges[i][j]['distance']
            total_time += edges[i][j]['distance'] / edges[i][j]['speed_limit']
    
    avg_speed = total_distance / total_time
    for h in heuristic:
        heuristic[h][str(end)] = heuristic[h][str(end)] / max(avg_speed - 15, 1)

    node_info = {}
    for node_idx in edges:
        node_info[node_idx] = {'time': 0, 'discover': 0, 'pre' : 0}
    priorirty_queue = []

    heapq.heappush(priorirty_queue, (0, str(start)))
    node_info[str(start)]['discover'] = 1
    while len(priorirty_queue) > 0:
        time_visited += 1
        current_node = heapq.heappop(priorirty_queue)[1]
        if current_node == str(end):
            break
        for next_node in edges[current_node]:
            if next_node in node_info and node_info[next_node]['discover'] == 0:
                node_info[next_node]['time'] = node_info[current_node]['time'] + edges[current_node][next_node]['time']
                node_info[next_node]['pre'] = current_node
                node_info[next_node]['discover'] = 1
                heapq.heappush(priorirty_queue, (node_info[next_node]['time'] + heuristic[next_node][str(end)], next_node))
            elif next_node in node_info and node_info[next_node]['discover'] == 1:
                for item in priorirty_queue:
                    if item[1] == next_node:
                        new_distance = node_info[current_node]['time'] + edges[current_node][next_node]['time']
                        if item[0] > new_distance + heuristic[next_node][str(end)]:
                            node_info[next_node]['time'] = new_distance
                            node_info[next_node]['pre'] = current_node
                            item = (node_info[next_node]['time'] + heuristic[next_node][str(end)], next_node)
                            heapq.heapify(priorirty_queue)
                        break
        node_info[current_node]['discover'] = 2

    cur = str(end)
    time_path.append(end)
    while cur != str(start):
        time_dist += edges[node_info[cur]['pre']][cur]['time']
        cur = node_info[cur]['pre']
        time_path.append(int(cur))
    time_path.reverse()

    return time_path, time_dist, time_visited

