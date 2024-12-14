from typing import Tuple
import pygame as pg
import content.simulation_manger as sim

class Button():
    def __init__(self, x_pos: int, y_pos: int, text: str, font_family: str, font_size: int, color: Tuple[int, int, int], index: int):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.font_family = font_family
        self.font_size = font_size
        self.color = color
        self.index = index
        self.content = pg.font.SysFont(font_family, font_size).render(text, True, color)
        self.text_rect = self.content.get_rect(center = (self.x_pos, self.y_pos))

    def checkForInput(self, position: Tuple[int, int]):
        if self.text_rect.collidepoint(position):
            return True
        
    def setColor(self, color):
        self.color = color

    def checkForHovering(self, position: Tuple[int, int]):
        if self.text_rect.collidepoint(position):
            self.content = pg.font.SysFont(self.font_family, self.font_size).render(self.text, True, sim.BUTTON_HOVERED_COLOR)
        else:
            self.content = pg.font.SysFont(self.font_family, self.font_size).render(self.text, True, self.color)

    def update(self):
        self.checkForHovering(pg.mouse.get_pos())
        self.text_rect = self.content.get_rect(center = (self.x_pos, self.y_pos))
        sim.SCREEN.blit(self.content, self.text_rect)