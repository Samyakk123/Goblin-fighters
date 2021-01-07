import os
import sys
import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# constant variables
screen_width = 378
screen_height = 600
screen_number = 0
t = 0
score = 0
x = 1


# Class Game where pygame is inti
class Game:
    def __init__(self):
        self.done = False
        # setting screen size
        self.image = pygame.Surface((800, 600))
        self.image.fill((0, 255, 0))
        self.screen = pygame.display.set_mode(
            (screen_width, screen_height))

        # all_sprites is used to update and draw all sprites together.
        # Groups are used for collision detection
        self.all_sprites = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.mobs_group = pygame.sprite.Group()

        self.ship = Ship()
        self.all_sprites.add(self.ship)
        self.clock = pygame.time.Clock()

    def handle_events(self):
        keys = pygame.key.get_pressed()

        # Player is defined under class ship, speed of player when moving left and right
        if keys[pygame.K_LEFT]:
            if self.ship.rect.centerx > 20:
                self.ship.rect.centerx -= 5
            elif self.ship.rect.centerx < 40:
                self.ship.rect.centerx = self.ship.rect.centerx

        if keys[pygame.K_RIGHT]:
            if self.ship.rect.centerx < 362:
                self.ship.rect.centerx += 5
            elif self.ship.rect.centerx > 338:
                self.ship.rect.centerx = self.ship.rect.centerx

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(self.ship)

                # This is for collision with the goblin (if this line is removed it won't remove the goblin if collided)

                    self.bullet_group.add(bullet)

                # This is for the bullet to appear altogether
                    self.all_sprites.add(bullet)

                # spawning enemies, where x is the amount that can be spawned
                if score > 100:
                    x = 2
                else:
                    x = 1
                for i in range(x):
                    m = Enemy()
                    self.mobs_group.add(m)
                    self.all_sprites.add(m)

    def update(self):
        global hit_me
        global hitplayer
        global mob
        global screen_number
        self.all_sprites.update()
        # Collision detection between player and enemy
        hit_me = pygame.sprite.spritecollide(Ship(), self.mobs_group, True)
        if hit_me:
            screen_number = 4
        # Collision detection between bullet and enemy
        for Bullet in self.bullet_group:
            global score
            hit_list = pygame.sprite.spritecollide(Bullet, self.mobs_group, True)
            player = Ship()
            hitplayer = pygame.sprite.spritecollide(player, self.mobs_group, True)
            if hit_list:
                score = score + 1

            for mob in hit_list:
                self.bullet_group.remove(Bullet)
                self.all_sprites.remove(Bullet)

            if Bullet.rect.y < -10:
                self.bullet_group.remove(Bullet)
                self.all_sprites.remove(Bullet)

    # Draws the background
    def draw(self):
        self.background = pygame.image.load(os.path.join("background1.jpg"))
        # self.background = pygame.image.load("background1.jpg").convert_alpha()
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)  # Draw the contained sprites.
        instructions1 = font_title.render("Score: " + str(score), True, WHITE)
        self.screen.blit(instructions1, [270, 0])
        pygame.display.update()

    def starting_screen(self):
        global screen_number
        global font
        # Starting screen where user gets to click play to start game
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        mouse_pressed = pygame.mouse.get_pressed()[0]
        self.screen.blit(self.image, (0, 0))
        title = font_title3.render("Goblin Fighter", True, BLACK)
        self.screen.blit(title, [0, 100])
        pygame.draw.rect(self.screen, BLACK, [125, 200, 85, 35], 2)
        difficulty = font_title.render("Play", True, BLACK)
        self.screen.blit(difficulty, [150, 200])
        # ------------------------------------------------------------------------------------
        pygame.draw.rect(self.screen, BLACK, [85, 300, 172, 35], 2)
        instructions = font_title.render("Instructions", True, BLACK)
        self.screen.blit(instructions, [110, 300])
        # ---------------------------------------------------------------------------------------
        # For music, player can choose to hear it or not hear it
        pygame.draw.rect(self.screen, BLACK, [85, 400, 165, 35], 2)
        instructions = font_title.render("Music", True, BLACK)
        self.screen.blit(instructions, [135, 400])
        if (125 < mouseX < 125 + 85) and (200 < mouseY < 200 + 35) and mouse_pressed == 1:
            pygame.time.delay(300)
            screen_number = 1
            pygame.display.flip()
        elif (85 < mouseX < 85 + 172) and (300 < mouseY < 300 + 35) and mouse_pressed == 1:
            pygame.time.delay(300)
            screen_number = 2

        elif (85 < mouseX < 85 + 165) and (400 < mouseY < 400 + 35) and mouse_pressed == 1:
            pygame.time.delay(300)
            screen_number = 3

    def instructions(self):
        global screen_number
        # Introduction screen where player gets to know the game better
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        mouse_pressed = pygame.mouse.get_pressed()[0]
        self.screen.blit(self.image, (0, 0))
        instructions1 = font_title2.render("To move left you hit the left arrow key", True, BLACK)
        self.screen.blit(instructions1, [0, 0])
        instructions1 = font_title.render("<--", True, RED)
        self.screen.blit(instructions1, [150, 30])

        instructions1 = font_title2.render("To move right you hit the right arrow key", True, BLACK)
        self.screen.blit(instructions1, [0, 60])
        instructions1 = font_title.render("-->", True, RED)
        self.screen.blit(instructions1, [150, 90])

        instructions1 = font_title2.render("To shoot a laser, press spacebar", True, BLACK)
        self.screen.blit(instructions1, [0, 120])
        x = pygame.image.load(os.path.join("bulletEnlarge.png"))
        # x = pygame.image.load("bulletEnlarge.png").convert()
        x.set_colorkey(BLACK)
        self.screen.blit(x, [80, 150])

        instructions1 = font_title2.render("Avoid hitting the goblins!", True, BLACK)
        self.screen.blit(instructions1, [0, 240])
        x = pygame.image.load(os.path.join("monster1.png"))
        # x = pygame.image.load("monster1.png").convert()
        x.set_colorkey(BLACK)
        self.screen.blit(x, [100, 270])

        instructions1 = font_title2.render("Character is randomized to either: ", True, BLACK)
        self.screen.blit(instructions1, [0, 425])
        x = pygame.image.load(os.path.join("dhrumik.png")).convert()
        # x = pygame.image.load("dhrumik.png").convert()
        x.set_colorkey(WHITE)
        self.screen.blit(x, [0, 450])
        x = pygame.image.load(os.path.join("samyak.png")).convert()
        # x = pygame.image.load("samyak.png").convert()
        x.set_colorkey(WHITE)
        self.screen.blit(x, [100, 450])

        pygame.draw.rect(self.screen, WHITE, [278, 550, 100, 50])
        instructions1 = font_title.render("Menu", True, BLACK)
        self.screen.blit(instructions1, [300, 560])

        if (278 < mouseX < 278 + 100) and (550 < mouseY < 550 + 50) and mouse_pressed == 1:
            screen_number = 0

    def screen3_music(self):
        global screen_number
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        mouse_pressed = pygame.mouse.get_pressed()[0]
        self.screen.blit(self.image, (0, 0))
        instructions1 = font_title3.render("MUSIC ", True, BLACK)
        self.screen.blit(instructions1, [120, 120])
        # ON SIGN
        pygame.draw.rect(self.screen, BLACK, [100, 220, 150, 80], 2)
        instructions1 = font_title3.render("ON!", True, BLACK)
        self.screen.blit(instructions1, [135, 240])
        # OFF SIGN
        pygame.draw.rect(self.screen, BLACK, [100, 340, 150, 80], 2)
        instructions1 = font_title3.render("OFF!", True, BLACK)
        self.screen.blit(instructions1, [123, 360])
        # Main Menu
        pygame.draw.rect(self.screen, WHITE, [278, 550, 100, 50])
        instructions1 = font_title.render("Menu", True, BLACK)
        self.screen.blit(instructions1, [300, 560])

        if (100 < mouseX < 100 + 150) and (220 < mouseY < 220 + 80) and mouse_pressed == 1:
            file = 'music.mp3'
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play(-1)
            pygame.event.wait()

        elif (100 < mouseX < 100 + 150) and (340 < mouseY < 340 + 80) and mouse_pressed == 1:
            pygame.mixer.music.stop()

        elif (278 < mouseX < 278 + 100) and (550 < mouseY < 550 + 50) and mouse_pressed == 1:
            screen_number = 0

    def closing_screen(self):
        # Closing screen where player is advanced after they die
        global game
        global screen_number
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
        mouse_pressed = pygame.mouse.get_pressed()[0]
        self.screen.blit(self.image, (0, 0))
        title = font_title3.render("YOU LOST!", True, BLACK)
        self.screen.blit(title, [70, 100])
        instructions1 = font_title2.render("Score: " + str(score), True, BLACK)
        self.screen.blit(instructions1, [150, 250])
        pygame.draw.rect(self.screen, WHITE, [278, 550, 100, 50])
        instructions1 = font_title.render("Done", True, BLACK)
        self.screen.blit(instructions1, [300, 560])
        if (278 < mouseX < 278 + 100) and (550 < mouseY < 550 + 50) and mouse_pressed == 1:
            self.done = True


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        global t
        pygame.sprite.Sprite.__init__(self)
        # Player class, user chooses to be either Dhrumik or Samyak
        a = random.randint(0, 1)
        if a == 0:
            self.image = pygame.image.load(os.path.join("dhrumik.png"))
            # self.image = pygame.image.load("dhrumik.png").convert()
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect(center=(189, 555))
        if a == 1:
            self.image = pygame.image.load(os.path.join("samyak.png"))
            # self.image = pygame.image.load("samyak.png").convert()
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect(center=(189, 535))


            ### self.screen.blit(instructions1, [300, 560])------------------------------------------------------------------------------------------------


