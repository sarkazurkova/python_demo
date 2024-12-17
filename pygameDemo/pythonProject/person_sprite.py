import pygame

class PersonSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('media/sprite-person.png').convert_alpha()
        self.frame_size = 64
        self.diretcions = ["down", "left", "right", "up"]
        self.frames = self.load_frames()
        self.image = self.frames["down"][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_index = 0;
        self.animation_speed = 0.1
        self.animation_counter = 0
        self.speed = 5
        self.is_active = False
        self.current_direction = "down"

    def load_frames(self):
        frames = {direction: [] for direction in self.diretcions}

        for i, direction in enumerate(self.diretcions):
            for j in range(4):
                frame = self.sprite_sheet.subsurface(
                    pygame.Rect(j * self.frame_size, i * self.frame_size, self.frame_size, self.frame_size)
                )
                frames[direction].append(frame)

        return frames

    def animate(self):
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.animation_index = (self.animation_index + 1) % len(self.frames[self.current_direction])
            self.image = self.frames[self.current_direction][self.animation_index]

    def update(self, keys, walls):
        '''Aktualizace postavy (pohyb + animace)'''
        if not self.is_active:  # Neaktivní postava se neaktualizuje
            return
        dx, dy = 0, 0
        direction = None

        if keys[pygame.K_LEFT]:
            dx = -self.speed
            direction = "left"
        if keys[pygame.K_RIGHT]:
            dx = self.speed
            direction = "right"
        if keys[pygame.K_UP]:
            dy = -self.speed
            direction = "up"
        if keys[pygame.K_DOWN]:
            dy = self.speed
            direction = "down"

        new_rect = self.rect.move(dx, dy)

        if not any(new_rect.colliderect(wall.rect) for wall in walls):
            self.rect = new_rect

        if direction:
            self.current_direction = direction
            self.animate()
        else:
            self.animation_index = 0
            self.image = self.frames[self.current_direction][0]