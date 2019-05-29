import pygame
from os import path
vec = pygame.math.Vector2

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 900
HEIGHT = 540
FPS = 60

# Player properties
PLAYER_VEL = 8
GROUND = HEIGHT - 70

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BGCOLOR = (200, 200, 200)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, GROUND)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        self.standing_frames = [self.resize(pygame.image.load(path.join(img_dir, "Idle__000.png")), 232, 439),
                                self.resize(pygame.image.load(path.join(img_dir, "Idle__001.png")), 232, 439),
                                self.resize(pygame.image.load(path.join(img_dir, "Idle__002.png")), 232, 439),
                                self.resize(pygame.image.load(path.join(img_dir, "Idle__003.png")), 232, 439),
                                self.resize(pygame.image.load(path.join(img_dir, "Idle__004.png")), 232, 439),
                                self.resize(pygame.image.load(path.join(img_dir, "Idle__005.png")), 232, 439),
                                self.resize(pygame.image.load(path.join(img_dir, "Idle__006.png")), 232, 439),
                                self.resize(pygame.image.load(path.join(img_dir, "Idle__007.png")), 232, 439),
                                self.resize(pygame.image.load(path.join(img_dir, "Idle__008.png")), 232, 439),
                                self.resize(pygame.image.load(path.join(img_dir, "Idle__009.png")), 232, 439)
                                ]


        self.walk_frames_r = [self.resize(pygame.image.load(path.join(img_dir, "Run__000.png")), 363, 458),
                              self.resize(pygame.image.load(path.join(img_dir, "Run__001.png")), 363, 458),
                              self.resize(pygame.image.load(path.join(img_dir, "Run__002.png")), 363, 458),
                              self.resize(pygame.image.load(path.join(img_dir, "Run__003.png")), 363, 458),
                              self.resize(pygame.image.load(path.join(img_dir, "Run__004.png")), 363, 458),
                              self.resize(pygame.image.load(path.join(img_dir, "Run__005.png")), 363, 458),
                              self.resize(pygame.image.load(path.join(img_dir, "Run__006.png")), 363, 458),
                              self.resize(pygame.image.load(path.join(img_dir, "Run__007.png")), 363, 458),
                              self.resize(pygame.image.load(path.join(img_dir, "Run__008.png")), 363, 458),
                              self.resize(pygame.image.load(path.join(img_dir, "Run__009.png")), 363, 458)]

        self.jump_frame = [self.resize(pygame.image.load(path.join(img_dir, "Jump__009.png")), 362, 483)]
        self.jump_frame_l = []
        for frame in self.jump_frame:
            self.jump_frame_l.append(pygame.transform.flip(frame, True, False))

        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            self.walk_frames_l.append(pygame.transform.flip(frame, True, False))

    def resize(self, image, width, height):
        image = pygame.transform.scale(image, (width // 4, height // 4))
        return image

    def jump(self):
        if self.pos.y == GROUND:
            self.vel.y = -15

    def update(self):
        self.animate()
        self.acc = vec(PLAYER_VEL, 0.8)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_VEL
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_VEL

        # equations of motion
        self.vel += self.acc
        self.pos.y += self.vel.y + 0.5 * self.acc.y
        self.pos.x += self.acc.x
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        if self.pos.y > HEIGHT - 70:
            self.pos.y = HEIGHT - 70
            self.vel.y = 0

        self.rect.midbottom = self.pos

    def animate(self):
        now = pygame.time.get_ticks()

        if self.vel.y != 0:
            self.jumping = True
        else:
            self.jumping = False

        # show jump frame
        if self.jumping:
            if now - self.last_update > 60:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jump_frame)
                bottom = self.rect.bottom
                if self.acc.x >= 0:
                    self.image = self.jump_frame[self.current_frame]
                else:
                    self.image = self.jump_frame_l[self.current_frame]

                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.acc.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking:
            if now - self.last_update > 60:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.acc.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]

                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # Show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # Update
    all_sprites.update()

    # Draw / render
    screen.fill(BGCOLOR)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
