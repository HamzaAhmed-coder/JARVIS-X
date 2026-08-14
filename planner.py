print("LOADED PLANNER:", __file__)
from app.llm import ask_llm
from app.tools.registry import get_tool
from app.memory.contacts import remember_contact, get_contact
from app.nlp import normalize
from app.memory.pending_action import (
    set_pending,
    get_pending,
    clear_pending,
)

import re

SYSTEM_PROMPT = """
You are JARVIS.
Answer normally unless the user wants an action.
"""
def run_agent(user_message):

    print("RUN_AGENT EXECUTED")
    print("=" * 40)
    print("User:", user_message)

    user_message = normalize(user_message)
    print("AFTER NORMALIZE:", repr(user_message))
    pending = get_pending()

    # ---------------- Pending Action ----------------
    if pending:

        if pending["action"] == "whatsapp":

            contact = pending["data"]["contact"]

            message = user_message

            clear_pending()

            saved = get_contact(contact)

            if saved:
                contact = saved

            return get_tool("send_whatsapp")(
                contact,
                message,
            )

    # ---------------- Multi Command ----------------
    result = handle_multi(user_message)
    if result:
        return result

    # WhatsApp
    result = handle_whatsapp(user_message)
    if result:
        return result
    
    whatsapp_result = handle_whatsapp(user_message)

    if whatsapp_result:
        return whatsapp_result

    # Gmail
    result = handle_gmail(user_message)
    if result:
        return result

    # Calendar
    result = handle_calendar(user_message)
    if result:
        return result

    # Google
    result = handle_google(user_message)
    if result:
        return result
    
    memory_result = handle_memory(
    user_message
)
    if memory_result:
        return memory_result
    # ---------------- Files ----------------

    result = handle_files(user_message)
    if result:
        return result
    # Memory
    result = handle_memory(user_message)
    if result:
        return result
    # AI Memory
    result = handle_ai_memory(user_message)
    if result:
        return result
    # Open Commands
    result = handle_open(user_message)
    if result:
        return result

    # Clipboard
    result = handle_clipboard(user_message)
    if result:
        return result

    # Windows
    result = handle_windows(user_message)
    if result:
        return result

    print(">>> Sending to LLM <<<")

    messages = [
        {
            "role":"system",
            "content":SYSTEM_PROMPT
        },
        {
            "role":"user",
            "content":user_message
        }
    ]

    return ask_llm(messages)
def handle_multi(user_message):

    commands = re.split(
        r"\s+(?:and|then)\s+",
        user_message,
        flags=re.IGNORECASE
    )

    if len(commands) <= 1:
        return None

    output = []

    for cmd in commands:

        cmd = cmd.strip()

        if cmd:

            output.append(run_agent(cmd))

    return "\n".join(output)
def handle_memory(user_message):

    # Remember Contact
    match = re.search(
        r"remember (.+?) as (.+)",
        user_message,
        re.IGNORECASE,
    )

    if match:

        real_name = match.group(1).strip()
        alias = match.group(2).strip()

        return remember_contact(alias, real_name)

    return None

def handle_ai_memory(user_message):

    msg = user_message.lower()

    # Remember
    match = re.search(
        r"remember (?:my )?(.+?) is (.+)",
        user_message,
        re.IGNORECASE,
    )

    if match:

        key = match.group(1).strip()
        value = match.group(2).strip()

        return get_tool("remember")(key, value)

    # Recall
    match = re.search(
        r"what is my (.+)",
        user_message,
        re.IGNORECASE,
    )

    if match:

        key = match.group(1).strip()

        value = get_tool("recall")(key)

        if value:
            return f"Your {key} is {value}."

        return f"I don't know your {key} yet."

    # Recall All
    if (
        "what do you know about me" in msg
        or "tell me about me" in msg
    ):

        memory = get_tool("recall_all")()

        if not memory:
            return "I don't know anything about you yet."

        text = "Here's what I know:\n\n"

        for key, value in memory.items():
            text += f"{key}: {value}\n"

        return text

    return None

