import random
import datetime
import sweeperlib as slib


# THE WINDOW NEEDS TO BE MANUALLY CLOSED 
# (IT DOESNT PHYSICALLY DISAPPEAR) AFTER 
# EVERY GAME SO THAT IT CAN BE RESET!

# THE GAME DOESN'T STORE STATISTICS, OVERWRITES THEM.

gamestate = { #DICTIONARY WITH GAME PARAMETERS
    "tiles": [] ,
    "exposed_tiles": [] ,
    "flagged_tiles": [] ,
    "game_over": False ,
    "width": 10 ,
    "length": 10 ,
    "mine_number": 15 ,
    "turn_amount": 0 ,
    "flag_amount": 0 ,
    "game_amount": 0 ,
    "starting_time": None ,
    "ending_time": None

}

def main_menu():
    """
    main menu with options
    """
    while True:
        print("\n|Minesweeper|\nChoose an option:\n")
        print("1-New Game")
        print("2-View Statistics")
        print("3-Quit")
        choice = input("\nInput: ")
        
        if choice == "1":

            gamestate["game_amount"]

            custom = input("Do you want to customize the game? Yes/No \n").lower()

            if custom == "yes":
                while True:
                    try:
                        answer = int(input("Input desired length: "))
                        if answer > 60:
                            print("\nPlease enter a smaller number!")
                        elif answer < 2:
                            print("\nPlease enter a bigger number!")
                        
                        else:
                            break
                    except ValueError:
                        print("Please only enter a number!")

                while True:
                    try:
                        answer2 = int(input("Input desired width: "))
                        if answer2 > 60:
                            print("\nPlease enter a smaller number!")
                        elif answer < 2:
                            print("\nPlease enter a bigger number!")
                        else:
                            break

                    except ValueError:
                        print("Please only enter a number!")

                while True:
                    try:
                        maxmines = (answer * answer2) - 1

                        answer3 = int(input("Input desired mine count: "))

                        if answer3 > maxmines:                    
                            print("\nPlease enter a smaller number.")
                        else:
                            break

                    except ValueError:
                        print("Please enter a valid number.")

                gamestate["length"] = answer
                gamestate["width"] = answer2
                gamestate["mine_number"] = answer3

                start_game()

            if custom == "no":
                gamestate["length"] = 10
                gamestate["width"] = 10
                gamestate["mine_number"] = 15

                start_game()

            else:
                main_menu()


                
        elif choice == "2":
            print("\nStatistics:\n")
            stats() #PUT THE NOTEPAD WITH STATS HERE

        elif choice == "3":
            break

            
        else:
            print("\nPlease input your choice again.")

def game_duration():

    if gamestate["starting_time"] is None:
        if gamestate["ending_time"] is None:
            return " No game played yet."    
             # just in case player gets into stats before 
             # playing? They shouldnt be able to.
    

    gamestate["ending_time"]=datetime.datetime.now()
    gameduration = gamestate["ending_time"]- gamestate["starting_time"]

    minutes = gameduration.seconds//60
    seconds = gameduration.seconds%60

    return f"{int(minutes)} minutes and {int(seconds)} seconds"
    


def filestats(current_time, result, mines_left, turns_played, duration):
    """
    filestats
    """
    current_time=datetime.datetime.now()
    with open("statistics.txt", "w") as file:
        file.write(f"Date: {current_time}\nResult: {result}\nMines Left: {mines_left}\nTurns: {turns_played}\nGame Duration: {duration}")

def stats():
    """
    configure all statistics.
    """

    if gamestate["starting_time"] is None:
        print("Please play a game to see statistics!")
        return

    current_time=datetime.datetime.now()
    gamestate["ending_time"] = gamestate["ending_time"] or current_time

    mines_left = gamestate["mine_number"] - gamestate["flag_amount"]

    turns_played = gamestate["turn_amount"]

    duration= game_duration()

    if gamestate["game_over"] == True:
        result = "lost"
    else:
        result = "won"

    file = filestats(current_time, result, mines_left, turns_played, duration)

    try:
        with open("statistics.txt", "r") as file:

            print(file.read())

    except FileNotFoundError:
        print("No statistics.\n")


