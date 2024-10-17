import pygame
import random
import sys
import os
#silly mess around

clickM = False

# Define constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
GRID_SIZE = 10
CELL_SIZE = 40
SHIP_TYPES = [('Battleship', 4), ('Submarine', 3), ('Destroyer', 2)]  # (name, length)
Playergameend = 3
computergameend = 3
# Colors
WATER_COLOR = (0, 0, 255)
SHIP_COLOR = (255, 0, 0)
HIT_COLOR = (255, 165, 0)
MISS_COLOR = (100, 100, 100)
SunkColor = (0, 255, 0)

pygame.init()
pygame.font.init()

#cursor
#exe image conversion
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



font = pygame.font.SysFont('Ariel_Bold', 50)
class Game:
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Battleship Game')
        self.CursorImage = pygame.image.load(resource_path('Sheild Symbol.png')).convert_alpha()
        self.CursorImage = pygame.transform.scale(self.CursorImage, (50, 50))
        self.CursorImage2 = pygame.image.load(resource_path("target.png")).convert_alpha()
        self.CursorImage2 = pygame.transform.scale(self.CursorImage2, (50, 50))
        pygame.mouse.set_visible(True)
        self.clock = pygame.time.Clock()
        self.player_board = Board()
        self.computer_board = Board()
        self.computer = Player('Computer', self.computer_board, is_computer=True)
        self.player = Player('Player', self.player_board)
        self.current_turn = self.player
        self.MenuState = True
        self.CreditState = False
    
    def Prerun(self):
        while True:
            if self.CreditState == True:
                self.ShowCredits()
            elif self.MenuState:
                self.ShowMenu()
            elif self.MenuState == False:
                self.run()
    def run(self):
        # Main game loop
        running = True
        while running:
            self.handle_events()
            self.draw()
            self.check_game_over()
            pygame.display.flip()
            self.clock.tick(30)
            
             
    def ShowMenu(self):
        pygame.mouse.set_visible(True)
        self.screen.fill((255, 255, 255))
        StartButton = pygame.Rect(400, 200, 200, 50)
        CreditsButton = pygame.Rect(400, 300, 200, 50)

        pygame.draw.rect(self.screen, (0, 255, 0), StartButton)
        pygame.draw.rect(self.screen, (0, 0, 255), CreditsButton)

        StartText = font.render('Start', True, (0, 0, 0))
        CreditsText = font.render('Credits', True, (0, 0, 0))

        self.screen.blit(StartText, (450, 210))
        self.screen.blit(CreditsText, (430, 310))

        pygame.display.flip()
        self.MenuEvents()

    def MenuEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    MousePos = event.pos
                    if 400 <= MousePos[0] <= 600 and 200 <= MousePos[1] <= 250:
                        self.MenuState = False  # Start game
                    elif 400 <= MousePos[0] <= 600 and 300 <= MousePos[1] <= 350:
                        self.CreditState = True

    def ShowCredits(self):
        
        self.screen.fill((255, 255, 255))
        CreditsText = font.render('Credit to Jackson Mackey', True, (0, 0, 0))
        BlackButton = pygame.Rect(400, 300, 200, 50)
        pygame.draw.rect(self.screen, (255, 0, 0), BlackButton)

        BlackText = font.render('Back', True, (0, 0, 0))
        self.screen.blit(CreditsText, (300, 250))
        self.screen.blit(BlackText, (450, 310))

        pygame.display.flip()
        self.CreditEvents()
        
    def CreditEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    MousePos = event.pos
                    if 400 <= MousePos[0] <= 600 and 300 <= MousePos[1] <= 350:
                        self.MenuState = True  # Go back to menu
                        self.CreditState = False

    def handle_events(self):
        # Handle player inputs and game events
        BackButton = pygame.Rect(875, 0, 100, 40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                # Get mouse position
                MousePos = event.pos
            
                # Check if "Back" button is clicked
                if BackButton.collidepoint(MousePos):
                    # Perform the action for the "Back" button click (e.g., return to the menu)
                    self.MenuState = True
                    self.CreditState = False
                    self.Prerun()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_player_turn(event.pos)
            self.handle_computer_turn()

    def DisplayText(self, pos, message,length,delay):
        flag = True
        delay = int(delay / 2.8)
        text_surface = font.render(f"{length}{message}!", flag, (255, 0, 255))  # Red color for hit
        self.screen.blit(text_surface, pos)  # Position the text at (100, 100)
        pygame.display.flip()
        pygame.time.delay(delay)
    def handle_player_turn(self, pos):
        # Player's turn logic, check clicks, and attack
        global Playergameend
        global clickM
        des = True
        if self.current_turn == self.player:
            ClickX = (pos[0] - 520) // CELL_SIZE
            ClickY = (pos[1] - 50) // CELL_SIZE
            if 0 <= ClickX < GRID_SIZE and 0 <= ClickY < GRID_SIZE:
                gridNum = self.computer_board.grid[ClickY][ClickX]
                if gridNum != 2 and gridNum != 3 and gridNum != 4:
                    if gridNum == 1:  # If it's a ship
                        self.computer_board.grid[ClickY][ClickX] = 2  # Mark as hit
                        for ship in self.computer_board.ships:
                            if self.computer_board.check_ship_sunk_recursively(ship):
                                self.computer_board.draw(self.screen, offset=(520, 50))
                                self.DisplayText((550,250), '-unit ship sunk',ship.length,3000)
                                des = False
                                Playergameend -= 1
                                pygame.display.flip()
                                if Playergameend <= 0:
                                    self.screen.fill((255, 255, 255))
                                    self.DisplayText((450,250), 'Player Wins','',10000)
                                    self.MenuState = True
                                    self.Prerun()
                                    clickM = True
                    else:
                        self.computer_board.grid[ClickY][ClickX] = 3  # Mark as miss
                        self.computer_board.draw(self.screen, offset=(520, 50))
                        self.DisplayText((pos[0]-50,pos[1]), 'miss', length='',delay=500)
                        self.current_turn = self.computer  # Switch turn to computer
                    if gridNum == 1 and des != False:
                        self.computer_board.draw(self.screen, offset=(520, 50))
                        self.DisplayText((pos[0]-50,pos[1]), 'hit','',1000)

    def handle_computer_turn(self):
        pygame.mouse.set_visible(False)
        # Computer's turn logic, randomly attack player's grid
        global computergameend
        global clickM
        des = True
        if self.current_turn == self.computer:
            ComputerHitX, ComputerHitY = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            gridNum = self.player_board.grid[ComputerHitY][ComputerHitX]
            if gridNum != 2 and gridNum != 3 and gridNum != 4:
                if gridNum == 1:
                    self.player_board.grid[ComputerHitY][ComputerHitX] = 2  # Mark as hit
                    for ship in self.player_board.ships:
                        if self.player_board.check_ship_sunk_recursively(ship):
                            self.player_board.draw(self.screen, offset=(82.5, 50))
                            self.DisplayText((182.5+50, 250), '-unit ship sunk',ship.length,3000)
                            des = False
                            computergameend -= 1
                            pygame.display.flip()
                            if computergameend <= 0:
                                self.screen.fill((255, 255, 255))
                                self.DisplayText((450,250), 'Computer Wins','',10000)
                                pygame.quit()
                                sys.exit()
                                clickM = True
                else:
                    self.player_board.grid[ComputerHitY][ComputerHitX] = 3  # Mark as miss
                    self.player_board.draw(self.screen, offset=(82.5, 50))
                    self.DisplayText((182.5+50, 250), 'miss', length='',delay=650)
                    self.current_turn = self.player  # Switch turn to computer
                if gridNum == 1 and des != False:
                    self.player_board.draw(self.screen, offset=(82.5, 50))
                    self.DisplayText((182.5+50, 250), 'hit','',1000)
    def check_game_over(self):
        # Check if all ships of either player or computer are sunk
        if self.player_board.all_ships_sunk() or self.computer_board.all_ships_sunk():
            print("Game Over")
            pygame.quit()
            exit()

    def draw(self):
        self.screen.fill((255, 255, 255))
        # Draw boards, ships, hits, and misses
        self.player_board.draw(self.screen, offset=(45 + 75 / 2, 50))  # centers the board
        self.computer_board.draw(self.screen, offset=(520, 50))
        MouseX, MouseY = pygame.mouse.get_pos()
        if clickM == True:
            self.screen.blit(self.CursorImage, (MouseX - self.CursorImage.get_width() // 2, MouseY - self.CursorImage.get_height() // 2))
        elif self.current_turn == self.player:
            self.screen.blit(self.CursorImage2, (MouseX - self.CursorImage2.get_width() // 2, MouseY - self.CursorImage2.get_height() // 2))

class Board:
    def __init__(self):
        self.grid = [['0' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]  # '0' for water
        self.ships = []
        self.place_ships()

    def place_ships(self):
        for name, length in SHIP_TYPES:
            print(name, length)
            self.place_ship_recursively(length)

    def place_ship_recursively(self, ship_length):
        # Recursively try placing a ship
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        orientation = random.choice(['H', 'V'])
        
        if self.can_place_ship(x, y, ship_length, orientation):
            ship = Ship(ship_length, orientation, (x, y))
            print(ship)
            print(f"{self.ships}liity")
            self.ships.append(ship)
            print(self.ships)
            self.mark_ship_on_grid(ship)
        else:
            self.place_ship_recursively(ship_length)

    def can_place_ship(self, x, y, length, orientation):
        # Check if a ship can be placed at the given coordinates
        # Add boundary checks and overlap checks
        #get ship length and start pos and orien, check if too close boarder
        #if orientation == 'V' and x >= 6
        print(f'testhere{self.ships}')
        print(len(self.grid))
        if orientation == 'H':
            if x + length > GRID_SIZE:
                return False
            for i in range(-1, length + 1):
                for y2 in range(-1, 2):
                    bufferX = x+i
                    bufferY = y+y2
                    if 0 <= bufferX < GRID_SIZE and 0 <= bufferY < GRID_SIZE:
                        if self.grid[bufferY][bufferX] == 1:
                            print("-----col-----")
                            return False
            return True
        if orientation == 'V':
            if y + length > GRID_SIZE:
                return False
            for i in range(-1, length + 1):
                for x2 in range(-1, 2):
                    bufferX = x+x2
                    bufferY = y+i
                    if 0 <= bufferX < GRID_SIZE and 0 <= bufferY < GRID_SIZE:
                        if self.grid[bufferY][bufferX] == 1:
                            print("-----col-----")
                            return False
            return True
        #check for ship colide
        #mark previos ship lengths

    def mark_ship_on_grid(self, ship):
        #self.grid[(ship.start_pos[0]-1)][ship.start_pos[1]-1] = '1'
        x, y =ship.start_pos
        print(x)
        #changing backend grid
        if ship.orientation == 'H':
            for i in range(ship.length):
                self.grid[y][x + i] = 1
        elif ship.orientation == 'V':
            for i in range(ship.length):
                self.grid[y + i][x] = 1
        print(self.grid)
        pass

    def all_ships_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)

    def check_ship_sunk_recursively(self, ship, index=0):
        # Base case
        if index >= ship.length:
            self.markSunkShip(ship)
            return True
        #other shit
        x, y = ship.start_pos
        if ship.orientation == 'H':
            if self.grid[y][x + index] != 2:  # Check if part is not hit (hibt = 2)
                return False
            else:
                # Recursive wow
                return self.check_ship_sunk_recursively(ship, index + 1)
        else:  # for the verticle
            if self.grid[y + index][x] != 2:  #same stuff
                return False 
            else:
                # Recursive wow
                return self.check_ship_sunk_recursively(ship, index + 1)

    def markSunkShip(self, ship):
        # Mark all parts of the ship as sunk (4)
        x, y = ship.start_pos
        if ship.orientation == 'H':
            for i in range(ship.length):
                self.grid[y][x + i] = 4
        else:  # Vertical
            for i in range(ship.length):
                self.grid[y + i][x] = 4

    def draw(self, screen, offset):
        # Draw the board with ships, hits, and misses
        BackButton = pygame.Rect(875, 0, 100, 40)
        pygame.draw.rect(screen, (255, 0, 0), BackButton)
        BackText = font.render('Back', True, (0, 0, 0))
        screen.blit(BackText, (880, 5))
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                # Draw each cell based on its state
                rect = pygame.Rect(offset[0] + col * CELL_SIZE, offset[1] + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, WATER_COLOR, rect)
                if self.grid[row][col] == 1:
                    if offset==(45 + 75/2, 50):
                        pygame.draw.rect(screen, SHIP_COLOR, rect)
                    else:
                        pygame.draw.rect(screen, WATER_COLOR, rect)
                elif self.grid[row][col] == 4:
                    pygame.draw.rect(screen, SunkColor, rect)
                elif self.grid[row][col] == 2:
                    pygame.draw.rect(screen, HIT_COLOR, rect)
                elif self.grid[row][col] == 3:
                    pygame.draw.rect(screen, MISS_COLOR, rect)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)


class Ship:
    def __init__(self, length, orientation, start_pos):
        self.length = length
        self.orientation = orientation
        self.start_pos = start_pos
        self.hits = 0

    def is_sunk(self):
        return self.hits >= self.length


class Player:
    def __init__(self, name, board, is_computer=False):
        self.name = name
        self.board = board
        self.is_computer = is_computer

# Main execution
if __name__ == '__main__':
    game = Game()
    game.Prerun()
