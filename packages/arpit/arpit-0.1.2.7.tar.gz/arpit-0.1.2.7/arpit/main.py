from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import json
import argparse
import sys, time
import webbrowser
from .utils import *
from termcolor import colored
from .video import execute_video
from .music import main as music_main


def main():
    parser = argparse.ArgumentParser(description="Hi, I'm Arpit. This is a library solely based on who I am.")
    parser.add_argument("-d", "--desc", action="store_true", help="gives a description of me.")    
    parser.add_argument("-l", "--links", action="store_true", help="redirects to my link tree.")
    parser.add_argument("-m", "--music", action="store_true", help="plays my favourite music.")    
    parser.add_argument("-s", "--secret", nargs='*', help="enter your birthday in the format DDMMYY.")
    parser.add_argument("-w", "--website", action="store_true", help="redirects to my website.")

    args = parser.parse_args()
    
    if not any(vars(args).values()) and not args.secret:
        try:
            webbrowser.open("https://youtu.be/cQf2UEkFYTg")
            # execute_video()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
    if args.secret:
        try:
            if args.secret==["080205"]:
                print(colored("Prompt accepted", "green"))
                time.sleep(1)
                print(colored("Loading cassette...", "yellow"))
                play_audio("assets/audio/loading_cassette.mp3")
                print(colored("Empty cassette detected.", "red", attrs=["blink"]))

            else:
                print(colored("you're not the one."))
                sys.exit()
        except AttributeError:
            print(colored("no input given."))
            
    if args.desc:
        
        with open(path_convertor('assets/data.json')) as json_file:
            data = json.load(json_file)
        print(data["desc"])
        
    if args.music:
        music_main()
        
    if args.links:
        webbrowser.open("https://linktr.ee/arpy8")
        # play_audio("assets/audio/affirm.mp3")
        
    if args.website:
        webbrowser.open("https://arpy8.github.io/")
        # play_audio("assets/audio/affirm.mp3")
        

if __name__ == "__main__":
    main()