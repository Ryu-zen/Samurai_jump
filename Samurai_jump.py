import pygame
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 350
GRAVITY = 1
JUMP_STRENGTH = 15
FPS = 60
OBSTACLE_GAP = 200  # Minimum gap between obstacles
INITIAL_OBSTACLE_SPEED = 5  # Initial speed of obstacles
SPEED_INCREMENT = 0.01  # Smaller speed increment after each score threshold
SCORE_THRESHOLD = 10  # Higher score threshold for increasing difficulty

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Samurai Jump")

# Load images
dino_stand_images = [pygame.transform.scale(pygame.image.load(f"dino_stand_{i}.png").convert_alpha(), (50, 50)) for i in range(1, 4)]
dino_jump_image = pygame.transform.scale(pygame.image.load("dino_jump.png").convert_alpha(), (50, 50))
obstacle_image = pygame.transform.scale(pygame.image.load("obstacle.png").convert_alpha(), (70, 70))
background_image = pygame.transform.scale(pygame.image.load("background.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
menu_background_image = pygame.transform.scale(pygame.image.load("menu_background.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))  # Load your menu background
game_over_background_image = pygame.transform.scale(pygame.image.load("game_over_background.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))  # Load your game over background

# Initialize font for score display and menu
font = pygame.font.Font(None, 36)

# Function to display the main menu
def draw_text_with_outline(text, font, color, outline_color, position):
    # Draw outline by rendering the text multiple times with offsets
    outline_offsets = [(1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
    for offset in outline_offsets:
        outline_position = (position[0] + offset[0], position[1] + offset[1])
        outline_text = font.render(text, True, outline_color)
        screen.blit(outline_text, outline_position)

    # Draw the main text on top
    main_text = font.render(text, True, color)
    screen.blit(main_text, position)

def show_menu():
    menu_running = True
    while menu_running:
        screen.blit(menu_background_image, (0, 0))  # Draw menu background
        
        title_text = "Samurai Jump"
        play_text = "Play"
        quit_text = "Quit"

        # Draw title with outline
        title_width, title_height = font.size(title_text)
        title_position = (SCREEN_WIDTH // 2 - title_width // 2, SCREEN_HEIGHT // 4 - title_height // 2)
        draw_text_with_outline(title_text, font, BLACK, WHITE, title_position)

        # Define button dimensions
        button_width = max(font.size(play_text)[0], font.size(quit_text)[0]) + 20
        button_height = font.size(play_text)[1] + 20
        button_spacing = 20  # Space between buttons

        play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - button_height // 2, button_width, button_height)
        quit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + button_height + button_spacing, button_width, button_height)

        # Draw buttons
        pygame.draw.rect(screen, WHITE, play_button_rect)  # Draw white rectangle for "Play" button
        pygame.draw.rect(screen, WHITE, quit_button_rect)  # Draw white rectangle for "Quit" button

        # Draw button text with outline
        play_text_width, play_text_height = font.size(play_text)
        play_text_position = (play_button_rect.x + (button_width - play_text_width) // 2, play_button_rect.y + (button_height - play_text_height) // 2)
        draw_text_with_outline(play_text, font, BLACK, WHITE, play_text_position)

        quit_text_width, quit_text_height = font.size(quit_text)
        quit_text_position = (quit_button_rect.x + (button_width - quit_text_width) // 2, quit_button_rect.y + (button_height - quit_text_height) // 2)
        draw_text_with_outline(quit_text, font, BLACK, WHITE, quit_text_position)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to play
                    menu_running = False
                if event.key == pygame.K_ESCAPE:  # Press Escape to quit
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if play_button_rect.collidepoint(mouse_x, mouse_y):  # Check if "Play" button is clicked
                    menu_running = False
                if quit_button_rect.collidepoint(mouse_x, mouse_y):  # Check if "Quit" button is clicked
                    pygame.quit()
                    quit()
                    
# Function to display the game over menu
def draw_text_with_outline(text, font, color, outline_color, position):
    # Draw outline by rendering the text multiple times with offsets
    outline_offsets = [(1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
    for offset in outline_offsets:
        outline_position = (position[0] + offset[0], position[1] + offset[1])
        outline_text = font.render(text, True, outline_color)
        screen.blit(outline_text, outline_position)

    # Draw the main text on top
    main_text = font.render(text, True, color)
    screen.blit(main_text, position)

def show_game_over(score):
    menu_running = True
    while menu_running:
        screen.blit(game_over_background_image, (0, 0))  # Draw game over background
        
        game_over_text = "Game Over"
        score_text = f"Score: {score}"
        play_again_text = "Play Again"
        quit_text = "Quit"

        # Draw texts with outline
        game_over_width, game_over_height = font.size(game_over_text)
        game_over_position = (SCREEN_WIDTH // 2 - game_over_width // 2, SCREEN_HEIGHT // 4 - game_over_height // 2)
        draw_text_with_outline(game_over_text, font, BLACK, WHITE, game_over_position)

        score_width, score_height = font.size(score_text)
        score_position = (SCREEN_WIDTH // 2 - score_width // 2, SCREEN_HEIGHT // 3 - score_height // 2)
        draw_text_with_outline(score_text, font, BLACK, WHITE, score_position)

        # Define button dimensions
        button_width = max(font.size(play_again_text)[0], font.size(quit_text)[0]) + 20
        button_height = font.size(play_again_text)[1] + 20
        button_spacing = 20  # Space between buttons

        play_again_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - button_height // 2, button_width, button_height)
        quit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + button_height + button_spacing, button_width, button_height)

        # Draw buttons
        pygame.draw.rect(screen, WHITE, play_again_button_rect)  # Draw white rectangle for "Play Again" button
        pygame.draw.rect(screen, WHITE, quit_button_rect)  # Draw white rectangle for "Quit" button

        # Draw button text with outline
        play_again_width, play_again_height = font.size(play_again_text)
        play_again_position = (play_again_button_rect.x + (button_width - play_again_width) // 2, play_again_button_rect.y + (button_height - play_again_height) // 2)
        draw_text_with_outline(play_again_text, font, BLACK, WHITE, play_again_position)

        quit_width, quit_height = font.size(quit_text)
        quit_position = (quit_button_rect.x + (button_width - quit_width) // 2, quit_button_rect.y + (button_height - quit_height) // 2)
        draw_text_with_outline(quit_text, font, BLACK, WHITE, quit_position)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to play again
                    menu_running = False
                    return True  # Restart the game
                if event.key == pygame.K_ESCAPE:  # Press Escape to quit
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if play_again_button_rect.collidepoint(mouse_x, mouse_y):  # Check if "Play Again" button is clicked
                    menu_running = False
                    return True  # Restart the game
                if quit_button_rect.collidepoint(mouse_x, mouse_y):  # Check if "Quit" button is clicked
                    pygame.quit()
                    quit()

    return False  # Quit the game

# Main game loop
def game_loop():
    global score
    dino_y = SCREEN_HEIGHT - 60
    dino_velocity = 0
    obstacles = []
    score = 0
    clock = pygame.time.Clock()
    running = True
    is_jumping = False
    last_obstacle_x = SCREEN_WIDTH
    obstacle_speed = INITIAL_OBSTACLE_SPEED

    # Background position
    background_x = 0

    # Animation variables
    frame_index = 0
    frame_delay = 5  # Delay between frames
    frame_count = 0

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping:
                    dino_velocity = -JUMP_STRENGTH
                    is_jumping = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not is_jumping:
                    dino_velocity = -JUMP_STRENGTH
                    is_jumping = True

        # Gravity logic
        if is_jumping:
            dino_velocity += GRAVITY  # Apply gravity to the jump
            dino_y += dino_velocity  # Update the dinosaur's position

            # Check if the dinosaur has landed
            if dino_y >= SCREEN_HEIGHT - 60:
                dino_y = SCREEN_HEIGHT - 60  # Reset to ground level
                dino_velocity = 0  # Reset velocity
                is_jumping = False  # Reset jump state

        # Update obstacles
        if len(obstacles) == 0 or (obstacles[-1][0] < SCREEN_WIDTH - OBSTACLE_GAP):
            obstacles.append([SCREEN_WIDTH, SCREEN_HEIGHT - 60])

        for obstacle in obstacles:
            obstacle[0] -= obstacle_speed  # Move obstacles at the current speed
            if obstacle[0] < 0:
                obstacles.remove(obstacle)
                score += 1

        # Increase difficulty based on score
        if score > 0 and score % SCORE_THRESHOLD == 0:
            obstacle_speed += SPEED_INCREMENT  # Increase obstacle speed

        # Collision detection
        for obstacle in obstacles:
            if (obstacle[0] < 70 and obstacle[0] > 0) and (dino_y >= SCREEN_HEIGHT - 60):
                running = False  # Game over

        # Update background position
        background_x -=  2  # Move the background to the left
        if background_x < -SCREEN_WIDTH:
            background_x = 0  # Reset background position

        # Draw everything
        screen.blit(background_image, (background_x, 0))  # Draw the background
        screen.blit(background_image, (background_x + SCREEN_WIDTH, 0))  # Draw the background again for seamless scrolling

        # Render score text
        score_text = font.render(f"Score: {score}", True, BLACK)  # Render the score text
        screen.blit(score_text, (10, 10))  # Draw the score text at the top-left corner

        # Animation logic
        frame_count += 1
        if frame_count >= frame_delay:
            frame_index = (frame_index + 1) % len(dino_stand_images)
            frame_count = 0

        if is_jumping:
            screen.blit(dino_jump_image, (50, dino_y))  # Draw the jumping dinosaur
        else:
            screen.blit(dino_stand_images[frame_index], (50, dino_y))  # Draw the standing dinosaur

        for obstacle in obstacles:
            screen.blit(obstacle_image, obstacle)  # Draw obstacles

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

    # Show game over menu
    return show_game_over(score)

# Main game loop
def main():
    while True:
        show_menu()
        if not game_loop():
            break

if __name__ == "__main__":
    main()
