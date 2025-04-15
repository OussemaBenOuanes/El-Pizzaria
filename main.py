import pygame
import sys
import os  # To run game.py
from game import game_screen  # Import game_screen from game.py

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 900, 550

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EL PIZZARIA")

# Load the application icon
icon = pygame.image.load("Assets/icon.png")
pygame.display.set_icon(icon)


def main_menu():
    # Load the home screen image
    home_screen_img = pygame.image.load("Assets/Home screen.png")

    # Scale the home screen image to have a height of 550 while maintaining its aspect ratio
    original_width, original_height = home_screen_img.get_size()
    new_width = int(original_width * (HEIGHT / original_height))  # Calculate new width to maintain aspect ratio
    home_screen_img = pygame.transform.scale(home_screen_img, (new_width, HEIGHT))

    # Get the rectangle of the scaled home screen image
    img_rect = home_screen_img.get_rect()

    # Center the home screen image on the screen
    img_rect.center = (WIDTH // 2, HEIGHT // 2)

    # Load the Pizzaria logo image
    logo_img = pygame.image.load("Assets/Pizzaria Logo.png")

    # Scale the logo image to make it smaller (e.g., 70% of its original size)
    logo_width, logo_height = logo_img.get_size()
    scaled_logo_width = int(logo_width * 0.7)  # Scale width to 70%
    scaled_logo_height = int(logo_height * 0.7)  # Scale height to 70%
    logo_img = pygame.transform.scale(logo_img, (scaled_logo_width, scaled_logo_height))

    # Get the rectangle of the scaled logo image
    logo_rect = logo_img.get_rect()

    # Center the logo image on the screen and move it 10 pixels higher
    logo_rect.center = (WIDTH // 2, (HEIGHT // 2) - 100)

    # Load the "إلعب" button image
    play_button_img = pygame.image.load("Assets/إلعب.png")

    # Scale the button image to 60% of its original size
    button_width, button_height = play_button_img.get_size()
    scaled_button_width = int(button_width * 0.6)  # Scale width to 60%
    scaled_button_height = int(button_height * 0.6)  # Scale height to 60%
    play_button_img = pygame.transform.scale(play_button_img, (scaled_button_width, scaled_button_height))

    # Get the rectangle of the button image
    play_button_rect = play_button_img.get_rect()

    # Position the button below the logo (80 pixels below)
    play_button_rect.center = (WIDTH // 2, logo_rect.bottom + 80)

    # Speed and direction for bouncing the home screen image
    speed_x = 0.5  # Horizontal movement speed (slow)
    last_reverse_time = 0  # Track the last time the direction was reversed

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Exit the game if the user closes the window
                pygame.quit()
                sys.exit()

            # Check for mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):  # If the button is clicked
                    running = False  # Exit the main menu loop

        # Check if the mouse is hovering over the button
        if play_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Change cursor to pointer
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Default cursor

        # Move the home screen image horizontally
        img_rect.x += speed_x

        # Get the current time in milliseconds
        current_time = pygame.time.get_ticks()

        # Reverse direction after 3 seconds when the home screen image hits the screen edges
        if (img_rect.right >= WIDTH or img_rect.left <= 0) and current_time - last_reverse_time >= 3000:
            speed_x = -speed_x  # Reverse direction
            last_reverse_time = current_time  # Update the last reverse time

        # Fill the screen with a background color
        screen.fill((255, 255, 255))

        # Draw the home screen image
        screen.blit(home_screen_img, img_rect)

        # Draw the logo image
        screen.blit(logo_img, logo_rect)

        # Draw the play button image
        screen.blit(play_button_img, play_button_rect)

        # Update the display to reflect changes
        pygame.display.flip()

    # Transition to the game screen
    game_screen(screen, WIDTH, HEIGHT)


# Start the main menu
main_menu()