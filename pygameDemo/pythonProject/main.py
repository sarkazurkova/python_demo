import pygame

from custom_surface import CustomSurface
from wall import WallManager
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from person_sprite import PersonSprite


class App:
    '''Hlavní třída aplikace'''
    def __init__(self):
        '''Konstruktor - Inicializace hry'''
        pygame.init()   # Inicializace Pygame
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # Vytvoření okna
        pygame.display.set_caption("Pygame Demo")   # Název okna
        self.clock = pygame.time.Clock()    # Vytvoření hodin
        self.running = True     # Hra běží

        # Komponenty
        # Vytvoření vlastního Surface
        self.custom_surface = CustomSurface(SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0))
        self.walls = WallManager()
        self.person_sprites = pygame.sprite.Group()
        self.person_sprites_list = []  # Seznam všech postav pro přepínání
        self.add_person_sprites()  # Přidání postav
        self.active_person_index = 0  # Index aktivní postavy
        self.set_active_person(0)

    def add_person_sprites(self):
        '''Přidání postav do hry'''
        self.person_sprites_list.append(PersonSprite(100, 100))
        self.person_sprites_list.append(PersonSprite(400, 300))
        for person in self.person_sprites_list:
            self.person_sprites.add(person)

    def set_active_person(self, index):
        '''Nastaví aktivní postavu'''
        for i, person in enumerate(self.person_sprites_list):
            person.is_active = (i == index)

    def run(self):
        '''Hlavní smyčka hry'''
        while self.running:
            self.handle_events()    # Zpracování událostí
            self.update()   # Aktualizace stavu
            self.draw()    # Vykreslení prvků
            self.clock.tick(FPS)    # Případné čekání na další snímek - nastavení počtu snímků za sekundu
        pygame.quit()   # Ukončení Pygame

    def handle_events(self):
        '''Zpracování všech událostí v hlavní smyčce hry'''
        for event in pygame.event.get():   # Projít všechny události ve frontě
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Ukončení hry
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                self.active_person_index = (self.active_person_index + 1) % len(self.person_sprites_list)
                self.set_active_person(self.active_person_index)
                
            # Vytvoření nebo manipulace se zdmi
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Levé tlačítko myši
                    keys = pygame.key.get_pressed()
                    self.walls.start_dragging(event.pos, keys)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Levé tlačítko myši
                    self.walls.stop_dragging(event.pos)

            if event.type == pygame.MOUSEMOTION:
                self.walls.update_dragging(event.pos)

            # Odstranění zdi
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    self.walls.delete_active_wall()



    def update(self):
        '''Aktualizace herního stavu'''
        keys = pygame.key.get_pressed()
        self.person_sprites.update(keys, self.walls.get_walls())


    def draw(self):
        '''Vykreslení herních prvků'''
        self.screen.fill((0, 255, 255)) # Vyplnění obrazovky žlutou barvou
        self.custom_surface.draw(self.screen) # Vykreslení vlastního Surface
        self.walls.draw(self.screen)    # Vykreslení zdí
        self.person_sprites.draw(self.screen)  # Vykreslení všech postav
        pygame.display.flip() # Zobrazení vykreslených prvků



# Spuštění aplikace
if __name__ == "__main__":
    app = App()     # Vytvoření instance třídy App
    app.run()      # Spuštění hlavní smyčky hry