def handle_whatsapp(user_message):

    msg = user_message.lower()

    # Open WhatsApp
    if (
        "open whatsapp" in msg
        or "whatsapp kholo" in msg
    ):
        return get_tool("whatsapp_desktop")()

    patterns = [

        r"send whatsapp message to (.+?) saying (.+)",

        r"send message to (.+?) on whatsapp saying (.+)",

        r"message (.+?) on whatsapp saying (.+)",

        r"send (.+?) to (.+?) on whatsapp",

        r"(.+?) ko whatsapp par (.+?) bhejo",

        r"(.+?) ko message bhejo (.+)",

        r"(.+?) ko (.+?) bhejo on whatsapp",

        r"message (.+?) on whatsapp",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            user_message,
            re.IGNORECASE,
        )

        if not match:
            continue

        # -------- Conversation Mode --------
        if pattern == r"message (.+?) on whatsapp":

            contact = match.group(1).strip()

            saved = get_contact(contact)
            if saved:
                contact = saved

            set_pending(
                "whatsapp",
                {
                    "contact": contact,
                },
            )

            return f"What message should I send to {contact}?"

        # -------- send MESSAGE to CONTACT --------
        elif pattern == r"send (.+?) to (.+?) on whatsapp":

            message = match.group(1).strip()
            contact = match.group(2).strip()

        # -------- All Other Patterns --------
        else:

            contact = match.group(1).strip()
            message = match.group(2).strip()

        saved = get_contact(contact)

        if saved:
            contact = saved

        return get_tool("send_whatsapp")(
            contact,
            message,
        )

    return None

def handle_calendar(user_message):

    match = re.search(
        r"(?:create|schedule)\s+(.*?)\s*meeting\s+at\s+(\d{1,2})\s*(a\.?m\.?|p\.?m\.?|am|pm)?(?:\s+(today|tomorrow))?",
        user_message,
        re.IGNORECASE,
    )

    if not match:
        return None

    title = match.group(1).strip()

    if title.lower() in ("", "a", "an"):
        title = "Meeting"

    hour = int(match.group(2))
    ampm = match.group(3)
    day = match.group(4)

    if ampm:
        ampm = ampm.lower().replace(".", "")

        if ampm == "pm" and hour != 12:
            hour += 12
        elif ampm == "am" and hour == 12:
            hour = 0

    days = 1 if day and day.lower() == "tomorrow" else 0

    print("CALLING CALENDAR")
    print(title, hour, days)

    return get_tool("calendar_create")(
        title,
        hour,
        0,
        days,
    )

def handle_gmail(user_message):

    msg = user_message.lower()

    # Read Emails
    if (
        "read my emails" in msg
        or "read latest emails" in msg
        or "show my emails" in msg
        or "check my emails" in msg
        or "email dikhao" in msg
    ):
        return get_tool("read_emails")()

    # Send Email
    match = re.search(
        r"send email to (.+?) saying (.+)",
        user_message,
        re.IGNORECASE,
    )

    if match:

        email = match.group(1).strip()
        body = match.group(2).strip()

        return get_tool("send_email")(
            email,
            "Message from JARVIS",
            body,
        )

    return None


def handle_google(user_message):

    msg = user_message.lower()

    # Google Search
    if msg.startswith("search ") or msg.startswith("google "):

        query = (
            user_message
            .replace("Search", "")
            .replace("search", "")
            .replace("Google", "")
            .replace("google", "")
            .strip()
        )

        return get_tool("google_search")(query)

    # Google News
    if (
        "latest news about" in msg
        or "news about" in msg
    ):

        query = (
            msg.replace("latest news about", "")
               .replace("news about", "")
               .strip()
        )

        return get_tool("google_news")(query)

    return None


