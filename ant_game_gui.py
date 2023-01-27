from pygame.locals import *
import pygame
# Set the position of the text box
text_pos_1 = (90, 80)
text_pos_2 = (560, 50)
text_pos_3 = (560, 180)
text_pos_4 = (560, 310)
text_pos_5 = (560, 440)
text_pos_6 = (560, 570)

# Set the size of the bounding box
rect_size_1 = (500, 500)
rect_size_2 = (110, 75)

# Set the position of the bounding box
rect_pos_1 = (30, 170 )
rect_pos_2 = (560, 75)
rect_pos_3 = (560, 205)
rect_pos_4 = (560, 335)
rect_pos_5 = (560, 465)
rect_pos_6 = (560, 595)

# Set the color and thickness of the bounding box
rect_color = (92, 64, 51) # Dark Brown
rect_thickness = 2

ant_size = (20, 20)


class Ant:
    x = rect_pos_1[0]
    y = rect_pos_1[1]
    speed = 5

    def moveRight(self):
        if self.x < rect_pos_1[0] + rect_size_1[0] - ant_size[0]:
            self.x = self.x + self.speed

    def moveLeft(self):
        if self.x > rect_pos_1[0]:
            self.x = self.x - self.speed

    def moveUp(self):
        if self.y > rect_pos_1[1]:
            self.y = self.y - self.speed

    def moveDown(self):
        if self.y < rect_pos_1[1] + rect_size_1[1] - ant_size[1]:
            self.y = self.y + self.speed

class App:
    windowWidth = 700
    windowHeight = 700
    ant = 0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._image_surf_copy = None
        self.ant = Ant()
        self.clock = None
        self.timer_event = None
        self.timer_duration = 60
        self.isRight = True


    def on_init(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("main_bgm.mp3")
        pygame.mixer.music.play(loops=-1)

        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)

        pygame.display.set_caption('The Ant Game')
        self._running = True

        self._image_surf = pygame.image.load("ant.png").convert()
        self._image_surf.set_colorkey((0, 0, 0), RLEACCEL)
        self._image_surf = pygame.transform.scale(self._image_surf, ant_size)
        self._image_surf_copy = self._image_surf.copy()
        self._image_surf_right = pygame.transform.flip(self._image_surf_copy, True, False)
        self.ant_rect = self._image_surf.get_rect()
        self.ant_rect.center = (30, 170)
        self.clock = pygame.time.Clock() # Create a clock object to track the elapsed time
        self.timer_event = pygame.USEREVENT+1
        pygame.time.set_timer(self.timer_event, 1000)

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        # # Set the font and font size
        font_1 = pygame.font.Font(None, 70)
        font_2 = pygame.font.Font(None, 35)

        # Set the text and text color
        text_color = (48,19,1)
        text_1 = "THE ANT GAME"
        text_2 = "LEVEL"
        text_3 = "TIME"
        text_4 = "SCORE"
        text_5 = "SUGAR 1"
        text_6 = "SUGAR 2"

        # Render the text
        text_surface_1 = font_1.render(text_1, True, text_color)
        text_surface_2 = font_2.render(text_2, True, text_color)
        text_surface_3 = font_2.render(text_3, True, text_color)
        text_surface_4 = font_2.render(text_4, True, text_color)
        text_surface_5 = font_2.render(text_5, True, text_color)
        text_surface_6 = font_2.render(text_6, True, text_color)

        # Set the level to display
        level = 1
        level_font = pygame.font.Font(None, 50)
        level_text = level_font.render(str(level), True, text_color)
        level_pose = (605, 95)

        # Set the score to display
        score = 12
        score_font = pygame.font.Font(None, 40)
        score_text = level_font.render(str(score) + "/20", True, text_color)
        score_pose = (570, 360)

        # Load sugar icon image
        sugar_image = pygame.image.load("sugar_3.png")
        sugar_image = pygame.transform.scale(sugar_image, (55,55))
        sugar_rect = sugar_image.get_rect()
        sugar_rect.center = (615, 500)
        sugar_rect_2 = sugar_image.get_rect()
        sugar_rect_2.center= (615, 630)


        # Timer
        timer_font = pygame.font.Font(None, 40)
        clock_text = level_font.render(str(self.timer_duration), True, text_color)
        clock_pose = (595, 225)

        # Draw the background
        self._display_surf.fill((255,255,255))

        # Draw the text box
        self._display_surf.blit(text_surface_1, text_pos_1)
        self._display_surf.blit(text_surface_2, text_pos_2)
        self._display_surf.blit(text_surface_3, text_pos_3)
        self._display_surf.blit(text_surface_4, text_pos_4)
        self._display_surf.blit(text_surface_5, text_pos_5)
        self._display_surf.blit(text_surface_6, text_pos_6)

        # Draw the bounding box
        pygame.draw.rect(self._display_surf, rect_color, (rect_pos_1, rect_size_1), rect_thickness)
        pygame.draw.rect(self._display_surf, rect_color, (rect_pos_2, rect_size_2), rect_thickness)
        pygame.draw.rect(self._display_surf, rect_color, (rect_pos_3, rect_size_2), rect_thickness)
        pygame.draw.rect(self._display_surf, rect_color, (rect_pos_4, rect_size_2), rect_thickness)
        pygame.draw.rect(self._display_surf, rect_color, (rect_pos_5, rect_size_2), rect_thickness)
        pygame.draw.rect(self._display_surf, rect_color, (rect_pos_6, rect_size_2), rect_thickness)

        # Blit the text surface to the window
        self._display_surf.blit(level_text,level_pose)
        self._display_surf.blit(clock_text, clock_pose)
        self._display_surf.blit(score_text,score_pose)

        # Blit the sugar icon to the window
        self._display_surf.blit(sugar_image, sugar_rect)
        self._display_surf.blit(sugar_image, sugar_rect_2)

        # Blit the ant icon to the window
        # self._display_surf.blit(self._image_surf_right, (self.ant.x,self.ant.y))
        if self.isRight:
            self._display_surf.blit(self._image_surf_right, (self.ant.x,self.ant.y))
        else:
            self._display_surf.blit(self._image_surf, (self.ant.x,self.ant.y))
        # Update the display
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            self.clock.tick(60)
            pygame.event.pump()

            for event in pygame.event.get():
                if event.type == self.timer_event:
                    self.timer_duration -= 1
                    if self.timer_duration < 0:
                        self.timer_duration = 60
                        pygame.time.set_timer(self.timer_event, 1000)

            keys = pygame.key.get_pressed()

            if (keys[K_RIGHT]):
                self.isRight = True
                self.ant.moveRight()

            if (keys[K_LEFT]):
                self.isRight = False
                self.ant.moveLeft()

            if (keys[K_UP]):
                self.ant.moveUp()

            if (keys[K_DOWN]):
                self.ant.moveDown()

            if (keys[K_ESCAPE]):
                self._running = False

            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
