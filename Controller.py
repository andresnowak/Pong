import pygame
from enum import Enum


class ControllerKeyTypes(Enum):
    KEY_UP = 1
    KEY_DOWN = 2


class Controller:
    def __init__(self, **kwargs):
        self.controller_keys_activated = {
            ControllerKeyTypes.KEY_UP: False, ControllerKeyTypes.KEY_DOWN: False}

        self.controller_keys = {}
        self.controller_keys[kwargs["up"]] = ControllerKeyTypes.KEY_UP
        self.controller_keys[kwargs["down"]] = ControllerKeyTypes.KEY_DOWN

    def action_activated(self, event):
        if event.type == pygame.KEYDOWN:
            self.controller_keys_activated[self.controller_keys.get(
                event.key)] = True
        elif event.type == pygame.KEYUP:
            self.controller_keys_activated[self.controller_keys.get(
                event.key)] = False

        return self.controller_keys_activated
