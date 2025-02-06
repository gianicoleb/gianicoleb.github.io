import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Energy Matching Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
GREEN = (34, 139, 34)  # Correct match
RED = (200, 50, 50)  # Incorrect match
LINE_COLOR = (0, 0, 0)  # Default black lines

# Font
FONT = pygame.font.Font(None, 30)

# Energy Consumption Data
appliances = {
    "Central AC": "3000-3500 watts per hour",
    "Window AC": "1000-1500 watts per hour",
    "Dishwasher": "1400 watts per hour",
    "Electric Blanket": "200 watts per hour",
    "Computer": "80 watts per hour",
    "TV": "200-700 watts per hour",
    "Central Heating": "10,000-50,000 watts per hour",
    "Portable Electric Heater": "750-1500 watts per hour",
    "LED Lightbulb": "2-18 watts per hour",
    "Incandescent Light Bulb": "25-100 watts per hour",
    "10-20 Gallon Water Heater": "1000-2000 watts per hour",
    "30-80 Gallon Water Heater": "4500 watts per hour",
    "Dehumidifier": "390 watts per hour",
    "Air Purifier": "250 watts per hour",
    "Vacuum Cleaner": "630 watts per hour",
    "Oven": "2000-3000 watts per hour",
    "Electric Stove": "1000-3000 watts per hour",
    "Electric Car per Mile": "200-400 watts",
    "Electric Car at 60mph": "15,000-24,000 watts per hour",
    "100 ChatGPT or Google AI Searches": "300 watts",
    "100 Google Searches": "30 watts"
}

# Shuffle appliance names and energy values separately
appliance_names = list(appliances.keys())
energy_values = list(appliances.values())
random.shuffle(energy_values)  # Shuffle energy values for mismatched display

# Create button positions
appliance_positions = [pygame.Rect(50, 50 + i * 30, 350, 40) for i in range(len(appliance_names))]
energy_positions = [pygame.Rect(500, 50 + i * 30, 350, 40) for i in range(len(energy_values))]

# Game variables
dragging = None  # Stores index of item being dragged
offset_x, offset_y = 0, 0  # Mouse offset for dragging
matched_pairs = {}  # Stores correct matches (appliance index → energy index)
incorrect_pairs = {}  # Stores incorrect matches (appliance index → correct energy index)
score = 0

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Draw title
    title_text = FONT.render("Drag the Appliance to its Energy Usage!", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 10))

    # Draw energy usage labels
    for i in range(len(energy_values)):
        pygame.draw.rect(screen, GREEN if i in matched_pairs.values() else RED, energy_positions[i])
        energy_text = FONT.render(energy_values[i], True, WHITE)
        screen.blit(energy_text, (energy_positions[i].x + 10, energy_positions[i].y + 10))

    # Draw appliances
    for i in range(len(appliance_names)):
        pygame.draw.rect(screen, BLUE, appliance_positions[i])
        appliance_text = FONT.render(appliance_names[i], True, WHITE)
        screen.blit(appliance_text, (appliance_positions[i].x + 10, appliance_positions[i].y + 10))

    # Draw the dragged item on top
    if dragging is not None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rect = pygame.Rect(mouse_x + offset_x, mouse_y + offset_y, 350, 40)
        pygame.draw.rect(screen, BLUE, rect)
        text = FONT.render(appliance_names[dragging], True, WHITE)
        screen.blit(text, (rect.x + 10, rect.y + 10))

    # Draw lines for matched pairs
    for appliance_idx, energy_idx in matched_pairs.items():
        appliance_rect = appliance_positions[appliance_idx]
        energy_rect = energy_positions[energy_idx]
        pygame.draw.line(screen, GREEN, (appliance_rect.right, appliance_rect.centery),
                         (energy_rect.left, energy_rect.centery), 3)

    # Draw red lines for incorrect pairs
    for appliance_idx, correct_energy_idx in incorrect_pairs.items():
        appliance_rect = appliance_positions[appliance_idx]
        energy_rect = energy_positions[correct_energy_idx]
        pygame.draw.line(screen, RED, (appliance_rect.right, appliance_rect.centery),
                         (energy_rect.left, energy_rect.centery), 3)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Check if an appliance is clicked
            for i, button in enumerate(appliance_positions):
                if button.collidepoint(mouse_x, mouse_y) and i not in matched_pairs:
                    dragging = i
                    offset_x = button.x - mouse_x
                    offset_y = button.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging is not None:
                mouse_x, mouse_y = event.pos

                # Check if dropped onto a valid energy slot
                for j, button in enumerate(energy_positions):
                    if button.collidepoint(mouse_x, mouse_y):
                        selected_appliance = appliance_names[dragging]
                        selected_energy = energy_values[j]

                        # Check if match is correct
                        if appliances[selected_appliance] == selected_energy:
                            matched_pairs[dragging] = j  # Store correct match
                            score += 1
                        else:
                            # Find the correct energy index for the incorrect match
                            correct_energy_idx = energy_values.index(appliances[selected_appliance])
                            incorrect_pairs[dragging] = correct_energy_idx  # Store incorrect match
                            print(f"❌ Incorrect: {selected_appliance} does not match {selected_energy}.")

                dragging = None  # Reset dragging

    # Check if game is won
    if len(matched_pairs) == len(appliances):
        win_text = FONT.render(f"🎉 You matched all pairs! Score: {score} 🎉", True, BLACK)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT - 50))

    pygame.display.flip()

pygame.quit()
