import subprocess
import time
import pyautogui


# =========================================
# OPEN WHATSAPP
# =========================================

def open_whatsapp():

    try:

        subprocess.Popen(
            r"explorer shell:AppsFolder\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"
        )

        time.sleep(5)

        return "WhatsApp opened."

    except Exception as e:

        return f"WhatsApp could not be opened: {e}"


# =========================================
# SEND WHATSAPP MESSAGE
# =========================================

def send_whatsapp(contact, message):

    try:

        print("================================")
        print("WHATSAPP AUTOMATION STARTED")
        print("CONTACT:", contact)
        print("MESSAGE:", message)
        print("================================")


        # ---------------------------------
        # OPEN WHATSAPP
        # ---------------------------------

        print("Opening WhatsApp...")

        open_whatsapp()

        time.sleep(4)


        # ---------------------------------
        # FOCUS WHATSAPP
        # ---------------------------------

        pyautogui.click(
            500,
            500
        )

        time.sleep(1)


        # ---------------------------------
        # SEARCH CONTACT
        # ---------------------------------

        print(
            "Searching Contact..."
        )

        pyautogui.hotkey(
            "ctrl",
            "f"
        )

        time.sleep(1)


        pyautogui.write(
            contact,
            interval=0.05
        )

        time.sleep(2)


        pyautogui.press(
            "enter"
        )

        time.sleep(3)


        # ---------------------------------
        # TYPE MESSAGE
        # ---------------------------------

        print(
            "Typing Message..."
        )


        pyautogui.write(
            message,
            interval=0.03
        )

        time.sleep(1)


        # ---------------------------------
        # SEND
        # ---------------------------------

        pyautogui.press(
            "enter"
        )


        print(
            "WhatsApp message sent."
        )


        return (
            f"Message sent to {contact}"
        )


    except Exception as e:

        print(
            "WHATSAPP ERROR:",
            e
        )


        return (
            f"WhatsApp Error: {e}"
        )