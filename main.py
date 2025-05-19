# Imports - - - - - - - - - - -
import random
import os
import time
from pynput import keyboard # type: ignore


# Global variables - - - - - - 
windowWidth = 20
windowHeight = 10
listener = keyboard.Listener()
scene = "menu"
menuSelection = 1
y = int(windowHeight / 2)
x = int(windowWidth / 2)
gameSpeed = 0.5
score = 0
heading = "d"
snakeLenght = []

apple = "@" #@
snake = "¤" #▓
snakeHead = "■" #■
wall = "█" #█
space = "░" #░


# Code - - - - - - - - - - - - 
def Main() -> None:
    global scene

    listener = keyboard.Listener(on_press=OnPress)
    listener.start()

    while True:
        match scene:
            case "menu":
                MenuLoop()
            case "game":
                Game(GetMap())
            case "settings":
                SettingsLoop()
            case "quit":

                break
        

def MenuLoop() -> None:
    global scene
    scene = "menu"

    DrawMenu()

    while scene == "menu":
        time.sleep(1)


def SettingsLoop() -> None:
    global scene, listener
    scene = "settings"

    Settings()
    scene = "menu"


def DrawBorder(content: list[str]) -> None:
    # Draws border around selected list of strings
    extraSpace = 2
    emptySpace = (windowWidth * extraSpace)

    totalLines = len(content)
    paddingTop = (windowHeight - totalLines) // extraSpace
    paddingBottom = windowHeight - totalLines - paddingTop

    controlsText = [
        "Monevent: WASD", 
        "Select:  Enter", 
        "Quit:  Q"
    ]

    print("#" + "-" * emptySpace + "#")

    for _ in range(paddingTop):
        print("|" + " " * emptySpace + "|")

    for i in range(totalLines):
        line_content = content[i] if i < len(content) else ""
        print("|" + str(line_content).center(emptySpace) + "|")

    for _ in range(paddingBottom):
        print("|" + " " * emptySpace + "|")

    print("#" + "-" * emptySpace + "#")

    for line in controlsText:
        print("|" + " " * int((emptySpace / 2) - (len(line) / 2)) + line 
              + " " * int((emptySpace / 2) - (len(line) / 2)) + "|")

    print("#" + "-" * emptySpace + "#")


def DrawMenu() -> None:
    Clear()
    text = [
        "- CmdSnek: Simple Snake in Python -",
        "",
        "Start Game",
        "Settings",
        "Exit"
    ]
    text[menuSelection + 1] = "> " + text[menuSelection + 1]
    DrawBorder(text)


def DrawSettings() -> None:
    Clear()
    print(" - - - Gameplay:")
    print("| (s) Game speed:", str(gameSpeed))
    print("| (w) Game width:", windowWidth)
    print("| (h) Game height", windowHeight)
    print()
    print(" - - - Graphics:")
    print("| (1) Snake body Symbol:", snake)
    print("| (2) Snake head Symbol:", snakeHead)
    print("| (3) Apple Symbol:", apple)
    print("| (4) Wall Symbol:", wall)
    print("| (5) Space Symbol:", space)
    print()
    print("| Press Enter to return to menu")
    print("| or select a symbol to change a setting")


def Settings() -> None:
    # Main settings loop, lets you change any ingame value
    global snake, apple, wall, space, gameSpeed, windowWidth, windowHeight
    input() # fixes instant disappear thanks to pynput

    while True:
        try:
            DrawSettings()
            key = input()
            Clear()
            match key:
                case "1":
                    print("| Please, write your new symbol for Snake body")
                    snake = input()
                case "2":
                    print("| Please, write your new symbol for Snake head")
                    snake = input()
                case "3":
                    print("| Please, write your new symbol for Apple")
                    apple = input()
                case "4":
                    print("| Please, write your new symbol for Wall")
                    wall = input()
                case "5":
                    print("| Please, write your new symbol for Space")
                    space = input()
                case "s":
                    print("| Please, write your new Game speed")
                    gameSpeed = float(input())
                case "w":
                    print("| Please, write your new Game width")
                    windowWidth = int(input())
                case "h":
                    print("| Please, write your new Game height")
                    windowHeight = int(input())
                case _:
                    break
        except:
            input("| You've inputted a non-valid value, try again...")


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

        # Move snake's xy in a direction
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

        # Check all possible events
        if (len(snakeLenght) < ((windowHeight - 2) * (windowWidth - 2))):
            if map[y][x] == apple:
                score += 1
                map = SpawnApple(map)
            elif (map[y][x] == wall) or (map[y][x] == snake):
                GameEnd()
                break
            else:
                map[tempY][tempX] = space
                del snakeLenght[0]
        else:
            GameEnd()
            break
        
        # Move snake's body
        map[y][x] = snakeHead
        if len(snakeLenght) > 0:
            map[snakeLenght[-1][0]][snakeLenght[-1][1]] = snake
        snakeLenght.append([y, x])


def OnPress(key) -> str:
    # Main controls function, takes in all key presses and turns them
    # into actions depending on the scene
    global heading, scene, menuSelection

    try:
        if scene == "menu":
            if hasattr(key, 'char') and key.char:
                if key.char == "w":
                    if menuSelection > 1:
                        menuSelection -= 1
                elif key.char == "s":
                    if menuSelection < 3:
                        menuSelection += 1
                DrawMenu()
            elif key == key.enter:
                match menuSelection:
                    case 1:
                        scene = "game"
                    case 2:
                        scene = "settings"
                        pass
                    case 3:
                        input()
                        listener.stop()
                        scene = "quit"
                        pass
                    case _:
                        print("ERROR: You selected a non-existing option!")

        elif scene == "game":
            if hasattr(key, 'char') and key.char in "wasdq":
                heading = key.char

    except:
        pass


def Initialize(map) -> list:
    # Generates clean map and resets all values
    global x, y, heading, score, snakeLenght

    x = int(windowWidth / 2)
    y = int(windowHeight / 2)
    score = 0
    heading = "d"
    snakeLenght = []

    map[y][x] = snakeHead
    snakeLenght.append([y, x])
    map = SpawnApple(map)
    return map
        

def GameEnd() -> None:
    # Ends the basic game loop
    input() # fixes instant disappear thanks to pynput
    global score, scene
    if score >= ((windowHeight - 2) * (windowWidth - 2)):
        print(" - - - Victory!")
        print(f"| Your score was {score}! Perfect game!")
        input("Press Enter to return to the menu...")
    else:
        print(" - - - Game Over!")
        print(f"| Your score was {score}! That's not bad.")
        input("Press Enter to return to the menu...")
    scene = "menu"


def SpawnApple(map) -> list:
    # Spawn the apple on an empty location
    while True:
        appleY = random.randint(1, windowHeight - 2)
        appleX = random.randint(1, windowWidth - 2)
        if map[appleY][appleX] == space:
            map[appleY][appleX] = apple
            return map


def DrawMap(map) -> None:
    # Simply draws the map
    Clear()
    parsedMap = []
    for i in range(len(map)):
        line = ""
        for j in range(len(map[i])):
            line += str(map[i][j])
        parsedMap.append(line)
    DrawBorder(parsedMap)


def Clear():
    os.system("cls" if os.name == "nt" else "clear")


Main()
