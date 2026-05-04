import sys
import os

# Make reasonflow importable from the parent reasonflow repo
# Assumes dex-backend is cloned alongside reasonflow:
#   ~/reasonflow/reasonflow/talnir.py
#   ~/reasonflow/reasonflow/engine.py
REASONFLOW_PATH = os.path.expanduser("~/reasonflow")
if REASONFLOW_PATH not in sys.path:
    sys.path.insert(0, REASONFLOW_PATH)

from reasonflow.talnir import translate
from reasonflow.engine import decompose


def dex_runtime(user_input: str) -> dict:
    """
    Real ReasonFlow pipeline:
    NL input → Talnir signal → engine decomposition → structured output
    """
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
