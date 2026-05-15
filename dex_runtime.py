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

    return {
        "input":    user_input,
        "intent":   signal.intent,
        "domain":   signal.domain,
        "modifiers":signal.modifiers,
        "tools":    signal.tools,
        "context":  result["context"],
        "branches": result["branches"],
        "sigil_ids":sigil_ids,
        "model":    routing["model"],
        "route_reason": routing["reason"],
    }
