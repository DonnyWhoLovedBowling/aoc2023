import logging
from logging import info, debug
import matplotlib.pyplot as plt
import networkx as nx
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex25.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]
connections = nx.Graph()



def make_group(link, group):
    if link in group:
        return
    group.add(link)
    for c in connections[link]:
        make_group(c, group)


def remove_connection(link1, link2):
    global connections
    connections[link1].remove(link2)
    connections[link2].remove(link1)


def count_groups():
    groups = []
    marked_links = set()
    for c in connections.keys():
        if c in marked_links:
            continue
        group1 = set()
        make_group(c, group1)
        groups.append(group1)
        marked_links = marked_links | group1
    return len(groups)

def pt1():
    global connections

    for line in lines:
        split = line.split(":")
        c1 = split[0]
        connected = {c.strip() for c in split[1].split(" ") if c.strip() != ''}
        for c2 in connected:
            connections.add_edge(c1, c2)

    options = {
        "font_size": 8,
        "node_size": 1000,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 2,
        "width": 1,
    }

    # nx.draw_networkx(connections, **options)
    # plt.show()

    connections.remove_edge("pcs", "rrl")
    connections.remove_edge("qnd", "mbk")
    connections.remove_edge("lcm", "ddl")

    sizes = [len(c) for c in nx.connected_components(connections)]
    info(f"ans pt1: {sizes[0] * sizes[1]}")
    debug(sizes)
    nx.draw_networkx(connections, **options)
    plt.show()


if __name__ == '__main__':
    pt1()
