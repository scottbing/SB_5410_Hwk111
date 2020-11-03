import random


# finds shortest path between 2 nodes of a graph using BFS
def bfs_shortest_path(graph: dict, start: str, goal: str):
    # keep track of explored nodes
    explored = []
    # keep track of all the paths to be checked
    queue = [[start]]

    # return path if start is goal
    if start == goal:
        # return "That was easy! Start = goal"
        return [start]

    # keeps looping until all possible paths have been checked
    while queue:
        # pop the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        if node not in explored:
            neighbours = graph[node]
            # go through all neighbour nodes, construct a new path and
            # push it into the queue
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                # return path if neighbour is goal
                if neighbour == goal:
                    return new_path

            # mark node as explored
            explored.append(node)

    # in case there's no path between the 2 nodes
    return "A path doesn't exist "

# end def bfs_shortest_path(graph, start, goal):


def main():
    graph = {"Omaha"        : ["Dallas", "Houston", "Chicago"],
             "Louisville"   : ["Dallas", "Houston", "Baltimore", "Chicago"],
             "Baltimore"    : ["Jacksonville", "Louisville", "Houston", "Dallas", "Portland", "Chicago"],
             "Portland"     : ["Baltimore"],
             "Jacksonville" : ["Dallas", "Houston", "Baltimore", "Chicago"],
             "Belize City" :  [],
             "Dallas"  	    : ["Houston", "Baltimore", "Jacksonville", "Louisville", "Chicago", "Omaha"],
             "Houston"  	: ["Dallas" ,  "Baltimore", "Jacksonville", "Louisville", "Chicago", "Omaha"],
             "Chicago"		: ["Dallas",  "Baltimore", "Jacksonville", "Louisville", "Omaha", "Houston"]
             }

    path=bfs_shortest_path(graph, 'Omaha', 'Louisville')
    print("From Omaha to Louisville: " + str(path))

    path1 = bfs_shortest_path(graph, 'Baltimore', 'Jacksonville')
    #print("From Baltimore to Jacksonville: " + str(path1))

    path2 = bfs_shortest_path(graph, 'Jacksonville', 'Portland')
    print("From Baltimore to Jacksonville: " + str(path1) + " to Portland, Maine: " + str(path2))

    path = bfs_shortest_path(graph, 'Belize City', 'Portland')
    print("From Belize City to Portland, Maine: " + str(path))


# end def main():

if __name__ == "__main__":
    main()
