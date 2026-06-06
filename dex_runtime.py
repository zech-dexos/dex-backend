from talnir import translate, decompose
try:
    from model_router import route, route_info
    ROUTER_ACTIVE = True
except ImportError:
    ROUTER_ACTIVE = False

try:
    from sigil import SigilMemory
    _memory = SigilMemory()
    SIGIL_ACTIVE = True
except ImportError:
    SIGIL_ACTIVE = False
    _memory = None

try:
    from pathlib import Path
    Path("/app/dexos_state").mkdir(exist_ok=True)
    from dexos import DexOS
    _dexos = DexOS()
    _dexos.initialize()
    DEXOS_ACTIVE = True
except Exception as e:
    DEXOS_ACTIVE = False
    _dexos = None

def dex_runtime(user_input: str) -> dict:
    result = decompose(user_input)
    signal = result["signal"]

    sigil_ids = []
    if SIGIL_ACTIVE and _memory:
        context = signal.domain or "CTX:ALL"
        active = _memory.activate_for_context(context)
        active = _memory.resolve_conflicts(active, context)
        sigil_ids = [s.id for s in active]

    routing = route_info(signal) if ROUTER_ACTIVE else {"model": "dex:latest", "reason": "router unavailable"}

    if DEXOS_ACTIVE and _dexos:
        governance = _dexos.process(user_input)
        if governance.get("status") == "flagged":
            return {
                "input":        user_input,
                "intent":       "blocked",
                "domain":       "security",
                "modifiers":    [],
                "tools":        [],
                "context":      {},
                "branches":     [],
                "sigil_ids":    [],
                "model":        "dexos",
                "route_reason": governance.get("drift_type", "flagged"),
                "governed":     True,
                "flagged":      True,
                "response":     governance.get("response", "")
            }

    return {
        "input":        user_input,
        "intent":       signal.intent,
        "domain":       signal.domain,
        "modifiers":    signal.modifiers,
        "tools":        signal.tools,
        "context":      result["context"],
        "branches":     result["branches"],
        "sigil_ids":    sigil_ids,
        "model":        routing["model"],
        "route_reason": routing["reason"],
        "governed":     DEXOS_ACTIVE,
        "flagged":      False
    }
