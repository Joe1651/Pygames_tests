import pygame
import pygame_gui
from pygame_gui.elements import *
import pygame_gui.elements.ui_2d_slider
from pygame_gui.windows import *

pygame.init()

pygame.display.set_caption('Quick Start')

HEIGHT = 720
WIDTH = 1280

# Fenêtre et manager
window_surface = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.Surface((WIDTH, HEIGHT))
background.fill(pygame.Color('green'))

# Charger le style du fichier JSON
manager = pygame_gui.UIManager((WIDTH, HEIGHT), "styles.json")

logo_img = pygame.image.load("road.png")

# Test des différents éléments 
hello_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((0, 0), (logo_img.get_width() + 20, logo_img.get_height() + 20)),
    text="",  # On ne met pas de texte pour ne voir que l'image
    manager=manager,
    object_id=pygame_gui.core.ObjectID(class_id="@build_tiles"),  # Doit correspondre à l'ID dans styles.json
    # anchors={"center": "center"},
    tool_tip_text="Routes - Peuvent être tournées avec la touche [R]"
)

file_window = UIFileDialog(
    rect=pygame.Rect((700, 0), (300, 300)),
    manager=manager,
    window_title="File Picker",
    initial_file_path="../",
    visible=True
)

window = UIWindow(
    rect=pygame.Rect((800, 400), (200, 200)),
    manager=manager,
    window_display_title="Custom Window :)",
    object_id="#Custom_Window"
)

container = UIAutoResizingContainer(
    relative_rect=pygame.Rect((0, 0), (200, 125)),
    manager=manager,
    container=window
)

text_box_slider = UITextBox(
    relative_rect=pygame.Rect((0, 0), (container.get_relative_rect().width, 100)),
    html_text=f"Current slider value: 0",
    manager=manager,
    container=container
)


slider_2d = UI2DSlider(
    relative_rect=pygame.Rect((0, text_box_slider.get_relative_rect().height), (text_box_slider.get_relative_rect().width, 25)),
    start_value_x=0,
    value_range_x=(0, 10),
    start_value_y=0,
    value_range_y=(0, 0),
    manager=manager,
    starting_height=0,
    container=container
)

text_box_slider.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)

# Game Logic
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # Vérifier si le bouton est cliqué
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == hello_button:
            print("Bouton cliqué !")
            if not hello_button.is_selected:
                hello_button.select()
                print("Selected")
                continue
            if hello_button.is_selected:
                hello_button.unselect()
                print("Unselected")
                continue
        
        if slider_2d.grabbed_slider:
            text_box_slider.set_text(f"Current slider value: {slider_2d.current_x_value}")

        manager.process_events(event)

    manager.update(time_delta)

    # Affichage
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    pygame.display.update()

pygame.quit()
