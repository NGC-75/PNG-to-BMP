import pygame
import sys
from tkinter import Tk, filedialog
from PIL import Image
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((700, 450))
pygame.display.set_caption("BMP Bit Depth Converter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 24)

# Input box and buttons
input_box = pygame.Rect(150, 100, 300, 40)
button_browse_input = pygame.Rect(150, 170, 300, 40)
button_browse_output = pygame.Rect(150, 240, 300, 40)
button_convert = pygame.Rect(150, 310, 300, 40)

# Variables
input_text = ""
file_path = ""
output_dir = ""
bit_depth = None
input_active = False
cursor_visible = True
cursor_timer = 0
convert_success = False

# Function to reduce color depth
def reduce_color_depth(image, bit_depth):
    """
    Reduces the color depth of an image to the specified bit depth.
    """
    if bit_depth >= 24:
        return image.convert("RGB")

    # Convert image to RGB if it's not already
    image = image.convert("RGB")

    # Calculate the number of colors for the given bit depth
    num_colors = 2 ** bit_depth

    # Quantize the image to the specified number of colors
    return image.quantize(colors=num_colors).convert("RGB")

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)

    # Draw labels
    bit_depth_label = font.render("Enter Bit Depth (1-32):", True, BLACK)
    screen.blit(bit_depth_label, (150, 60))

    input_file_label = font.render("Input File:", True, BLACK)
    screen.blit(input_file_label, (150, 140))

    output_dir_label = font.render("Output Directory:", True, BLACK)
    screen.blit(output_dir_label, (150, 210))

    # Draw input box
    pygame.draw.rect(screen, GRAY, input_box)
    pygame.draw.rect(screen, BLUE if input_active else BLACK, input_box, 2)

    # Draw blinking cursor
    if input_active and cursor_visible:
        cursor_x = input_box.x + 10 + font.size(input_text)[0]
        pygame.draw.line(screen, BLACK, (cursor_x, input_box.y + 5), (cursor_x, input_box.y + 35), 2)

    # Draw buttons
    pygame.draw.rect(screen, GRAY, button_browse_input)
    pygame.draw.rect(screen, BLACK, button_browse_input, 2)
    pygame.draw.rect(screen, GRAY, button_browse_output)
    pygame.draw.rect(screen, BLACK, button_browse_output, 2)
    pygame.draw.rect(screen, GREEN if convert_success else GRAY, button_convert)
    pygame.draw.rect(screen, BLACK, button_convert, 2)

    # Draw text
    text_surface = font.render(input_text, True, BLACK)
    screen.blit(text_surface, (input_box.x + 10, input_box.y + 5))

    browse_input_text = font.render("Browse Input File", True, BLACK)
    screen.blit(browse_input_text, (button_browse_input.x + 50, button_browse_input.y + 5))

    browse_output_text = font.render("Choose Output Directory", True, BLACK)
    screen.blit(browse_output_text, (button_browse_output.x + 20, button_browse_output.y + 5))

    convert_text = font.render("Convert", True, BLACK)
    screen.blit(convert_text, (button_convert.x + 100, button_convert.y + 5))

    # Draw selected file and output directory
    if file_path:
        file_path_text = small_font.render(f"Selected: {file_path}", True, BLACK)
        screen.blit(file_path_text, (470, 180))
    if output_dir:
        output_dir_text = small_font.render(f"Selected: {output_dir}", True, BLACK)
        screen.blit(output_dir_text, (470, 250))

    # Draw success message
    if convert_success:
        success_text = font.render("Conversion Successful!", True, GREEN)
        screen.blit(success_text, (150, 370))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if input_box.collidepoint(mouse_pos):
                input_active = True
            else:
                input_active = False

            if button_browse_input.collidepoint(mouse_pos):
                # Open file dialog for input file
                Tk().withdraw()
                file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
                print(f"Selected input file: {file_path}")
            elif button_browse_output.collidepoint(mouse_pos):
                # Open file dialog for output directory
                Tk().withdraw()
                output_dir = filedialog.askdirectory()
                print(f"Selected output directory: {output_dir}")
            elif button_convert.collidepoint(mouse_pos):
                # Convert the image
                if file_path and output_dir and input_text.isdigit():
                    bit_depth = int(input_text)
                    if bit_depth < 1 or bit_depth > 32:
                        print("Bit depth must be between 1 and 32.")
                    else:
                        try:
                            # Load the image
                            image = Image.open(file_path)

                            # Reduce color depth
                            image = reduce_color_depth(image, bit_depth)

                            # Save the BMP file
                            output_filename = f"{output_dir}/output_{bit_depth}bit.bmp"
                            image.save(output_filename)
                            print(f"Image saved as {output_filename}")
                            convert_success = True
                        except Exception as e:
                            print(f"Error: {e}")
                            convert_success = False
        if event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    # Cursor blinking logic
    cursor_timer += clock.get_time()
    if cursor_timer >= 500:  # Toggle cursor every 500ms
        cursor_visible = not cursor_visible
        cursor_timer = 0

    pygame.display.flip()
    clock.tick(30)

# Quit Pygame
pygame.quit()