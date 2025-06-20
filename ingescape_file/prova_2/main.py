#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

import sys
import ingescape as igs
from transitions import Machine

# ------------------------
# Traffic light state machine
# ------------------------

class TrafficLight:
    pass

states = ['Green', 'Red']

transitions = [
    {'trigger': 'evRed', 'source': 'Green', 'dest': 'Red'},
    {'trigger': 'evGreen', 'source': 'Red', 'dest': 'Green'}
]

traffic_light = TrafficLight()
machine = Machine(model=traffic_light, states=states, transitions=transitions, initial='Green')

def update_outputs():
    if traffic_light.state == "Green":
        igs.output_set_int("green", 1)
        igs.output_set_int("red", 0)
    elif traffic_light.state == "Red":
        igs.output_set_int("green", 0)
        igs.output_set_int("red", 1)

# ------------------------
# Ingescape input callback
# ------------------------

def input_callback(io_type, name, value_type, value, my_data):
    if name == "motion_sensor":
        igs.debug(f"[In] motion_sensor = {value}")
        try:
            if value:
                traffic_light.evRed()
            else:
                traffic_light.evGreen()
            igs.debug(f"[FSM] New state: {traffic_light.state}")
        except Exception as e:
            igs.error(f"[FSM] Transition error: {e}")
        update_outputs()

# ------------------------
# Main
# ------------------------

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python3 main.py agent_name network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)

    igs.agent_set_name(sys.argv[1])
    igs.definition_set_class("prova_2")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    igs.input_create("motion_sensor", igs.BOOL_T, None)
    igs.observe_input("motion_sensor", input_callback, None)

    igs.output_create("green", igs.INTEGER_T, None)
    igs.output_create("red", igs.INTEGER_T, None)

    update_outputs()

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()
    igs.stop()
