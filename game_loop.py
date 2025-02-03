import pygame
import pygame_gui

class Circulab():
    def __init__(self, height: int = 720, width: int = 1280):
        # Setup Window
        pygame.init()
        pygame.display.set_caption('CircuLab')

        # Load Images
        self.logo = pygame.image.load("logo.png")

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
        self.running = True
    
    def run(self):
        while self.running:
            # FPS Capping
            time_delta = self.clock.tick(60)/1000

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

                self.manager.process_events(event)

            # Remplit le fond de couleur verte
            self.screen.fill(self.GREY)

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
    
    def unselect_all_btns(self):
        for btn in self.tool_bar_btns:
            btn.unselect()



game = Circulab()
game.run()