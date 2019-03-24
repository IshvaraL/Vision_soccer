import pygame
from pygame.locals import *


class App:
    def __init__(self):
        self._running = True
        self._display = None
        self._image_surf = None
        self.size = self.weight, self.height = 549, 412
        self._image_surf = None

        self.player_1 = None
        self.player_2 = None
        self.player_3 = None
        self.player_4 = None
        self.player_5 = None
        self.player_6 = None

    def on_init(self):
        pygame.init()
        self._display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._image_surf = pygame.image.load("../pics/soccerfield_2d.png").convert()

        self.player_1 = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.player_1, (255, 0, 0), (15, 15), 15)

        self.player_2 = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.player_2, (255, 0, 0), (15, 15), 15)

        self.player_3 = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.player_3, (255, 0, 0), (15, 15), 15)

        self.player_4 = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.player_4, (0, 0, 255), (15, 15), 15)

        self.player_5 = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.player_5, (0, 0, 255), (15, 15), 15)

        self.player_6 = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.player_6, (0, 0, 255), (15, 15), 15)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            print("test")

    def on_loop(self):
        pass

    def on_render(self):
        self._display.blit(self._image_surf, (0, 0))
        self._display.blit(self.player_1, (50, 70))
        self._display.blit(self.player_2, (50, 140))
        self._display.blit(self.player_3, (50, 280))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()