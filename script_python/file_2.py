import re

INPUT_PATH = r"path to .txt with explanation of state machine logic"
OUTPUT_PATH = r" main.py, path of ingescape agent"

def parse_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    states = re.findall(r"🔵 ([A-Za-z_]+)", content)

    transitions = []
    for line in content.splitlines():
        match = re.match(r"🔁 ([A-Za-z_]+) → ([A-Za-z_]+)(?: con trigger '([^']+)')?", line)
        if match:
            src, dst, trigger = match.groups()
            if trigger:
                transitions.append({
                    'trigger': trigger.replace("ev_", "ev"),  # es: ev_Red -> evRed
                    'source': src,
                    'dest': dst
                })

    return states, transitions

def generate_main_py(states, transitions, initial_state="Green", class_name="TrafficLight"):
    states_block = "[" + ", ".join(f"'{s}'" for s in states) + "]"

    transitions_block = "[\n" + ",\n".join(
        f"    {{'trigger': '{t['trigger']}', 'source': '{t['source']}', 'dest': '{t['dest']}'}}"
        for t in transitions
    ) + "\n]"

    return f"""#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

import sys
import ingescape as igs
from transitions import Machine

# ------------------------
# Traffic light state machine
# ------------------------

class {class_name}:
    pass

states = {states_block}

transitions = {transitions_block}

traffic_light = {class_name}()
machine = Machine(model=traffic_light, states=states, transitions=transitions, initial='{initial_state}')

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
        igs.debug(f"[In] motion_sensor = {{value}}")
        try:
            if value:
                traffic_light.evRed()
            else:
                traffic_light.evGreen()
            igs.debug(f"[FSM] New state: {{traffic_light.state}}")
        except Exception as e:
            igs.error(f"[FSM] Transition error: {{e}}")
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
            print(f" {{device}}")
        exit(0)

    igs.agent_set_name(sys.argv[1])
    igs.definition_set_class("prova_2")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {{igs.version()}} (protocol v{{igs.protocol()}})")

    igs.input_create("motion_sensor", igs.BOOL_T, None)
    igs.observe_input("motion_sensor", input_callback, None)

    igs.output_create("green", igs.INTEGER_T, None)
    igs.output_create("red", igs.INTEGER_T, None)

    update_outputs()

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()
    igs.stop()
"""

def main():
    states, transitions = parse_txt(INPUT_PATH)
    code = generate_main_py(states, transitions)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"[✓] main.py generato correttamente in:\n{OUTPUT_PATH}")

if __name__ == "__main__":
    main()