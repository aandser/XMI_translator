def estrai_logica_macchina_stati(xmi_path, output_txt, statemachine_name):
    with open(xmi_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    inside_statemachine = False
    inside_region = False
    statemachine_id = ""
    pseudostates = {}
    states = {}
    transitions = []
    triggers_raw = {}
    signal_events = {}
    signals = {}

    current_transition = None
    found = False

    # 🔁 PRIMO PASSAGGIO: raccogliamo tutto
    for i, line in enumerate(lines):
        stripped = line.strip()

        # 📌 Individua la macchina a stati cercata
        if f"<packagedElement xmi:type='uml:StateMachine'" in stripped and f"name='{statemachine_name}'" in stripped:
            inside_statemachine = True
            found = True
            statemachine_id = get_attribute(stripped, "xmi:id")
            continue

        # Dentro macchina a stati
        if inside_statemachine:

            # Inizia <region>
            if "<region" in stripped and "xmi:type='uml:Region'" in stripped:
                inside_region = True
                continue

            # Finisce </region>
            if "</region>" in stripped:
                inside_region = False
                continue

            if inside_region:
                # pseudostate
                if "xmi:type='uml:Pseudostate'" in stripped:
                    pid = get_attribute(stripped, "xmi:id")
                    pseudostates[pid] = "Initial"
                # state
                elif "xmi:type='uml:State'" in stripped:
                    sid = get_attribute(stripped, "xmi:id")
                    name = get_attribute(stripped, "name")
                    states[sid] = name
                # transition
                elif "xmi:type='uml:Transition'" in stripped:
                    current_transition = {
                        "id": get_attribute(stripped, "xmi:id"),
                        "source": get_attribute(stripped, "source"),
                        "target": get_attribute(stripped, "target"),
                        "trigger": None
                    }
                    transitions.append(current_transition)
                # trigger
                elif "xmi:type='uml:Trigger'" in stripped:
                    trig_id = get_attribute(stripped, "xmi:id")
                    event = get_attribute(stripped, "event")
                    triggers_raw[trig_id] = event
                    if current_transition:
                        current_transition["trigger"] = trig_id

        # 📦 Raccolta globale degli elementi esterni
        if "<packagedElement xmi:type='uml:Signal'" in stripped:
            sig_id = get_attribute(stripped, "xmi:id")
            sig_name = get_attribute(stripped, "name")
            signals[sig_id] = sig_name

        elif "<packagedElement xmi:type='uml:SignalEvent'" in stripped:
            se_id = get_attribute(stripped, "xmi:id")
            signal_ref = get_attribute(stripped, "signal")
            signal_events[se_id] = signal_ref

        elif "</packagedElement>" in stripped and inside_statemachine:
            inside_statemachine = False

    # 🔁 Mappa finale Trigger ID → Nome segnale
    trigger_names = {}
    for trig_id, event_id in triggers_raw.items():
        signal_id = signal_events.get(event_id)
        trigger_names[trig_id] = signals.get(signal_id, "UnknownSignal")

    # 📝 Output TXT
    with open(output_txt, 'w', encoding='utf-8') as out:
        if not found:
            out.write(f"❌ Nessuna macchina a stati '{statemachine_name}' trovata.\n")
            return

        out.write(f"📘 State Machine: {statemachine_name}\n\n")

        out.write("🔹 Stati:\n")
        for pid in pseudostates:
            out.write(f"🟠 Pseudostato iniziale (ID: {pid})\n")
        for sid, name in states.items():
            out.write(f"🔵 {name} (ID: {sid})\n")

        out.write("\n🔁 Transizioni:\n")
        for t in transitions:
            source_id = t['source']
            target_id = t['target']
            source_name = pseudostates.get(source_id) or states.get(source_id, f"Unknown({source_id})")
            target_name = pseudostates.get(target_id) or states.get(target_id, f"Unknown({target_id})")
            trigger_id = t.get("trigger")
            trigger_label = trigger_names.get(trigger_id)

            if trigger_label:
                out.write(f"🔁 {source_name} → {target_name} con trigger '{trigger_label}'\n")
            else:
                out.write(f"🔁 {source_name} → {target_name} (senza trigger)\n")

    print(f"✅ Logica macchina a stati '{statemachine_name}' salvata in: {output_txt}")

def get_attribute(line, attr_name):
    import re
    match = re.search(fr"{attr_name}='([^']+)'", line)
    return match.group(1) if match else None

# ▶️ ESEMPIO USO
if __name__ == "__main__":
    xmi_path = r"path to xmi"
    output_txt = r"path to logic explanation of state machine .txt"
    statemachine_name = "Traffic_light"

    estrai_logica_macchina_stati(xmi_path, output_txt, statemachine_name)