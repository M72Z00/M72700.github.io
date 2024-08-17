import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pacman')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define fonts
FONT = pygame.font.SysFont('Arial', 24)

#Initalize level complete variable
level_complete = False  # Flag to indicate if the level is complete

def reset_game():
    global score, lives, game_over, game_start, level_complete, pacman, ghost, maze
    score = 0
    lives = 3
    game_over = False
    game_start = True
    level_complete = False
    pacman.position = find_start_position(maze)
    ghost.position = [screen_width // 4, screen_height // 4]

# Pacman class definition
class Pacman:
    def __init__(self, position, speed):
        self.position = position  # Position is a list [x, y]
        self.direction = 'RIGHT'  # Initial movement direction
        self.speed = speed        # Movement speed
        self.radius = 20          # Radius of the Pacman circle

    def move(self, maze):
        # Update Pacman's position based on direction
        new_position = self.position[:]
        if self.direction == 'UP':
            new_position[1] -= self.speed
        elif self.direction == 'DOWN':
            new_position[1] += self.speed
        elif self.direction == 'LEFT':
            new_position[0] -= self.speed
        elif self.direction == 'RIGHT':
            new_position[0] += self.speed
        
        # Check for collision with walls
        if not maze.check_wall_collision(new_position):
            self.position = new_position

        # Boundary checks to keep Pacman within the screen
        self.position[0] = max(self.radius, min(self.position[0], screen_width - self.radius))
        self.position[1] = max(self.radius, min(self.position[1], screen_height - self.radius))

    def draw(self, screen):
        # Draw Pacman as a yellow circle
        pygame.draw.circle(screen, (255, 255, 0), (int(self.position[0]), int(self.position[1])), self.radius)

def find_start_position(maze):
    # Try to place Pac-Man at a random position until it's not inside a wall
    while True:
        position = [random.randint(20, screen_width - 20), random.randint(20, screen_height - 20)]
        if not maze.check_wall_collision(position):
            return position
class Ghost:
    def __init__(self, position, speed, ai_type):
        self.position = position  # Position is a list [x, y]
        self.direction = 'LEFT'  # Initial movement direction
        self.speed = speed       # Movement speed
        self.ai_type = ai_type   # AI type (e.g., 'CHASE', 'FLEE')
        self.size = 20           # Size of the ghost (used for square size)

    def move(self, pacman_position, maze):
        # Calculate direction vector from ghost to Pacman
        dx = pacman_position[0] - self.position[0]
        dy = pacman_position[1] - self.position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Normalize direction vector
        if distance != 0:
            dx /= distance
            dy /= distance

        # Determine direction based on AI type
        if self.ai_type == 'CHASE':
            direction_vector = [dx, dy]
        elif self.ai_type == 'FLEE':
            direction_vector = [-dx, -dy]

        # Determine potential new position
        new_position = [
            self.position[0] + direction_vector[0] * self.speed,
            self.position[1] + direction_vector[1] * self.speed
        ]

        # If the new position collides with a wall, adjust direction and try again
        if maze.check_wall_collision(new_position):
            # Try moving in perpendicular directions
            if abs(dx) > abs(dy):
                # Horizontal move failed, try vertical
                alt_position_1 = [
                    self.position[0],
                    self.position[1] + self.speed * (1 if dy > 0 else -1)
                ]
                if not maze.check_wall_collision(alt_position_1):
                    new_position = alt_position_1
            else:
                # Vertical move failed, try horizontal
                alt_position_2 = [
                    self.position[0] + self.speed * (1 if dx > 0 else -1),
                    self.position[1]
                ]
                if not maze.check_wall_collision(alt_position_2):
                    new_position = alt_position_2

        # Update the ghost's position
        self.position = new_position

        # Boundary checks to keep Ghost within the screen
        self.position[0] = max(self.size, min(self.position[0], screen_width - self.size))
        self.position[1] = max(self.size, min(self.position[1], screen_height - self.size))

    def draw(self, screen):
        # Draw Ghost as a red square
        pygame.draw.rect(screen, RED, (int(self.position[0] - self.size / 2), int(self.position[1] - self.size / 2), self.size, self.size))

# Maze class definition
class Maze:
    def __init__(self, layout):
        self.layout = layout  # Layout is a dictionary with 'pellets' and 'walls'
        self.pellets = [pygame.Rect(pellet, (10, 10)) for pellet in layout['pellets']]  # Create Rect objects for pellet collision detection
        self.walls = [pygame.Rect(wall, (random.randint(20, 60), random.randint(20, 60))) for wall in layout['walls']]  # Create Rect objects for wall collision detection with varied sizes

    def draw(self, screen):
        # Draw walls
        for wall in self.walls:
            pygame.draw.rect(screen, BLUE, wall)  # Blue walls
        # Draw pellets
        for pellet in self.pellets:
            pygame.draw.rect(screen, WHITE, pellet)

    def check_collision(self, position):
        # Check if Pacman collides with any pellet
        pacman_rect = pygame.Rect(position[0] - 10, position[1] - 10, 20, 20)  # Pacman's rectangle for collision detection
        for pellet in self.pellets:
            if pacman_rect.colliderect(pellet):
                self.pellets.remove(pellet)
                return True
        return False

    def is_empty(self):
        # Check if there are no more pellets
        return len(self.pellets) == 0
    
    def check_wall_collision(self, position):
        pacman_rect = pygame.Rect(position[0] - 10, position[1] - 10, 20, 20)
        for wall in self.walls:
            if pacman_rect.colliderect(wall):
                return True
        return False

# Initialize Pacman, Ghosts, and Maze
maze = Maze(layout={
    'pellets': [
        (100, 100), (200, 200), (300, 300), (400, 400),
        (500, 100), (600, 200), (700, 300), (150, 500)
    ],
    'walls': [
        (50, 50), (150, 50), (250, 50), (350, 50),
        (450, 50), (550, 50), (650, 50), (750, 50),
        (50, 150), (50, 250), (50, 350), (50, 450),
        (150, 450), (250, 450), (350, 450), (450, 450),
        (550, 450), (650, 450), (750, 450), (750, 150),
        (650, 150), (550, 150), (450, 150), (350, 150),
        (250, 150), (150, 150), (150, 250), (250, 250),
        (350, 250), (450, 250), (550, 250), (650, 250),
        (750, 250), (250, 350), (350, 350), (450, 350),
        (550, 350), (650, 350), (750, 350), (250, 450)
    ]
})

# Initialize Pacman with a non-colliding start position
pacman = Pacman(position=find_start_position(maze), speed=5)
ghost = Ghost(position=[screen_width // 4, screen_height // 4], speed=3, ai_type='CHASE')

# Game variables
score = 0
lives = 3
game_over = False  # Flag to indicate if the game is over
game_start = True  # Flag to indicate if the game has just started

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # Clean up Pygame resources
            sys.exit()     # Exit the program

    if not game_over:
        if game_start:
            # Display a message to start the game
            start_message = FONT.render("Press any key to start", True, WHITE)
            screen.fill(BLACK)  # Clear the screen
            screen.blit(start_message, (screen_width // 2 - start_message.get_width() // 2, screen_height // 2 - start_message.get_height() // 2))
            pygame.display.flip()

            keys = pygame.key.get_pressed()
            if any(keys):
                game_start = False  # Start the game when any key is pressed
        elif level_complete:
            # Display level complete message
            level_complete_message = FONT.render("YOU WIN! Q to Quit", True, WHITE)
            screen.fill(BLACK)  # Clear the screen
            screen.blit(level_complete_message, (screen_width // 2 - level_complete_message.get_width() // 2, screen_height // 2 - level_complete_message.get_height() // 2))
            pygame.display.flip()

            # Handle user input for level complete screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                        
        else:
            # Handle user input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                pacman.direction = 'UP'
            elif keys[pygame.K_DOWN]:
                pacman.direction = 'DOWN'
            elif keys[pygame.K_LEFT]:
                pacman.direction = 'LEFT'
            elif keys[pygame.K_RIGHT]:
                pacman.direction = 'RIGHT'

            # Move Pacman and Ghost
            pacman.move(maze)  # Pass maze to check for wall collisions
            ghost.move(pacman.position, maze)

            # Check for collisions between Pacman and Ghost
            distance = math.sqrt((pacman.position[0] - ghost.position[0]) ** 2 + (pacman.position[1] - ghost.position[1]) ** 2)
            if distance < pacman.radius + ghost.size:  # Collision detected
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    # Reset Pacman and Ghost positions after losing a life
                    pacman.position = find_start_position(maze)
                    ghost.position = [screen_width // 4, screen_height // 4]
                    pygame.time.wait(1000)  # Pause for 1 second before resuming

            # Check for collisions between Pacman and pellets
            if maze.check_collision(pacman.position):
                score += 1  # Increment score

            # Check if all pellets are collected
            if maze.is_empty():
                level_complete = True

            # Clear screen
            screen.fill(BLACK)

            # Draw Maze, Pacman, and Ghost
            maze.draw(screen)
            pacman.draw(screen)
            ghost.draw(screen)

            # Draw score and lives
            score_text = FONT.render(f"Score: {score}", True, WHITE)
            lives_text = FONT.render(f"Lives: {lives}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (10, 40))

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            pygame.time.Clock().tick(30)  # 30 frames per second

    else:  # Game Over
        # Display the game over message
        game_over_message = FONT.render("Game Over! Press R to Restart or Q to Quit", True, WHITE)
        screen.fill(BLACK)  # Clear the screen
        screen.blit(game_over_message, (screen_width // 2 - game_over_message.get_width() // 2, screen_height // 2 - game_over_message.get_height() // 2))
        pygame.display.flip()

        # Handle user input for game over screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    # Reset the game
                    reset_game()
