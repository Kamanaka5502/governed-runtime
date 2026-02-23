def process(state):

    state["eos"] = True
    state["lifecycle"] = "COMPLETE"

    print({
        "layer": 101,
        "EOS": True,
        "status": "RUNTIME_CLOSED"
    })

    return state
