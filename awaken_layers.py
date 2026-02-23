import glob
import os

template = """
def process(state):

    state["pressure"] *= 0.9995
    state["coherence"] = min(1.0, state.get("coherence",0)+0.0002)

    print({{
        "layer": "{layer}",
        "status": "active"
    }})

    return state
"""

for f in glob.glob("layer*.py"):
    with open(f, "r") as file:
        content = file.read()

    if "def process" not in content:
        name = os.path.splitext(os.path.basename(f))[0]
        layer_id = name.replace("layer","")

        with open(f, "a") as file:
            file.write(template.format(layer=layer_id))

        print(f"Activated: {f}")

