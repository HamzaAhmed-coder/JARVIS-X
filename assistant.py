from app.voice.listener import record_audio, speech_to_text
from app.voice.speaker import speak
from app.planner import run_agent


def start():

    print("🤖 JARVIS Online")

    while True:

        print("\n🎤 Listening...")

        audio = record_audio(duration=5)

        text = speech_to_text(audio)

        if not text:
            print("No speech detected.")
            input("\nPress ENTER to listen again...")
            continue

        print(f"\nYou : {text}")

        if text.lower() in ["exit", "quit", "bye", "stop jarvis"]:
            speak("Goodbye.")
            break

        reply = run_agent(text)

        print(f"\nJARVIS : {reply}")

        if reply:
            speak(str(reply))

        input("\nPress ENTER for next command...")