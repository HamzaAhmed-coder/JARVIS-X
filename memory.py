import json
import os


# =========================================
# PROJECT DATA DIRECTORY
# =========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

os.makedirs(
    DATA_DIR,
    exist_ok=True
)


MEMORY_FILE = os.path.join(
    DATA_DIR,
    "memory.json"
)


# =========================================
# LOAD MEMORY
# =========================================

def load_memory():

    if not os.path.exists(MEMORY_FILE):

        return {}

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as e:

        print(
            "MEMORY LOAD ERROR:",
            e
        )

        return {}


# =========================================
# SAVE MEMORY
# =========================================

def save_memory(memory):

    try:

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                memory,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except Exception as e:

        print(
            "MEMORY SAVE ERROR:",
            e
        )

        return False


# =========================================
# REMEMBER
# =========================================

def remember(key, value):

    memory = load_memory()

    memory[
        key.lower().strip()
    ] = value.strip()

    if save_memory(memory):

        return (
            f"I'll remember that "
            f"{key} is {value}."
        )

    return (
        "I couldn't save that "
        "to memory."
    )


# =========================================
# RECALL
# =========================================

def recall(key):

    memory = load_memory()

    key = key.lower().strip()

    if key in memory:

        return (
            f"{key.title()} is "
            f"{memory[key]}."
        )

    return (
        f"I don't have anything "
        f"saved about {key}."
    )


# =========================================
# SHOW ALL MEMORY
# =========================================

def get_all_memory():

    memory = load_memory()

    if not memory:

        return (
            "My memory is currently empty."
        )

    lines = []

    for key, value in memory.items():

        lines.append(
            f"{key}: {value}"
        )

    return "\n".join(lines)


# =========================================
# FORGET
# =========================================

def forget(key):

    memory = load_memory()

    key = key.lower().strip()

    if key not in memory:

        return (
            f"I don't have anything "
            f"saved about {key}."
        )

    del memory[key]

    save_memory(memory)

    return (
        f"I've forgotten {key}."
    )