def dex_runtime(user_input: str):

    # TALNIR REASONING SPACE
    paths = [
        {"name": "direct", "description": "Answer directly", "confidence": 0.7},
        {"name": "decompose", "description": "Break into structured steps", "confidence": 0.85},
        {"name": "intent", "description": "Infer deeper meaning", "confidence": 0.75}
    ]

    # SELECT BEST PATH
    selected = max(paths, key=lambda p: p["confidence"])

    # EXECUTION LAYER
    if selected["name"] == "direct":
        output = f"Dex → {user_input}"

    elif selected["name"] == "decompose":
        output = (
            f"Dex decomposition:\n"
            f"- Input: {user_input}\n"
            f"- Step 1: analyze components\n"
            f"- Step 2: map relationships\n"
            f"- Step 3: construct response"
        )

    else:
        output = f"Dex intent model → interpreting: {user_input}"

    # TALNIR TRACE OUTPUT (CRITICAL CONTRACT)
    return {
        "input": user_input,
        "output": output,
        "selected_path": selected["name"],
        "reasoning_trace": selected["description"],
        "reasoning_paths": paths
    }
