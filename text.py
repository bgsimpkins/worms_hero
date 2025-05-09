import pygame as pg


class DebugPanel:
    def __init__(self, screen):
        self.mess_render_list = []
        self.screen = screen

        self.font = pg.font.SysFont("comicsansms", 18)

    def add_message(self, m):
        self.mess_list.append(m)

    def set_message_list(self, m_list):
        self.mess_render_list.clear()
        for m in m_list:
            self.mess_render_list.append(self.font.render(m, True, (200, 200, 200)))

    def render(self):
        y = 10
        for m in self.mess_render_list:
            self.screen.blit(m, (10, y))
            y += 30


