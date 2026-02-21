import pygame
from helpers.asstes import Assets

class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.onclick = False
        self.hoverBackgroundColor = "blue"

    def display(self, screen, events):
        isMouseOverButton = self.isMouseOverButton(events)
        borderColor = "white"
        if (isMouseOverButton):
            backgroundColor = self.hoverBackgroundColor
            textColor = "white"
        else:
            backgroundColor = "grey"
            textColor = (40, 40, 40)
        font = pygame.font.Font(None, 35) 
        text = font.render(self.text, True, textColor)
        pygame.draw.rect(screen, backgroundColor, (
            self.x,
            self.y,
            self.width,
            self.height,
        ))
        pygame.draw.line(
            screen,
            borderColor, 
            (self.x, self.y), 
            (self.x + self.width, self.y)
        ),
        pygame.draw.line(
            screen,
            borderColor, 
            (self.x, self.y), 
            (self.x, self.y + self.height)
        )
        pygame.draw.line(
            screen,
            borderColor, 
            (self.x + self.width, self.y), 
            (self.x + self.width, self.y + self.height)
        )
        pygame.draw.line(
            screen,
            borderColor, 
            (self.x, self.y + self.height), 
            (self.x + self.width, self.y + self.height)
        )
        textRect = text.get_rect()
        centerX = self.x + self.width / 2
        centerY = self.y + self.height / 2
        textRect.center = (centerX, centerY)
        screen.blit(text, textRect)
        if (self.onclick and events.MOUSEBUTTONDOWN and isMouseOverButton):
            if self.onclick:
                Assets.play('click3.wav')
                if callable(self.onclick):
                    self.onclick()
                else:
                    self.onclick[0](self.onclick[1])

    def setOnclick(self, callback):
        self.onclick = callback

    def setHoverBackgroudColor(self, color):
        self.hoverBackgroundColor = color

    def isMouseOverButton(self, events):
        x, y = pygame.mouse.get_pos()
        if (
            x >= self.x 
            and x <= self.x + self.width 
            and y >= self.y 
            and y <= self.y + self.height
        ):
            return True
        return False