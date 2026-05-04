from talnir import translate
from engine import decompose


def dex_runtime(user_input: str) -> dict:
    result = decompose(user_input)
    signal = result["signal"]

    return {
        "input": user_input,
        "intent": signal.intent,
        "domain": signal.domain,
        "modifiers": signal.modifiers,
        "tools": signal.tools,
        "context": result["context"],
        "branches": result["branches"],
    }