def handle_files(user_message):
    print(">>> HANDLE_FILES CALLED <<<")
    msg = user_message.lower()
    print("DEBUG FILES:", repr(user_message))
    # ---------- Create Folder ----------
    match = re.search(
        r"create folder (.+?) (?:on|in) (desktop|documents|downloads|pictures)",
        msg,
    )

    if match:
        return get_tool("create_folder")(
            match.group(1).strip(),
            match.group(2).strip(),
        )

    match = re.search(r"create folder (.+)", msg)

    if match:
        return get_tool("create_folder")(
            match.group(1).strip()
        )

    # ---------- Create File ----------
    match = re.search(
        r"create file (.+?) (?:on|in) (desktop|documents|downloads|pictures)",
        msg,
    )

    if match:
        return get_tool("create_file")(
            match.group(1).strip(),
            match.group(2).strip(),
        )

    match = re.search(r"create file (.+)", msg)

    if match:
        return get_tool("create_file")(
            match.group(1).strip()
        )

    # ---------- Delete File ----------
    match = re.search(
        r"delete file (.+?) (?:on|in) (desktop|documents|downloads|pictures)",
        msg,
    )

    if match:
        return get_tool("delete_file")(
            match.group(1).strip(),
            match.group(2).strip(),
        )

    # ---------- Delete Folder ----------
    match = re.search(
        r"delete folder (.+?) (?:on|in) (desktop|documents|downloads|pictures)",
        msg,
    )

    if match:
        return get_tool("delete_folder")(
            match.group(1).strip(),
            match.group(2).strip(),
        )

    # ---------- Find File ----------
    match = re.search(
        r"(?:find|search)\s+(.+)",
        user_message,
        re.IGNORECASE,
    )

    if match:
        return get_tool("search_file")(
            match.group(1).strip()
        )

    # ---------- Open File ----------
    match = re.search(
        r"open file (.+)",
        user_message,
        re.IGNORECASE,
    )

    if match:
        return get_tool("open_file")(
            match.group(1).strip()
        )

    return None

def handle_open(user_message):

    msg = user_message.lower()

   # Websites

    if "open google" in msg:
        return get_tool("google_home")()

    # YouTube Search / Play
    match = re.search(
    r"(?:play|search)\s+(.+?)\s+(?:on|in)\s+youtube",
    user_message,
    re.IGNORECASE,
)

    if match:
        query = match.group(1).strip()
        return get_tool("youtube")(query)

    # Open YouTube Home
    if "open youtube" in msg:
        return get_tool("youtube_home")()

    if "open instagram" in msg:
        return get_tool("instagram_home")()

    if "open github" in msg:
        return get_tool("github")()

    if "open linkedin" in msg:
        return get_tool("linkedin")()

    if "open gmail" in msg:
        return get_tool("gmail")()

    # Desktop folders
    if "open desktop" in msg:
        return get_tool("desktop")()

    if "open downloads" in msg:
        return get_tool("downloads")()

    if "open documents" in msg:
        return get_tool("documents")()

    if "open pictures" in msg:
        return get_tool("pictures")()

    if "open explorer" in msg or "file explorer" in msg:
        return get_tool("explorer")()

    if "open cmd" in msg or "command prompt" in msg:
        return get_tool("cmd")()

    if "open paint" in msg:
        return get_tool("paint")()

    if "open vscode" in msg or "open vs code" in msg:
        return get_tool("vscode")()

    if "calculator" in msg:
        return get_tool("calculator")()

    if "notepad" in msg:
        return get_tool("notepad")()

    # Generic Open App
    match = re.search(r"open (.+)", msg)

    if match:

        app = match.group(1).strip()

        tool = get_tool("open_app")

        if tool:

            result = tool(app)

            if (
                "don't know" not in result.lower()
                and "not installed" not in result.lower()
            ):
                return result

    return None

def handle_clipboard(user_message):

    msg = user_message.lower()

    if msg.startswith("copy "):

        text = user_message[5:]

        return get_tool("copy")(text)

    if (
        "read clipboard" in msg
        or "clipboard" == msg
    ):
        return get_tool("clipboard")()

    return None

def handle_whatsapp(user_message):

    text = user_message.lower().strip()
    # -----------------------------------------
