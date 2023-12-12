import json
import sys, time, os
import threading
import keyboard
from .utils import play_audio, path_convertor

music_played = True

def load_animation(name, artist):
    global music_played

    load_str = f"playing {name} by {artist}  "
    ls_len = len(load_str)

    animation = [".(^-^)'", "-(^-^)-", "'(^-^).", "-(^-^)-", ".(^-^)'", "-(^-^)-", "'(^-^).", "-(^-^)-"]
    anicount = 0

    counttime = 0
    i = 0

    while music_played:
        time.sleep(0.125)

        load_str_list = list(load_str)

        x = ord(load_str_list[i])
        y = 0

        if x != 32 and x != 46:
            if x > 90:
                y = x - 32
            else:
                y = x + 32
            load_str_list[i] = chr(y)

        res = ''
        for j in range(ls_len):
            res = res + load_str_list[j]

        sys.stdout.write("\r" + res + animation[anicount])
        sys.stdout.flush()

        load_str = res

        anicount = (anicount + 1) % 4
        i = (i + 1) % ls_len
        counttime = counttime + 1

    # if os.name == "nt":
    #     os.system("cls")
    os.system("exit")  
    

def get_music_data():
    relative_json_path = path_convertor('assets/data.json')
    
    with open(relative_json_path) as json_file:
        data = json.load(json_file)

    return data["music"]["name"], data["music"]["artist"]

def exit_program():
    music_played = False

def main():
    global music_played, audio_thread, animation_thread

    name, artist = get_music_data()
    path = 'assets/audio/song.mp3'
    

    animation_thread = threading.Thread(target=load_animation, args=[name, artist])
    audio_thread = threading.Thread(target=play_audio, args=[path])

    audio_thread.start()
    animation_thread.start()

    keyboard.add_hotkey('esc', exit_program)
    # try:
    #     while music_played:
    #         time.sleep(1)
    
    if KeyboardInterrupt:
        print("\nCtrl+C pressed. Stopping animation and audio playback.")
        keyboard.wait('esc')
        
        # audio_thread.join()
        # animation_thread.join()
        
        
        # exit_program()
        sys.exit()

# def exit_program():
#     global music_played, animation_thread
#     animation_thread.join()

#     music_played = False
#     os.system("exit")
#     sys.exit()