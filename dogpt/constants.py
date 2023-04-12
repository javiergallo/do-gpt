import inspect
import time

ROUTINES_SPEC = {
    "print": {
        "short_desc": (
            "Prints objects to the text stream file, separated by sep and "
            "followed by end."
        ),
        "callable": print,
        "signature": "(*objects, sep=' ', end='\\n', file=None, flush=False)",
    },
    "range": {
        "short_desc": "Returns a range.",
        "callable": range,
        "signature": "(start, stop, step=1)",
    },
    "sleep": {
        "short_desc": (
            "Suspends execution of the calling thread for the given number of "
            "seconds."
        ),
        "callable": time.sleep,
        "signature": "(secs)",
    },
    "time": {
        "short_desc": (
            "Returns the time in seconds since the epoch as a floating point "
            "number."
        ),
        "callable": time.time,
        "signature": "()",
    },
}

ROUTINE_MENU_ITEM_PATTERN = "* {name}{signature}  # {short_desc}"

ROUTINE_MENU = "\n".join(
    ROUTINE_MENU_ITEM_PATTERN.format(
        name=routine_alias,
        signature=routine_spec.get("signature")
        or inspect.signature(routine_spec["callable"]),
        short_desc=routine_spec["short_desc"],
    )
    for routine_alias, routine_spec in ROUTINES_SPEC.items()
)

SUPERPROMT_HEADER = """
Suppose we have the following Python routines:

{routine_menu}
""".format(
    routine_menu=ROUTINE_MENU
)

SUPERPROMT_BODY_PATTERN = """
Translate the following instructions into a Python program:

{prompt}

You might want to use the previously defined routines.
Do NOT define procedures nor functions.
Avoid imports and builtin procedures or functions.
Output just the code, and nothing else.
"""

SUPERPROMT_PATTERN = SUPERPROMT_HEADER + SUPERPROMT_BODY_PATTERN
