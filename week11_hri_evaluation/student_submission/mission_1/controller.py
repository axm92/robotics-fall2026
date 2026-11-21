"""Complete decide() using the transition requirements in the Lab 10 guide."""


def decide(state, event):
    # --- Read the current phase, incoming event, and target ---
    phase = state["phase"]
    kind = event["kind"]
    target = event["target"]
    named = target in ("red", "blue")

    # --- Interrupt: cancellation has priority over every other rule ---
    if kind == "CANCEL":
        if phase not in ("IDLE", "COMPLETE", "CANCELLED"):
            return "cancel"
        return "hold"

    # --- Select: a new request resolves which cup the person wants ---
    if kind == "REQUEST" and phase in ("IDLE", "CLARIFY", "CONFIRM", "RECOVERY", "CANCELLED"):
        return "select" if named else "clarify"

    # --- Select: a correction naming a cup replaces the active task ---
    if kind == "CORRECT" and named:
        return "select"

    # --- Confirm: only valid while waiting for confirmation ---
    if kind == "CONFIRM" and phase == "CONFIRM":
        return "begin"

    # --- Advance: keep moving toward the station while executing ---
    if kind == "TICK" and phase == "EXECUTING":
        return "advance"

    # --- Release: needs the WAIT_READY phase AND the READY event ---
    if kind == "READY" and phase == "WAIT_READY":
        return "release"

    # --- Timeout: the offer expired while waiting for readiness ---
    if kind == "TIMEOUT" and phase == "WAIT_READY":
        return "timeout"

    # --- Fallback: no valid transition, so hold ---
    return "hold"