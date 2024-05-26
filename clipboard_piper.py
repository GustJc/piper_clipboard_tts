from os import getenv
from pathlib import Path
from threading import Thread
from urllib.parse import urlencode
import sounddevice as sd
import soundfile as sf


import keyboard
import pyperclip
import time
import unicodedata
import sys, os
import subprocess


PIPER_BIN = getenv('PIPER_BIN', 'F:\Programas\Piper TTS\piper\piper.exe')
PIPER_PATH = Path(PIPER_BIN).resolve().parent

EXIT_PROGRAM = False

WAV_PATH = Path(__file__).resolve().parent / 'audio\\'

WAVE_FILENAME_1 = 'tts1.wav'
WAVE_FILENAME_2 = 'tts2.wav'
WAV_FILE = WAV_PATH / WAVE_FILENAME_1
IS_FIRST_WAV = True
CHECK_CLIPBOARD = True
CLIPBOARD_AUTO_PLAY = True

japanese_text_found_callback = None

VOICE_ID = None


def speak_voice(sentence, play_new_voice=True):
    global WAV_FILE
    global last_voice_id

    switch_wav_file()
    
    cmd = r'echo "{}" | "{}" --model "{}" --output_file "{}"' \
        .format(sentence.replace('\n', ' '), PIPER_BIN, PIPER_PATH / VOICE_ID, WAV_FILE)
    print("Command: {}".format(cmd))
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    ps.communicate()

    # Dont generate voice, only update ui with callback
    if play_new_voice == False:
        print('skip playing voice')
        return

    last_voice_id = VOICE_ID

    play_voice()

def switch_wav_file():
    global WAV_FILE
    global IS_FIRST_WAV

    if IS_FIRST_WAV:
        WAV_FILE = WAV_PATH / WAVE_FILENAME_1
    else:
        WAV_FILE = WAV_PATH / WAVE_FILENAME_2

    IS_FIRST_WAV = not IS_FIRST_WAV

def play_voice():
    global WAV_FILE

    data, fs = sf.read(WAV_FILE, dtype='float32')
    sd.stop()
    sd.play(data, fs)


current_text = ''
previous_text = ''
last_voice_id = VOICE_ID
## Thread that keeps checking the clipboard for new text
def check_clipboard():
    global current_text
    global previous_text
    global EXIT_PROGRAM
    while EXIT_PROGRAM == False:
        if CHECK_CLIPBOARD == True:
            current_text = pyperclip.paste()
            if current_text:
                check_new_text_and_play_voice()
        time.sleep(0.1)

def check_new_text_and_play_voice(not_from_clipboard = False, sentence = None):
    global current_text
    global previous_text
    global last_voice_id

    changed = current_text != previous_text
    if not_from_clipboard:
        changed = sentence != previous_text
    if last_voice_id != VOICE_ID:
        changed = True

    if changed:
        auto_play_voice = CLIPBOARD_AUTO_PLAY
        if not_from_clipboard:
            auto_play_voice = True
            if CHECK_CLIPBOARD:
                pyperclip.copy(sentence) # so it does not trigger check clipboard
                print('Clipboard text: ' + current_text)
            current_text = sentence

        print('New text: ' + current_text)
        previous_text = current_text
        speak_voice(current_text, auto_play_voice)
    elif not_from_clipboard:
        # Replay last voice if from UI
        print("Replaying voice if the same")
        play_voice()

def stop_voice_play():
    print("Killing voice.")
    sd.stop()

def run_clipboard_voice():
    print('Using voiceid : ' + str(VOICE_ID))
    print('Ctrl+D to exit')
    print('Ctrl+alt+a to kill voice')

    # Create a keyboard listener
    keyboard.add_hotkey('ctrl+alt+a', stop_voice_play)

    check_clipboard()

    print("Ending clipboard observer...")

if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) > 0:
        VOICE_ID = int(args[0])

    run_clipboard_voice()

