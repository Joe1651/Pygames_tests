import pygame
import pygame_gui
from pygame_gui.elements import *
from pygame_gui.windows import *

pygame.init()

pygame.display.set_caption('Quick Start')

# Fenêtre et manager
window_surface = pygame.display.set_mode((800, 600))
background = pygame.Surface((800, 600))
background.fill(pygame.Color('green'))

# Charger le style du fichier JSON
manager = pygame_gui.UIManager((800, 600), "styles.json")

logo_img = pygame.image.load("road.png")

# Création du bouton avec un style défini dans styles.json
hello_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((0, 0), (logo_img.get_width() + 20, logo_img.get_height() + 20)),
    text="",  # On ne met pas de texte pour ne voir que l'image
    manager=manager,
    object_id=pygame_gui.core.ObjectID(class_id="@build_tiles"),  # Doit correspondre à l'ID dans styles.json
    anchors={"center": "center"},
    tool_tip_text="Routes - Peuvent être tournées avec la touche [R]"
)

file_window = UIFileDialog(
    rect=pygame.Rect((0, 0), (300, 300)),
    manager=manager,
    window_title="File Picker",
    initial_file_path="../",
    visible=True
)

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

        manager.process_events(event)

    manager.update(time_delta)

    # Affichage
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)
    pygame.display.update()

pygame.quit()