# OPEN WHATSAPP
# -----------------------------------------

    if (
    "open whatsapp" in text
    or "whatsapp kholo" in text
    ):

        return get_tool(
        "whatsapp_desktop"
        )()

    patterns = [
        r"send whatsapp message to (.+?) saying (.+)",
        r"send a whatsapp message to (.+?) saying (.+)",
        r"whatsapp (.+?) saying (.+)",
        r"message (.+?) on whatsapp saying (.+)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            contact = match.group(1).strip()

            message = match.group(2).strip()

            print(
                "WHATSAPP CONTACT:",
                contact
            )

            print(
                "WHATSAPP MESSAGE:",
                message
            )

            tool = get_tool(
                "send_whatsapp"
            )

            if not tool:

                return (
                    "WhatsApp tool is not registered."
                )

            return tool(
                contact,
                message
            )

    return None

# =========================================
# MEMORY HANDLER
# =========================================

def handle_memory(user_message):

    text = user_message.lower().strip()


    # -----------------------------------------
    # REMEMBER
    # -----------------------------------------

    patterns = [

        r"remember that (.+?) is (.+)",

        r"remember (.+?) is (.+)",

        r"save that (.+?) is (.+)",

    ]


    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            key = match.group(1).strip()

            value = match.group(2).strip()


            tool = get_tool(
                "remember"
            )


            if not tool:

                return (
                    "Memory tool is not registered."
                )


            return tool(
                key,
                value
            )


    # -----------------------------------------
    # RECALL
    # -----------------------------------------

    recall_patterns = [

        r"what is my (.+)",

        r"what's my (.+)",

        r"do you remember my (.+)",

        r"what do you remember about (.+)",

    ]


    for pattern in recall_patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            key = match.group(1).strip()


            tool = get_tool(
                "recall"
            )


            if not tool:

                return (
                    "Memory tool is not registered."
                )


            return tool(
                key
            )


    # -----------------------------------------
    # SHOW ALL MEMORY
    # -----------------------------------------

    if (

        "what do you remember" in text

        or

        "show my memory" in text

        or

        "show me what you remember" in text

    ):

        tool = get_tool(
            "get_all_memory"
        )


        if not tool:

            return (
                "Memory tool is not registered."
            )


        return tool()


    # -----------------------------------------
    # FORGET
    # -----------------------------------------

    forget_patterns = [

        r"forget my (.+)",

        r"forget (.+)",

        r"delete my memory of (.+)",

    ]


    for pattern in forget_patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            key = match.group(1).strip()


            tool = get_tool(
                "forget"
            )


            if not tool:

                return (
                    "Memory tool is not registered."
                )


            return tool(
                key
            )


    return None

def handle_windows(user_message):

    msg = user_message.lower()

    # Screenshot
    if "take screenshot" in msg or "screenshot" in msg:
        return get_tool("screenshot")()

    # Lock
    if (
        "lock computer" in msg
        or "lock pc" in msg
        or "lock my pc" in msg
        or "lock laptop" in msg
    ):
        return get_tool("lock")()

    # Shutdown
    if (
        "shutdown computer" in msg
        or "shutdown pc" in msg
        or "shutdown laptop" in msg
        or "turn off computer" in msg
        or "turn off pc" in msg
    ):
        return get_tool("shutdown")()

    # Restart
    if (
        "restart computer" in msg
        or "restart pc" in msg
        or "restart laptop" in msg
        or "reboot computer" in msg
    ):
        return get_tool("restart")()

    # ---------------- Volume ----------------

    if any(cmd in msg for cmd in [
        "volume up",
        "increase volume",
        "raise volume",
        "turn volume up",
        "volume high",
        "volume max",
        "max volume",
        "louder",
    ]):
        return get_tool("volume_up")()

    if any(cmd in msg for cmd in [
        "volume down",
        "decrease volume",
        "lower volume",
        "reduce volume",
        "volume low",
        "low volume",
        "softer",
    ]):
        return get_tool("volume_down")()

    if any(cmd in msg for cmd in [
        "mute",
        "silence",
        "turn off sound",
    ]) and "unmute" not in msg:
        return get_tool("mute")()

    if any(cmd in msg for cmd in [
        "unmute",
        "restore sound",
        "turn sound on",
    ]):
        return get_tool("unmute")()

    # ---------------- Brightness ----------------

    if any(cmd in msg for cmd in [
        "brightness up",
        "increase brightness",
        "raise brightness",
        "brighter",
    ]):
        return get_tool("brightness_up")()

    if any(cmd in msg for cmd in [
        "brightness down",
        "decrease brightness",
        "lower brightness",
        "dimmer",
    ]):
        return get_tool("brightness_down")()

    if any(cmd in msg for cmd in [
        "maximum brightness",
        "max brightness",
    ]):
        return get_tool("brightness_max")()

    if any(cmd in msg for cmd in [
        "minimum brightness",
        "min brightness",
    ]):
        return get_tool("brightness_min")()

    match = re.search(
        r"set brightness(?: to)? (\d{1,3})",
        msg,
    )

    if match:
        return get_tool("set_brightness")(int(match.group(1)))

    # Sleep
    if (
        "sleep computer" in msg
        or "sleep pc" in msg
        or "sleep laptop" in msg
        or "put computer to sleep" in msg
    ):
        return get_tool("sleep")()

    return None