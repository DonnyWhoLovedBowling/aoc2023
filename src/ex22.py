import logging
from logging import info, debug
from copy import deepcopy as dc
from collections import deque

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex22.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]

supports_map = dict()
supported_by_map = dict()
bricks_by_z_min = dict()
bricks_by_z_max = dict()
bricks = dict()


def supports(bid1, bid2, test_z=True):

    if bid1 == bid2:
        return False
    if bricks[bid2]['z_min'] != (bricks[bid1]['z_max'] + 1) and test_z:
        return False
    if bricks[bid2]['x_min'] > bricks[bid1]['x_max'] or bricks[bid2]['x_max'] < bricks[bid1]['x_min']:
        return False
    if bricks[bid2]['y_min'] > bricks[bid1]['y_max'] or bricks[bid2]['y_max'] < bricks[bid1]['y_min']:
        return False
    return True


def fill_support_maps():
    global supports_map, supported_by_map, bricks
    supports_map = dict()
    supported_by_map = dict()

    for bid1 in bricks.keys():
        for bid2 in bricks.keys():
            if supports(bid1, bid2):
                if bid1 in supports_map:
                    supports_map[bid1].add(bid2)
                else:
                    supports_map[bid1] = {bid2}

                if bid2 in supported_by_map:
                    supported_by_map[bid2].add(bid1)
                else:
                    supported_by_map[bid2] = {bid1}


def drop_brick(bid):
    global supports_map, supported_by_map, bricks_by_z_max, bricks_by_z_min
    assert not is_supported(bid)
    if bid in supports_map:
        for b in supports_map[bid]:
            supported_by_map[b].remove(bid)
        del supports_map[bid]
    z_min = bricks[bid]['z_min']
    z_max = bricks[bid]['z_max']
    bricks_by_z_max[z_max].remove(bid)
    bricks_by_z_min[z_min].remove(bid)
    bricks[bid]['z_min'] -= 1
    bricks[bid]['z_max'] -= 1
    z_min_new = z_min-1
    if z_min_new in bricks_by_z_min:
        bricks_by_z_min[z_min_new].add(bid)
    else:
        bricks_by_z_min[z_min_new] = {bid}
    z_max_new = z_max-1
    if z_max_new in bricks_by_z_max:
        bricks_by_z_max[z_max_new].add(bid)
    else:
        bricks_by_z_max[z_max_new] = {bid}

    bricks_by_z_max[z_max-1].add(bid)


def is_supported(bid):
    return bid in supported_by_map and len(supported_by_map[bid]) > 0


def pt1():
    global supports_map, supported_by_map
    for i, line in enumerate(lines):
        brick = dict()
        x_min, y_min, z_min = tuple(map(int, line.split("~")[0].split(',')))
        x_max, y_max, z_max = tuple(map(int, line.split("~")[1].split(',')))
        assert x_max >= x_min
        assert y_max >= y_min
        brick['x_min'] = x_min
        brick['x_max'] = x_max
        brick['y_min'] = y_min
        brick['y_max'] = y_max
        brick['z_min'] = z_min
        brick['z_max'] = z_max
        brick['id'] = i
        bricks[i] = brick
        if z_min in bricks_by_z_min:
            bricks_by_z_min[z_min].add(i)
        else:
            bricks_by_z_min[z_min] = {i}
        if z_max in bricks_by_z_max:
            bricks_by_z_max[z_max].add(i)
        else:
            bricks_by_z_max[z_max] = {i}

    fill_support_maps()
    debug(supported_by_map)
    debug(supports_map)

    for z in [z for z in sorted(bricks_by_z_min.keys()) if z != 1]:
        bids = dc(bricks_by_z_min[z])
        for bid in bids:
            support_layer = z-1
            while not is_supported(bid):
                drop_brick(bid)
                support_layer -= 1
                if support_layer == 0:
                    break
                if support_layer in bricks_by_z_max:
                    for bid2 in bricks_by_z_max[support_layer]:
                        if supports(bid2, bid):
                            if bid in supported_by_map:
                                supported_by_map[bid].add(bid2)
                            else:
                                supported_by_map[bid] = {bid2}

    fill_support_maps()
    debug(supported_by_map)
    debug(supports_map)
    removables = set()
    for bid in bricks.keys():
        if bid not in supports_map:
            removables.add(bid)
            continue
        might_be_removed = True
        for bid2 in supports_map[bid]:
            if len(supported_by_map[bid2]) < 2:
                might_be_removed = False
                break
        if might_be_removed:
            removables.add(bid)
    debug(removables)
    info(f"number of removables: {len(removables)}")

    total = 0
    for current_bid in set(bricks.keys()).difference(removables):
        new_supported_by = dc(supported_by_map)
        new_supports = dc(supports_map)
        would_fall = set()
        dq = deque([current_bid])
        while dq:
            bid = dq.popleft()
            if bid not in supports_map:
                continue
            for new_bid in new_supports[bid]:
                new_supported_by[new_bid].remove(bid)
                if len(new_supported_by[new_bid]) == 0:
                    would_fall.add(new_bid)
                    dq.append(new_bid)
            del new_supports[bid]
        debug(f"number of falling bricks for {current_bid}: {len(would_fall)}")
        total += len(would_fall)
    info(f"total chain length: {total}")


if __name__ == '__main__':
    pt1()

