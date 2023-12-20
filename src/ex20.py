import logging
from logging import info, debug
from math import lcm

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex20.txt")
lines = [file.replace("\n", "") for file in in_file.readlines()]

connections = dict()
conjunctions = dict()
flipflops = dict()
highs = 0
lows = 0
low_rx_signals_per_click = 0
factors = dict()


def run_steps(_receiver, _sender, _is_high_signal, it):
    global conjunctions, connections, flipflops, highs, lows, factors
    steps = [(_receiver, _sender, _is_high_signal)]
    while steps:
        receiver, sender, is_high_signal = steps.pop(0)
        if receiver == 'dg' and is_high_signal and it:
            if sender not in factors:
                factors[sender] = it
                if len(factors.keys()) == 4:
                    info(lcm(*factors.values()))
                    break
                debug(factors)
        if is_high_signal:
            sig = '-high'
            highs += 1
        else:
            sig = '-low'
            lows += 1
        debug(f"{sender} {sig}-> {receiver}")
        send_signal = True
        if receiver in conjunctions:
            conjunctions[receiver][sender] = is_high_signal
            new_signal_type = not all([v for k, v in conjunctions[receiver].items()])
        elif receiver in flipflops:
            if is_high_signal:
                send_signal = False
            else:
                flipflops[receiver] = not flipflops[receiver]
            new_signal_type = flipflops[receiver]
        elif receiver == 'broadcaster':
            new_signal_type = is_high_signal
        else:
            new_signal_type = False
            ValueError("do_step: receiver unknown type")

        if send_signal and receiver in connections:
            for new_receiver in connections[receiver]:
                steps.append((new_receiver, receiver, new_signal_type))


def solution():
    global conjunctions, connections, flipflops, low_rx_signals_per_click
    for line in lines:
        sender, receivers_txt = line.split(" -> ")
        if sender[0] == '%':
            sender = sender[1:]
            flipflops[sender] = False
        elif sender[0] == '&':
            sender = sender[1:]
            conjunctions[sender] = {}
        elif sender == 'broadcaster':
            pass
        else:
            ValueError("not a flipflop, conjunction or broadcaster!")
        connections[sender] = receivers_txt.split(', ')
    for s, rs in connections.items():
        for r in rs:
            if r in conjunctions.keys():
                conjunctions[r][s] = False
    debug(conjunctions)
    debug(conjunctions['dg'])

    it = 0
    while True:
        it += 1
        run_steps('broadcaster', 'button', False, it)
        if it == 1000:
            info(highs*lows)
        if len(factors) > 3:
            break


if __name__ == '__main__':
    solution()
