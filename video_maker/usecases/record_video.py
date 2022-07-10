import os
from time import sleep
import subprocess
import pyautogui
import pydirectinput
from entities.match_data import MatchData


class RecordVideo:
    def __init__(self, match_data: MatchData) -> None:
        self.__video_file_dir = r'C:\Users\Joao\Videos'
        self.__replay_file_dir = r'C:\youtube\lol\replays'
        self.__match_data = match_data

    def record(self):
        # self.__show_mouse_position()
        self.__run_game()
        self.__run_obs()
        sleep(50)
        self.__select_player()
        pydirectinput.keyDown('o')
        pydirectinput.keyUp('o')
        pydirectinput.keyDown('u')
        pydirectinput.keyUp('u')
        sleep(5)
        self.__start_stop_recording()
        sleep(self.__duration_in_seconds())
        self.__start_stop_recording()
        sleep(10)
        pydirectinput.click(962, 641)
        sleep(1)
        pydirectinput.leftClick(962, 641)
        sleep(5)
        return self.__select_video_file()

    def __run_game(self):
        file = os.listdir(self.__replay_file_dir)[0]
        subprocess.call(
            ['start', fr'{self.__replay_file_dir}\{file}'], shell=True)

    def __run_obs(self):
        pyautogui.hotkey('super', '4')

    def __select_player(self):
        if self.__match_data['team1']['result'] == 'Victory':
            pydirectinput.keyDown('f1')
            pydirectinput.keyUp('f1')
            pydirectinput.keyDown(self.__match_data['player_index'])
            pydirectinput.keyUp(self.__match_data['player_index'])
            pydirectinput.keyDown(self.__match_data['player_index'])
            pydirectinput.keyUp(self.__match_data['player_index'])
        else:
            keys = ['q', 'w', 'e', 'r', 't']
            pydirectinput.keyDown('f2')
            pydirectinput.keyUp('f2')
            pydirectinput.keyDown(
                keys[int(self.__match_data['player_index']) - 1])
            pydirectinput.keyUp(
                keys[int(self.__match_data['player_index']) - 1])
            pydirectinput.keyDown(
                keys[int(self.__match_data['player_index']) - 1])
            pydirectinput.keyUp(
                keys[int(self.__match_data['player_index']) - 1])

    def __start_stop_recording(self):
        pyautogui.keyDown('shiftleft')
        pyautogui.keyDown('x')
        pyautogui.keyUp('shiftleft')
        pyautogui.keyUp('x')

    def __duration_in_seconds(self) -> int:
        array = self.__match_data['duration'].split(':')
        return (int(array[0]) * 60) + int(array[1]) - 15

    def __show_mouse_position(self):
        while True:
            print(pyautogui.position())
            sleep(1)

    def __select_video_file(self):
        file = os.listdir(self.__video__file_dir)
        return file[0]

    def remove_video_file(self):
        file = os.listdir(self.__video_file_dir)
        os.rename(os.path.join(self.__video_file_dir, file[0]), os.path.join(
            self.__video_file_dir, 'shorts', file[0]))