def minefield(gamestate):
    """
    tile grid and mine setup
    """

    #SET UP TILES
    tiles = []

    for y in range(gamestate["length"]):
        tiles.append([]) 

        for x in range(gamestate["width"]):
            tiles[y].append(0)       
    
    #SET UP MINES

    placed_mines = 0

    while placed_mines < gamestate["mine_number"]:

        x = random.randint(0, gamestate["width"] - 1)
        y = random.randint(0, gamestate["length"] - 1)

        if tiles[y][x] != 'x': 

            tiles[y][x] = 'x'
            placed_mines += 1
            
    #CALCULATE NUMBER
    for y in range(gamestate["length"]):  
        for x in range(gamestate["width"]):

            if tiles[y][x] != 'x': 
                surroundings = [(x, y), (x + 1, y), (x - 1, y), (x, y + 1),
                (x - 1, y - 1), (x + 1, y + 1), (x - 1, y + 1),
                (x + 1, y - 1), (x, y - 1)]
                mine_count = 0
                for x2, y2 in surroundings:
                    if 0 <= x2 < gamestate["width"] and 0 <= y2 < gamestate["length"] and tiles[y2][x2] == 'x': 
                        mine_count += 1

                tiles[y][x] = mine_count

    #UPDATE GAMESTATE
    gamestate["tiles"] = tiles


def floodfill(x, y):
    """
    floodfill
    """

    tiles = gamestate["tiles"]
    exposed_tiles = gamestate["exposed_tiles"]

    if tiles[y][x] == 0:
        if (x, y) not in exposed_tiles:
            exposed_tiles.append((x, y))
        
            if x > 0:
                floodfill(x - 1, y)  
            if x < gamestate["width"] - 1:
                floodfill(x + 1, y)  
            if y > 0:
                floodfill(x, y - 1)
            if y < gamestate["length"] - 1:
                floodfill(x, y + 1) 
        
    elif gamestate["tiles"][y][x] != 0:
        exposed_tiles.append((x, y))

    tiles = gamestate["tiles"]
    exposed_tiles = gamestate["exposed_tiles"]

def draw_tile(x, y, tile):
    """
    use the proper sprite based on the tile
    """

    numbers = [1,2,3,4,5,6,7,8]

    if (x, y) in gamestate["flagged_tiles"]:
        slib.prepare_sprite("f", x * 40, y * 40)
    elif tile == "x": 
        slib.prepare_sprite("x", x * 40, y * 40)
    elif tile == " ": 
        slib.prepare_sprite(" ", x * 40, y * 40)
    elif tile == 0:  
        slib.prepare_sprite("0", x * 40, y * 40)
    else:
        for number in numbers:
            if tile == number:
                slib.prepare_sprite(str(number), x * 40, y * 40)
                break 
    

def handle_mouse(x, y, button, modifiers):
    """
    mouse handler
    """

    x = x // 40
    y = y // 40

    if button == slib.MOUSE_LEFT:
        left_click(x, y)

    elif button == slib.MOUSE_RIGHT:
        right_click(x, y)


def left_click(x,y):
    """
    left click
    """
    if gamestate["game_over"] == True:
        return



    gamestate["turn_amount"] += 1
    
    if (x, y) not in gamestate["exposed_tiles"]: 
        if gamestate["tiles"][y][x] == 0:
            floodfill(x, y)
        else:
            gamestate["exposed_tiles"].append((x, y))

        if gamestate["tiles"][y][x] == 'x': 
            gamestate["game_over"] = True
            gamestate["exposed_tiles"].append((x, y))
            print("\nGame Over, close the Window to go back to the main menu!")

            
        
        if gamestate["game_over"] == False:
            if gamestate["length"]* gamestate["width"] - gamestate["mine_number"] == len(gamestate["exposed_tiles"]):
                gamestate["game_over"] = True
                print("You won! Please close the Window to go back to the main menu!" )


def right_click(x,y):
    """
    right click
    """

    if (x,y) in gamestate["flagged_tiles"]:
        gamestate["flagged_tiles"].remove((x, y))
        gamestate["flag_amount"] = gamestate["flag_amount"] - 1

    elif (x,y) not in gamestate["exposed_tiles"]:
        gamestate["flagged_tiles"].append((x, y))
        gamestate["flag_amount"] += 1

def draw_field():
    """
    draw the field on the window
    """
    for y in range(gamestate["length"]):  
        for x in range(gamestate["width"]):
            if (x, y) in gamestate["exposed_tiles"]:
                tile = gamestate["tiles"][y][x]
            else:
                tile = ' '

            draw_tile(x, y, tile)

    slib.draw_sprites()



def start_game():
    """
    reset all parameters
    setup and start the game
    """

    gamestate["game_over"] = False
    gamestate["exposed_tiles"] = []
    gamestate["flagged_tiles"] = []
    gamestate["turn_amount"] = 0
    gamestate["flag_amount"] = 0
    gamestate["starting_time"] = datetime.datetime.now()



    slib.load_sprites("sprites")
    slib.create_window(width=gamestate["width"] * 40, height=gamestate["length"] * 40)

    minefield(gamestate)
    
    slib.clear_window()
    slib.draw_background()
    slib.set_mouse_handler(handle_mouse)
    slib.set_draw_handler(draw_field)

    slib.start()

if __name__ == "__main__":
    main_menu()
