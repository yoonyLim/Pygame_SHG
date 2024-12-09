from typing import Tuple
import pygame as pg
import content.simulation_manger as sim

class TextBox():
    def __init__(self, x_pos: int, y_pos: int, text: str, font_family: str, font_size: int, color: Tuple[int, int, int], position: str = "center"):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.font_family = font_family
        self.font_size = font_size
        self.color = color
        self.position = position
        self.content = pg.font.SysFont(self.font_family, self.font_size, True).render(text, True, color)
        if position == "center":
            self.text_rect = self.content.get_rect(center = (self.x_pos, self.y_pos))
        else:
            self.text_rect = self.content.get_rect(topleft = (self.x_pos, self.y_pos))

    def update(self):
        if self.position == "center":
            self.text_rect = self.content.get_rect(center = (self.x_pos, self.y_pos))
        else:
            self.text_rect = self.content.get_rect(topleft = (self.x_pos, self.y_pos))
        sim.SCREEN.blit(self.content, self.text_rect)