class Bullet(pygame.sprite.Sprite):
    def __init__(self, ship):
        pygame.sprite.Sprite.__init__(self)
        # Bullet class
        self.image = pygame.image.load(os.path.join("bullet.png"))
        # self.image = pygame.image.load("bullet.png").convert()
        self.image.set_colorkey(BLACK)  # Transparent in background
        self.rect = self.image.get_rect()  # makes a hitbox
        self.rect.centerx = ship.rect.centerx  # x is now the player's x
        self.rect.centery = ship.rect.centery - 35  # y is now the player's y

    def update(self):
        # Move up 5 pixels per frame.
        self.rect.y -= 12


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        # Enemy class
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("monster.png"))
        # self.image = pygame.image.load("monster.png").convert()
        self.image.set_colorkey(BLACK)  # Transparent in background
        self.rect = self.image.get_rect()  # Makes a hit box
        self.rect.y = 0
        self.rect.x = random.randrange(0, 378)  # X speed is randomized
        self.speedy = random.randrange(3, 4)  # Y Speed is randomized

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > screen_height:
            self.rect.y = 50
            self.rect.x = random.randrange(0, 378)
            self.speedy = random.randrange(3, 4)


def main():
    pygame.init()
    pygame.display.set_caption('Space Game')
    clock = pygame.time.Clock()
    game = Game()

    while not game.done:
        global font_title
        global font
        global font_title2
        global font_title3
        # Fonts used in game
        font_title = pygame.font.SysFont("Rockwell Condensed", 25, True, False)
        font = pygame.font.SysFont("Times New Roman", 25, True, False)
        font_title2 = pygame.font.SysFont("Rockwell Condensed", 20, True, False)
        font_title3 = pygame.font.SysFont("Showcard Gothic", 40, True, False)
        # Screen number code to advance game to different screens
        if screen_number == 0:
            game.handle_events()
            game.starting_screen()
            pygame.display.flip()

        elif screen_number == 1:
            game.handle_events()
            game.update()
            game.draw()
            clock.tick(60)
            pygame.display.flip()

        elif screen_number == 2:
            game.handle_events()
            game.update()
            game.instructions()

        elif screen_number == 3:
            game.handle_events()
            game.update()
            game.screen3_music()

        elif screen_number == 4:
            game.handle_events()
            game.update()
            game.closing_screen()

        pygame.display.flip()


if __name__ == '__main__':
    main()
    pygame.quit()
    sys.exit()
