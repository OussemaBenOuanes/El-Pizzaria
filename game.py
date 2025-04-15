import pygame
import sys
import os

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


def game_screen(screen, WIDTH, HEIGHT):
    """Display the game screen with the kitchen background, animated images, and scrollable items."""
    # Load and scale the kitchen image
    kitchen_img = pygame.image.load("Assets/kitchen.png")
    kitchen_width, kitchen_height = kitchen_img.get_size()
    if kitchen_width > WIDTH or kitchen_height > HEIGHT:
        kitchen_img = pygame.transform.scale(kitchen_img, (WIDTH, HEIGHT))
    kitchen_rect = kitchen_img.get_rect()
    kitchen_rect.center = (WIDTH // 2, HEIGHT // 2)

    # Load the Empty Pizza image
    try:
        pizza_img = pygame.image.load("Assets/Pizza/Empty Pizza.png")
    except pygame.error as e:
        print(f"Error loading Empty Pizza image: {e}")
        sys.exit()
    pizza_width, pizza_height = pizza_img.get_size()
    pizza_img = pygame.transform.scale(pizza_img, (int(pizza_width * 0.2), int(pizza_height * 0.2)))  # Adjust scale
    pizza_rect = pizza_img.get_rect()
    pizza_rect.center = (WIDTH // 1, HEIGHT // 2)  # Center the pizza on the screen

    # Load the Menu image
    try:
        menu_img = pygame.image.load("Assets/Menu.png")
    except pygame.error as e:
        print(f"Error loading Menu image: {e}")
        sys.exit()
    menu_width, menu_height = menu_img.get_size()
    scaled_menu_width = int(menu_width * (550 / menu_height))  # Scale width to maintain aspect ratio
    menu_img = pygame.transform.scale(menu_img, (scaled_menu_width, 550))  # Scale height to 550
    menu_rect = menu_img.get_rect()
    menu_rect.topleft = (0, 0)  # Ensure it sticks to the top-left corner

    # Load the items (ingredients) from the Assets/Items folder
    items_folder = "Assets/Items"
    items_images = []
    fixed_item_height = 110  # Set a larger fixed height for all items
    try:
        for item_file in os.listdir(items_folder):
            item_path = os.path.join(items_folder, item_file)
            item_img = pygame.image.load(item_path)
            item_width, item_height = item_img.get_size()
            scaled_item_width = int(item_width * (fixed_item_height / item_height))  # Scale width to maintain aspect ratio
            scaled_item_img = pygame.transform.scale(item_img, (scaled_item_width, fixed_item_height))  # Set fixed height
            items_images.append(scaled_item_img)
    except FileNotFoundError as e:
        print(f"Error loading items: {e}")
        sys.exit()

    # Set up scrolling for the items
    scroll_y = 0  # Initial scroll position
    scroll_speed = 5  # Speed of scrolling
    item_spacing = 20  # Space between items for better styling
    items_rects = []  # Store rects for positioning

    # Calculate positions for items
    for i, item_img in enumerate(items_images):
        item_rect = item_img.get_rect()
        item_rect.centerx = menu_rect.width // 2  # Center horizontally within the menu
        item_rect.y = scroll_y + i * (item_rect.height + item_spacing)
        items_rects.append(item_rect)

    # Animation speeds
    pizza_speed = -1  # Move left
    menu_speed = 0  # Move right

    # Store added ingredients on the pizza with their positions
    added_ingredients = {}

    # Define positions for ingredients on the pizza
    ingredient_positions = [
        (-30, -30), (30, -30), (-30, 30), (30, 30),  # Four corners around the center
        (0, -50), (0, 50), (-50, 0), (50, 0)         # Top, bottom, left, right
    ]
    used_positions = []  # Track used positions to avoid overlap

    # Load the check button image
    check_button_img = pygame.image.load("Assets/check.png")
    check_button_width, check_button_height = check_button_img.get_size()
    scaled_check_button_img = pygame.transform.scale(
        check_button_img, (int(check_button_width * 0.4), int(check_button_height * 0.4))  # Make it smaller
    )
    check_button_rect = scaled_check_button_img.get_rect()
    check_button_rect.topleft = (menu_rect.right + 30, HEIGHT // 2 - check_button_height // 3)  # Add margin from the menu

    # Load the mcha image for the popup
    mcha_img = pygame.image.load("Assets/mcha.png")
    mcha_width, mcha_height = mcha_img.get_size()
    scaled_mcha_width = int(mcha_width * (550 / mcha_height))  # Scale width to maintain aspect ratio
    scaled_mcha_img = pygame.transform.scale(
        mcha_img, (scaled_mcha_width, 550)  # Set height to 550 while maintaining aspect ratio
    )
    mcha_rect = scaled_mcha_img.get_rect()
    mcha_rect.center = (WIDTH // 2, HEIGHT // 2)  # Center the popup on the screen

    # Function to blur the screen
    def blur_surface(surface, amount):
        """Apply a blur effect to the given surface."""
        scale = 1 / amount
        small_surface = pygame.transform.smoothscale(surface, (int(WIDTH * scale), int(HEIGHT * scale)))
        return pygame.transform.smoothscale(small_surface, (WIDTH, HEIGHT))

    # Main loop
    running = True
    show_popup = False  # Flag to show the popup
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    if items_rects[0].top < menu_rect.top:
                        scroll_y += scroll_speed
                elif event.button == 5:  # Scroll down
                    if items_rects[-1].bottom + item_spacing > menu_rect.bottom:
                        scroll_y -= scroll_speed
                # Check if an item is clicked
                for i, item_rect in enumerate(items_rects):
                    if item_rect.collidepoint(event.pos):
                        # Get the corresponding ingredient image from Assets/Pizza
                        item_name = os.listdir(items_folder)[i]  # Get the item file name
                        ingredient_path = os.path.join("Assets/Pizza", item_name)
                        if os.path.exists(ingredient_path) and item_name not in added_ingredients:
                            if len(added_ingredients) < 5:  # Limit to 5 unique items
                                ingredient_img = pygame.image.load(ingredient_path)
                                ingredient_width, ingredient_height = ingredient_img.get_size()
                                scaled_ingredient_img = pygame.transform.scale(
                                    ingredient_img, (int(ingredient_width * 0.1), int(ingredient_height * 0.1))
                                )  # Scale to match pizza size
                                added_ingredients[item_name] = scaled_ingredient_img  # Add unique ingredient

                # Check if the check button is clicked
                if check_button_rect.collidepoint(event.pos) and added_ingredients:
                    show_popup = True  # Show the popup

        # Update item positions based on scroll_y
        for i, item_rect in enumerate(items_rects):
            item_rect.centerx = menu_rect.width // 2  # Keep centered horizontally
            item_rect.y = scroll_y + i * (item_rect.height + item_spacing)

        # Animate the Empty Pizza image (move from right to stop at 50 pixels horizontally)
        if pizza_rect.right > 870:
            pizza_rect.x += pizza_speed

        # Animate the Menu image (move from left to center)
        if menu_rect.left < WIDTH // 2 - menu_rect.width // 2:
            menu_rect.x += menu_speed

        # Draw the kitchen background
        screen.fill((255, 255, 255))  # Background color
        screen.blit(kitchen_img, kitchen_rect)

        # Draw the animated images
        screen.blit(pizza_img, pizza_rect)
        screen.blit(menu_img, menu_rect)

        # Draw the items (ingredients) centered and styled
        for i, item_img in enumerate(items_images):
            item_rect = items_rects[i]
            if menu_rect.top <= item_rect.bottom <= menu_rect.bottom:  # Only draw items visible in the menu
                screen.blit(item_img, (menu_rect.x + item_rect.x, item_rect.y))

        # Draw the added ingredients on the pizza
        for ingredient_img in added_ingredients.values():
            ingredient_width, ingredient_height = ingredient_img.get_size()
            scaled_ingredient_img = pygame.transform.scale(
                ingredient_img, (int(ingredient_width * 2), int(ingredient_height * 2))  # Make items larger
            )
            ingredient_x = pizza_rect.centerx - scaled_ingredient_img.get_width() // 2
            ingredient_y = pizza_rect.centery - scaled_ingredient_img.get_height() // 2
            screen.blit(scaled_ingredient_img, (ingredient_x, ingredient_y))

        # Draw the check button if there are added ingredients
        if added_ingredients:
            screen.blit(scaled_check_button_img, check_button_rect)

        # If the popup is active, blur the background and show the popup
        if show_popup:
            blurred_screen = blur_surface(screen, 10)  # Apply blur effect
            screen.blit(blurred_screen, (0, 0))  # Draw the blurred background
            screen.blit(scaled_mcha_img, mcha_rect)  # Draw the popup

        # Ensure proper spacing for the last items
        if len(items_rects) > 1:
            for i in range(len(items_rects) - 1):
                if items_rects[i].bottom > items_rects[i + 1].top:
                    items_rects[i + 1].top = items_rects[i].bottom + item_spacing

        # Update the display
        pygame.display.flip()