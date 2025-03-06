# Imports - - - - - - - - - - -
import random
import os
import time
import sys
from pynput import keyboard # type: ignore


# Global variables - - - - - - 
windowWidth = 20
windowHeight = 10
listener = keyboard.Listener()

y = 5
x = 5
gameSpeed = 0.5
score = 0
heading = "d"
snakeLenght = []

apple = "@"
snake = "▓"
wall = "█"
space = "░"


# Code - - - - - - - - - - - - 
def Main() -> None:
    while True:
        DrawMenu()
        key = input()
        match key:
            case "1":
                # Starts main game loop
                Game(GetMap())
            case "2":
                # Shows settings
                Settings()
            case "3":
                # Exits the game
                break
            case _:
                pass


def DrawMenu() -> None:
    Clear()
    print(" - - - CmdSnek: Simple Snake in Python")
    print("| Press 1 to Start")
    print("| Press 2 to Settings")
    print("| Press 3 to Exit")


def DrawSettings() -> None:
    Clear()
    print(" - - - Controls:")
    print("| Movement: WASD")
    print("| Quit Game: Q")
    print()
    print(" - - - Graphics:")
    print("| (1) Snake Symbol:", snake)
    print("| (2) Apple Symbol:", apple)
    print("| (3) Wall Symbol:", wall)
    print("| (4) Space Symbol:", space)
    print()
    print("| Press Enter to return to menu")
    print("| or select a number to change graphics")


def Settings() -> None:
    global snake, apple, wall, space

    while True:
        DrawSettings()
        key = input()
        match key:
            case "1":
                Clear()
                print("| Please, write your new symbol for Snake")
                snake = input()
            case "2":
                Clear()
                print("| Please, write your new symbol for Apple")
                apple = input()
            case "3":
                Clear()
                print("| Please, write your new symbol for Wall")
                wall = input()
            case "4":
                Clear()
                print("| Please, write your new symbol for Space")
                space = input()
            case _:
                break


def GetMap() -> list:
    # Generates initial empty map
    map = []
    line = []

    for i in range(windowWidth):
        line.append(wall)
    map.append(line)
    line = []

    for i in range(windowHeight - 2):
        line.append(wall)
        for j in range(windowWidth - 2):
            line.append(space)
        line.append(wall)
        map.append(line)
        line = []

    for i in range(windowWidth):
        line.append(wall)
    map.append(line)
    line = []

    return map


def Game(map):
    # Starts main game loop
    map = Initialize(map)
    global x, y, heading, score

    while True:
        DrawMap(map)
        tempY = snakeLenght[0][0]
        tempX = snakeLenght[0][1]

        time.sleep(gameSpeed)

        # Move snake in a direction
        match heading:
            case "w":
                y -= 1
            case "a":
                x -= 1
            case "s":
                y += 1
            case "d":
                x += 1
            case "q":
                GameEnd()
                break
            case _:
                pass

        if map[y][x] == apple:
            # Snake picked up an apple
            score += 1
            map = SpawnApple(map)
        elif (map[y][x] == wall) or (map[y][x] == snake):
            GameEnd()
            break
        else:
            map[tempY][tempX] = space
            del snakeLenght[0]
        
        map[y][x] = snake
        snakeLenght.append([y, x])


def OnPress(key) -> str:
    global heading

    try:
        if key.char in "wasdq":
            heading = key.char
    except:
        pass


def Initialize(map) -> list:
    global x, y, heading, score, snakeLenght

    listener = keyboard.Listener(on_press=OnPress)
    listener.start()

    x = 5
    y = 5
    score = 0
    heading = "d"
    snakeLenght = []

    map[y][x] = snake
    snakeLenght.append([y, x])
    map = SpawnApple(map)
    return map
        

def GameEnd() -> None:
    sys.stdout.flush()
    listener.stop()

    print(" - - - Game Over!")
    print(f"| Your score was {score}! That's not bad.")
    input("Press Enter to return to the menu...")


def SpawnApple(map) -> list:
    while True:
        appleY = random.randint(1, windowHeight - 2)
        appleX = random.randint(1, windowWidth - 2)
        if map[appleY][appleX] == space:
            map[appleY][appleX] = apple
            return map


def DrawMap(map) -> None:
    Clear()
    for i in range(len(map)):
        line = ""
        for j in range(len(map[i])):
            line += str(map[i][j])
        print(line)


def Clear():
    os.system("cls" if os.name == "nt" else "clear")


Main()
