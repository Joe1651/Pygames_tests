import pygame
import pygame_gui
from tuile import Tuile

class Circulab():
    def __init__(self, height: int = 720, width: int = 1280):
        # Setup Window
        pygame.init()
        pygame.display.set_caption('CircuLab')

        # Load Images
        self.logo = pygame.image.load("logo.png")

        # Load Fonts
        self.font = pygame.font.Font("freesansbold.ttf", 32)

        # Color palette
        self.BLACK = "#040f0f"
        self.DARK_GREEN = "#248232"
        self.GREEN = "#2ba84a"
        self.GREY = "#2d3a3a"
        self.WHITE = "#fcfffc"
        self.BLUE_GREY = "#77a6b6"

        # Taille de la fenêtre
        self.HEIGHT = height
        self.WIDTH = width
        self.TOOL_BAR_HEIGHT = self.HEIGHT * 1/8
        self.TOOL_BAR_WIDTH = self.WIDTH * 3/4
        self.TOOL_BAR_BTN_SIZE = 78
        
        # Transform Images
        self.logo = pygame.transform.scale(self.logo, (self.WIDTH - self.TOOL_BAR_WIDTH, self.TOOL_BAR_HEIGHT + 10))

        # Surface de la fenêtre
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # GUI Manager
        self.manager = pygame_gui.UIManager((self.WIDTH, self.HEIGHT), theme_path="styles_real.json")

        # Dessiner les éléments du GUI
        self.tool_bar_btns = pygame.sprite.Group()
        self.draw_top_UI()
        self.draw_button_tool_bar()

        # Horloge (pour les FPS)
        self.clock = pygame.time.Clock()

        # Variable de jeu
        self.ROWS = 150
        self.COLUMNS = 150
        self.TILE_SIZE = 64
        self.scrollx = (self.COLUMNS * self.TILE_SIZE) / 2  # Set le scroll x au milieu
        self.scrolly = (self.ROWS * self.TILE_SIZE) / 2  # Set le scroll y au milieu
        self.scroll_speed = 1
        self.vertical_scroll = 0
        self.horizontal_scroll = 0
        self.running = True
    
    def run(self):
        while self.running:
            # FPS Capping
            time_delta = self.clock.tick(60)/1000

            #scroll la grip
            if self.horizontal_scroll == 1 and self.scrollx < (self.COLUMNS * self.TILE_SIZE) - self.WIDTH:
                self.scrollx += 5 * self.scroll_speed
            elif self.horizontal_scroll == -1 and self.scrollx > 0:
                self.scrollx -= 5 * self.scroll_speed
            
            if self.vertical_scroll == 1 and self.scrolly < (self.ROWS * self.TILE_SIZE) - self.HEIGHT:  # Descend l'écran
                self.scrolly += 5 * self.scroll_speed
            elif self.vertical_scroll == -1 and self.scrolly > 0:  # Monte l'écran
                self.scrolly -= 5 * self.scroll_speed

            #get mouse position
            pos = pygame.mouse.get_pos()
            x = (pos[0] + self.scrollx) // self.TILE_SIZE
            y = (pos[1] + self.scrolly) // self.TILE_SIZE
            print(f"({x} | {y})")

            # Vérifie si le joueur clique sur le "X"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element in self.tool_bar_btns:
                    btn = event.ui_element
                    if not btn.is_selected:
                        self.unselect_all_btns()
                        btn.select()
                        continue
                    elif btn.is_selected:
                        btn.unselect()
                        continue
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.horizontal_scroll = -1
                    if event.key == pygame.K_RIGHT:
                        self.horizontal_scroll = 1
                    if event.key == pygame.K_UP:
                        self.vertical_scroll = -1
                    if event.key == pygame.K_DOWN:
                        self.vertical_scroll = 1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.horizontal_scroll = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.vertical_scroll = 0

                self.manager.process_events(event)

            # Remplit le fond de couleur verte
            self.screen.fill(self.GREY)
            pygame.draw.rect(self.screen, self.BLUE_GREY, (x * self.TILE_SIZE - self.scrollx, y * self.TILE_SIZE - self.scrolly, self.TILE_SIZE, self.TILE_SIZE))
            self.draw_text(f"X: {int(x)} | Y: {int(y)}", self.font, self.WHITE, pos[0], pos[1]-self.TILE_SIZE/2)
            self.draw_grid()

            # Affiche le logo
            self.screen.blit(self.logo, (0, 0))    

            # Update l'écran
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()
    
        pygame.quit()
    
    def draw_top_UI(self):
        self.tool_bar_window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((self.WIDTH - self.TOOL_BAR_WIDTH, 0), (self.TOOL_BAR_WIDTH, self.TOOL_BAR_HEIGHT)), 
            object_id="#tool_bar_window", 
            manager=self.manager)
        
        self.tool_bar_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0, 0), (self.TOOL_BAR_WIDTH, self.TOOL_BAR_HEIGHT)), 
                                                                           manager=self.manager, 
                                                                           container=self.tool_bar_window, 
                                                                           object_id="#tool_bar_container",
                                                                           allow_scroll_y=True)
    
    def draw_button_tool_bar(self):
        for i in range(9):
            new_btn = pygame_gui.elements.UIButton(
                        relative_rect=pygame.Rect(((3/2 * i * self.TOOL_BAR_BTN_SIZE) + self.TOOL_BAR_BTN_SIZE/2 , 0), (self.TOOL_BAR_BTN_SIZE, self.TOOL_BAR_BTN_SIZE)),
                        text="",
                        manager=self.manager,
                        anchors={"centery": "centery"},
                        container=self.tool_bar_container,
                        object_id=pygame_gui.core.ObjectID(class_id="@tool_tip_btn", object_id=f"#tool_tip_btn_{i + 1}"))
            
            self.tool_bar_btns.add(new_btn)
    
    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        img_rect = img.get_rect()
        img_rect.center = (x, y)
        self.screen.blit(img, img_rect)

    def unselect_all_btns(self):
        for btn in self.tool_bar_btns:
            btn.unselect()

    def draw_grid(self):
        for c in range(self.COLUMNS + 1):
            pygame.draw.line(self.screen, self.WHITE, (c * self.TILE_SIZE - self.scrollx, 0), (c * self.TILE_SIZE - self.scrollx, self.HEIGHT))
        for c in range(self.ROWS + 1):
            pygame.draw.line(self.screen, self.WHITE, (0, c * self.TILE_SIZE - self.scrolly), (self.WIDTH, c * self.TILE_SIZE - self.scrolly))


game = Circulab()
game.run()